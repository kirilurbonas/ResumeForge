"""LLM service for generating resume improvement suggestions."""

import asyncio
import logging
import os
import time
from abc import ABC, abstractmethod
from typing import AsyncIterator, List, Optional

logger = logging.getLogger(__name__)


class LLMGenerationError(Exception):
    """Raised when the LLM provider fails after retries (callers map to HTTP 503 / llm_error payload)."""

    def __init__(self, message: str, code: str = "llm_provider_error"):
        self.message = message
        self.code = code
        super().__init__(message)


class LLMService(ABC):
    """Abstract base class for LLM services."""

    @abstractmethod
    async def generate_suggestions(
        self,
        resume_text: str,
        analysis_results: dict,
        suggestion_type: str = "general",
    ) -> str:
        """Generate improvement suggestions for resume."""
        raise NotImplementedError

    @abstractmethod
    async def stream_suggestions(
        self,
        resume_text: str,
        analysis_results: dict,
        suggestion_type: str = "general",
    ) -> AsyncIterator[str]:
        """Stream suggestions."""
        raise NotImplementedError


class OpenAIService(LLMService):
    """OpenAI LLM service implementation."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError("openai package is required. Install with: pip install openai") from e

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

        self.model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
        timeout = float(os.getenv("OPENAI_TIMEOUT_SECONDS", "60"))
        self.client = OpenAI(api_key=self.api_key, timeout=timeout)

    def _chat_completions_create(self, **kwargs):
        """Sync chat.completions.create with retries on transient failures."""
        from openai import (
            APIConnectionError,
            APIStatusError,
            APITimeoutError,
            RateLimitError,
        )

        delays = (0.6, 1.2, 2.4)
        last_error: Optional[Exception] = None

        for attempt in range(3):
            try:
                return self.client.chat.completions.create(**kwargs)
            except (APIConnectionError, APITimeoutError, RateLimitError) as e:
                last_error = e
                logger.warning("OpenAI transient error (attempt %s): %s", attempt + 1, e)
                if attempt < 2:
                    time.sleep(delays[attempt])
            except APIStatusError as e:
                last_error = e
                if getattr(e, "status_code", 0) and e.status_code >= 500 and attempt < 2:
                    logger.warning("OpenAI 5xx (attempt %s): %s", attempt + 1, e)
                    time.sleep(delays[attempt])
                    continue
                raise LLMGenerationError(str(e), code="llm_api_error") from e
            except Exception as e:
                raise LLMGenerationError(str(e), code="llm_error") from e

        raise LLMGenerationError(
            str(last_error) if last_error else "LLM request failed",
            code="llm_unavailable",
        ) from last_error

    def _build_suggestion_prompt(
        self, resume_text: str, analysis_results: dict, suggestion_type: str
    ) -> str:
        """Build prompt for resume suggestions (resume body trimmed in code, not in the prompt text)."""
        ats_score = analysis_results.get("ats_score", 0)
        strengths = analysis_results.get("strengths", [])
        weaknesses = analysis_results.get("weaknesses", [])
        snippet = (resume_text or "")[:2000]

        return f"""You are an expert resume writer and career coach. Analyze this resume and provide specific, actionable improvement suggestions.

Resume Text:
{snippet}

Current Analysis:
- ATS Score: {ats_score}/100
- Strengths: {", ".join(strengths[:5]) if strengths else "None"}
- Weaknesses: {", ".join(weaknesses[:5]) if weaknesses else "None"}

Please provide {suggestion_type} improvement suggestions. Be specific and actionable. Format your response as a bulleted list of suggestions.

Suggestions:"""

    async def generate_suggestions(
        self,
        resume_text: str,
        analysis_results: dict,
        suggestion_type: str = "general",
    ) -> str:
        """Generate improvement suggestions using OpenAI API."""
        prompt = self._build_suggestion_prompt(resume_text, analysis_results, suggestion_type)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert resume writer and career coach. "
                    "Provide specific, actionable suggestions to improve resumes."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        def _call():
            return self._chat_completions_create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800,
            )

        response = await asyncio.to_thread(_call)
        content = response.choices[0].message.content
        if not content:
            raise LLMGenerationError("Empty model response", code="llm_empty_response")
        return content

    async def stream_suggestions(
        self,
        resume_text: str,
        analysis_results: dict,
        suggestion_type: str = "general",
    ) -> AsyncIterator[str]:
        """Stream suggestions using OpenAI API."""
        prompt = self._build_suggestion_prompt(resume_text, analysis_results, suggestion_type)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert resume writer and career coach. "
                    "Provide specific, actionable suggestions to improve resumes."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        try:

            def _stream():
                return self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=800,
                    stream=True,
                )

            stream = await asyncio.to_thread(_stream)
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except LLMGenerationError:
            raise
        except Exception as e:
            logger.error("Streaming suggestions failed: %s", e, exc_info=True)
            yield f"Error generating suggestions: {e!s}"

    def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate text from a prompt (synchronous)."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]

        def _call():
            return self._chat_completions_create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=max_tokens,
            )

        response = _call()
        content = response.choices[0].message.content
        if not content:
            raise LLMGenerationError("Empty model response", code="llm_empty_response")
        return content

    async def _generate_text_async(self, prompt: str, max_tokens: int) -> str:
        """Async text generation."""

        def _call():
            return self.generate_text(prompt, max_tokens=max_tokens)

        return await asyncio.to_thread(_call)

    async def generate_action_verbs(self, job_description: str = None) -> List[str]:
        """Generate strong action verb suggestions."""
        prompt = """Provide a list of 10-15 strong action verbs that are effective for resume bullet points.
Focus on verbs that demonstrate impact and achievement (e.g., 'achieved', 'implemented', 'optimized').
Format as a simple comma-separated list."""
        messages = [
            {"role": "system", "content": "You are a resume writing expert."},
            {"role": "user", "content": prompt},
        ]

        try:

            def _call():
                return self._chat_completions_create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=200,
                )

            response = await asyncio.to_thread(_call)
            content = response.choices[0].message.content or ""
            verbs = [v.strip() for v in content.split(",")]
            return verbs[:15]
        except LLMGenerationError:
            return [
                "achieved",
                "improved",
                "increased",
                "developed",
                "created",
                "designed",
                "implemented",
                "managed",
                "led",
                "optimized",
                "enhanced",
                "streamlined",
                "established",
                "launched",
                "built",
            ]

    async def rewrite_section(self, section_text: str, section_type: str = "experience") -> str:
        """Rewrite a resume section to be more impactful."""
        prompt = f"""Rewrite this {section_type} section from a resume to be more impactful and use stronger action verbs.
Keep it concise and focused on achievements.

Original:
{section_text}

Rewritten:"""
        messages = [
            {
                "role": "system",
                "content": "You are an expert resume writer. Rewrite sections to be more impactful.",
            },
            {"role": "user", "content": prompt},
        ]

        try:

            def _call():
                return self._chat_completions_create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=300,
                )

            response = await asyncio.to_thread(_call)
            return response.choices[0].message.content or section_text
        except LLMGenerationError:
            return section_text


def get_llm_service(provider: str = "openai", **kwargs) -> LLMService:
    """Factory function to get LLM service instance."""
    provider = provider.lower()
    if provider == "openai":
        return OpenAIService(**kwargs)
    raise ValueError(f"Unknown LLM provider: {provider}. Only 'openai' is supported.")


llm_service = None


def initialize_llm_service():
    """Initialize the global LLM service instance."""
    global llm_service
    provider = os.getenv("LLM_PROVIDER", "openai")
    llm_service = get_llm_service(
        provider=provider,
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("LLM_MODEL"),
    )
