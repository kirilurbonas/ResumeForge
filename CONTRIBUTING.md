# Contributing to ResumeForge

Thank you for your interest in contributing to ResumeForge! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/ResumeForge.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m "Add your meaningful commit message"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp ../.env.example ../.env
# Edit .env and add your OPENAI_API_KEY
```

5. Run the development server:
```bash
uvicorn app.main:app --reload
```

### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Code Style

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for all functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### JavaScript/React (Frontend)

- Use ES6+ features
- Follow React best practices
- Use functional components with hooks
- Keep components small and focused
- Use meaningful variable and function names

## Commit Messages

Write clear, descriptive commit messages:

- Use present tense: "Add feature" not "Added feature"
- Use imperative mood: "Fix bug" not "Fixed bug"
- Keep the first line under 50 characters
- Add more details in the body if needed

Example:
```
Add file size validation to upload endpoint

- Validate file size before processing
- Return clear error messages for oversized files
- Update MAX_FILE_SIZE constant
```

## Pull Request Process

1. Ensure your code follows the project's style guidelines
2. Update documentation if you've changed functionality
3. Add tests if applicable
4. Ensure all tests pass
5. Update the README.md if needed
6. Request review from maintainers

## Reporting Issues

When reporting issues, please include:

- Clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, Node version)
- Screenshots if applicable

## Feature Requests

For feature requests, please:

- Check if the feature already exists or has been requested
- Provide a clear description of the feature
- Explain the use case and benefits
- Consider implementation complexity

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

Thank you for contributing to ResumeForge! 🚀
