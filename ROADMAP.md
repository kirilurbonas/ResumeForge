# ResumeForge – Further Roadmap

Prioritized ideas for what to do next. Order is approximate; pick by impact and time.

---

## 1. Reliability & production readiness

| Item | Description | Effort |
|------|-------------|--------|
| **Rate limiting** | Throttle API by IP or user (e.g. `slowapi` or custom middleware) to protect against abuse. | Small |
| **Run migrations in Docker** | Run `alembic upgrade head` on backend startup or in a one-off init container so deploys stay in sync with schema. | Small |
| **Health check depth** | Extend `GET /api/health` to optionally check DB connectivity and critical deps (ChromaDB, optional). | Small |
| **Structured logging** | JSON logs, log levels from env, request IDs for tracing. | Small |

---

## 2. Testing

| Item | Description | Effort |
|------|-------------|--------|
| **Backend API tests** | pytest + FastAPI `TestClient`: auth (register, login, 401), resume upload/list/delete, templates, health. Use a test DB or SQLite in-memory. | Medium |
| **Backend unit tests** | Pytest for a few critical services (e.g. resume parser, auth helpers) with mocked LLM/Chroma. | Medium |
| **Frontend unit tests** | Vitest + React Testing Library: key components (Login, ResumeUpload, ErrorBoundary), hooks (useToast). | Medium |
| **E2E tests** | Playwright or Cypress: login → upload → view analysis → generate. Optional, higher maintenance. | Large |

---

## 3. UX & product

| Item | Description | Effort |
|------|-------------|--------|
| **React Router** | URL-based routes: `/`, `/login`, `/resumes`, `/upload`, `/analysis/:resumeId`, etc. Enables shareable links and correct 401 redirect. | Medium |
| **Password reset** | “Forgot password” flow (email link or token) with secure token storage and expiry. | Medium |
| **Dark mode** | Toggle using existing design tokens (CSS variables); persist preference in localStorage. | Small |
| **Export analysis** | “Download analysis report” as PDF (or HTML) from the Analysis tab. | Small–Medium |

---

## 4. Storage & scale

| Item | Description | Effort |
|------|-------------|--------|
| **S3 for generated files** | Store generated PDF/DOCX in S3 (or local volume); return a download link or signed URL so users can re-download without regenerating. | Medium |
| **Optional: keep original file** | Store uploaded PDF/DOCX in S3 and reference it from DB; keep current “parse to JSON only” as an option. | Medium |

---

## 5. Developer experience & ops

| Item | Description | Effort |
|------|-------------|--------|
| **Frontend lint in CI** | Add ESLint (and optionally Prettier), `npm run lint` in CI. | Small |
| **Pre-commit hooks** | Run flake8, eslint, and optionally tests before commit (e.g. husky + lint-staged). | Small |
| **Docker Compose env** | Pass `JWT_SECRET_KEY`, `DATABASE_URL`, and `CORS_ORIGINS` via env file so production-like runs are easy. | Small |

---

## 6. Security hardening

| Item | Description | Effort |
|------|-------------|--------|
| **Rate limiting** | See §1. | Small |
| **Shorter access token + refresh** | Shorter-lived access token (e.g. 15 min) + refresh token stored in httpOnly cookie or secure storage. | Medium |
| **Security headers** | CORS, CSP, X-Frame-Options, etc. (FastAPI middleware and/or reverse proxy). | Small |

---

## 7. Features

| Item | Description | Effort |
|------|-------------|--------|
| **Compare versions** | Side-by-side or diff view for two resume versions. | Medium |
| **Duplicate resume** | “Copy resume” to create a new resume from an existing one (new id, same content). | Small |
| **Resume search** | Search by filename or date in addition to existing industry/tag filters. | Small |
| **Email verification** | Optional email verification on signup before full access. | Medium |

---

## Suggested order (if starting from scratch)

1. **Rate limiting** + **migrations in Docker** + **health check** – quick production hardening.
2. **React Router** – better UX and correct 401 behavior.
3. **Backend API tests** – confidence for refactors and new features.
4. **S3 for generated files** or **Export analysis** – clear user value.
5. **Frontend tests** and **ESLint in CI** – quality and consistency.
6. **Password reset** or **Dark mode** – next UX wins.

---

*This roadmap is a living list; adjust priorities to match your goals (portfolio vs. production vs. learning).*
