# ResumeForge

[![CI](https://github.com/kirilurbonas/ResumeForge/actions/workflows/ci.yml/badge.svg)](https://github.com/kirilurbonas/ResumeForge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent resume analysis and optimization system that helps job seekers improve their resumes. Upload your resume, get AI-powered analysis, ATS optimization suggestions, skills gap analysis, format improvements, select from professional templates, and generate polished resumes in DOC or PDF format.

## ✨ Key Features

- **Resume Parsing**: Extract structured data from PDF/DOCX resumes
- **AI-Powered Analysis**: Get strengths, weaknesses, and ATS compatibility scores
- **ATS Optimization**: Optimize your resume for Applicant Tracking Systems
- **Skills Gap Analysis**: Compare your resume against job descriptions
- **Format Improvement**: AI-powered format optimization suggestions
- **Template Selection**: Choose from 7+ professional templates including industry-specific options
- **Resume Generation**: Export polished resumes in DOC or PDF format
- **Job Matching**: Match your resume to specific job descriptions
- **Version Management**: Track and manage multiple versions of your resume
- **Cover Letter Generation**: AI-powered cover letter creation based on your resume and job description
- **Interview Preparation**: Generate interview questions and suggested answers
- **Template Customization**: Customize templates with advanced parameters
- **Industry-Specific Templates**: Templates optimized for Tech, Finance, Healthcare, and more


## 🏗️ Architecture

```
┌─────────────┐
│   Frontend  │  React Application
│  (React)    │  - Resume Upload
└──────┬──────┘  - Analysis Dashboard
       │         - Template Selection
       │ HTTP    - Resume Generation
       ▼
┌─────────────┐
│   Backend   │  FastAPI Application
│  (FastAPI)  │  - REST API
└──────┬──────┘  - Resume Processing
       │
       ├─────────┐
       │         │
       ▼         ▼
┌──────────┐  ┌──────────────┐
│ Resume   │  │   Embedding  │
│ Parser   │  │    Model     │
└────┬─────┘  └──────┬───────┘
     │               │
     │               ▼
     │         ┌──────────────┐
     │         │ Vector Store │
     │         │  (ChromaDB)  │
     │         └──────┬───────┘
     │                │
     └────────────────┘
              │
              ▼
       ┌──────────────┐
       │  LLM Service │
       │ (OpenAI/Local)│
       └──────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM (SQLite for development, PostgreSQL/MySQL for production)
- **JWT**: Authentication with python-jose
- **Bcrypt**: Password hashing
- **sentence-transformers**: For resume/job description embeddings
- **ChromaDB**: Vector database for semantic matching
- **PyPDF2 / python-docx**: Resume parsing and DOC generation
- **reportlab**: PDF generation
- **OpenAI API**: LLM for analysis and suggestions
- **Boto3**: AWS S3 integration for cloud storage (optional; not used for resume persistence by default)

**Data storage:** Uploaded resume files are parsed and stored as structured JSON in the database (SQLite/PostgreSQL). Raw PDF/DOCX files are not persisted; only the extracted content is. S3/cloud storage is available in the codebase for future use (e.g. storing generated PDF/DOCX outputs).

### Frontend
- **React + Vite**: UI framework
- **Axios**: HTTP client with JWT interceptors
- **Modern CSS**: Design system (variables, tokens), responsive layout, toast notifications, error boundary

### Infrastructure
- **Docker & Docker Compose**: Containerization

## 📦 Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose (optional, for containerized deployment)
- OpenAI API key (if using OpenAI LLM)

## 🔧 Installation

### Option 1: Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ResumeForge.git
cd ResumeForge
```

2. Create a `.env` file:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. Start the services:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
export LLM_PROVIDER=openai
export LLM_MODEL=gpt-3.5-turbo
export EMBEDDING_MODEL=all-MiniLM-L6-v2
```

5. Run database migrations (recommended for new installs or schema updates):
```bash
alembic upgrade head
```
The app also creates tables on startup if they do not exist.

6. Run the server:
```bash
uvicorn app.main:app --reload
```

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

4. Access the application at http://localhost:3000

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for LLM | Required |
| `LLM_PROVIDER` | LLM provider: `openai` | `openai` |
| `LLM_MODEL` | Model name (e.g., `gpt-3.5-turbo`) | `gpt-3.5-turbo` |
| `EMBEDDING_MODEL` | Embedding model name | `all-MiniLM-L6-v2` |
| `VITE_API_URL` | Backend API URL for frontend | `http://localhost:8000/api` |
| `MAX_FILE_SIZE` | Maximum file upload size in bytes | `10485760` (10MB) |
| `CORS_ORIGINS` | Comma-separated list of allowed origins | `http://localhost:3000,http://localhost:5173` |
| `JWT_SECRET_KEY` | Secret key for JWT signing (required in production) | Random per process if unset |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token lifetime in minutes | `43200` (30 days) |
| `DATABASE_URL` | Database connection string | `sqlite:///./resumeforge.db` |
| `STORAGE_TYPE` | Storage type: `local` or `s3` | `local` |
| `S3_BUCKET_NAME` | AWS S3 bucket name (if using S3) | Required for S3 |
| `AWS_ACCESS_KEY_ID` | AWS access key (if using S3) | Required for S3 |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key (if using S3) | Required for S3 |
| `AWS_REGION` | AWS region (if using S3) | `us-east-1` |

### Supported File Types

- PDF (`.pdf`) - Maximum size: 10MB
- Microsoft Word (`.docx`, `.doc`) - Maximum size: 10MB

**Note**: File size limits can be configured via the `MAX_FILE_SIZE` environment variable.

## 📖 Usage

### Getting Started

1. **Register an account**: Create a new account with your email and username
2. **Login**: Use your credentials to login
3. **Upload your resume**: Upload your resume file (PDF or DOCX)
4. **Analyze and optimize**: Use the analysis tools to improve your resume
5. **Generate**: Create polished resumes with professional templates

### Uploading a Resume

1. Navigate to the "Upload Resume" tab
2. Click "Choose File" and select your resume (PDF or DOCX)
3. Click "Upload Resume"
4. Wait for processing

### Analyzing Your Resume

1. After upload, navigate to the "Analysis" tab
2. View your ATS compatibility score
3. Review strengths and areas for improvement
4. Check improvement suggestions

### Generating a Resume

1. Navigate to the "Templates & Generate" tab
2. Select a template (Modern, Classic, ATS-Friendly, or Minimalist)
3. Choose output format (DOCX or PDF)
4. Click "Generate & Download"
5. Your formatted resume will download automatically

## 📡 API Documentation

### Endpoints

#### Resume Management

- `POST /api/resume/upload` - Upload and parse resume
- `GET /api/resume/{id}` - Get parsed resume data
- `DELETE /api/resume/{id}` - Delete a resume

#### Analysis

- `POST /api/resume/{id}/analyze` - Run full analysis
- `POST /api/resume/{id}/ats-optimize` - Get ATS suggestions
- `POST /api/resume/{id}/match-job` - Match resume to job description
- `GET /api/resume/{id}/suggestions` - Get improvement suggestions

#### Templates & Generation

- `GET /api/templates` - List available templates (query param: industry)
- `GET /api/templates/{id}` - Get template details
- `GET /api/industries` - List industries with specific templates
- `POST /api/resume/{id}/improve-format` - Apply format improvements
- `POST /api/resume/{id}/generate` - Generate resume (query params: template_id, format=doc|pdf)
- `POST /api/resume/{id}/generate-custom` - Generate resume with custom template parameters

#### Version Management

- `POST /api/resume/{id}/version` - Create a new version of a resume
- `GET /api/resume/{id}/versions` - List all versions of a resume
- `GET /api/resume/{id}/version/{version}` - Get a specific version
- `PUT /api/resume/{id}` - Update resume metadata (industry, tags)
- `GET /api/resumes` - List all resumes (query params: industry, tag)

#### Cover Letters

- `POST /api/resume/{id}/cover-letter` - Generate a cover letter

#### Interview Preparation

- `POST /api/resume/{id}/interview-questions` - Generate interview questions
- `POST /api/resume/{id}/interview-answer` - Get suggested answer for a question

#### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get access token
- `GET /api/auth/me` - Get current user information (requires auth)

#### System

- `GET /api/health` - Health check (public, no auth required)

**Note**: All resume endpoints require authentication. Include the JWT token in the Authorization header: `Bearer <token>`

Full API documentation available at http://localhost:8000/docs (Swagger UI)

## 🚢 Deployment

### Production Deployment

1. **Build Docker images**:
```bash
docker-compose build
```

2. **Set production environment variables**:
```bash
# Edit docker-compose.yml or use .env file
# Required: OPENAI_API_KEY, JWT_SECRET_KEY (use a strong random value)
# Update CORS_ORIGINS for your frontend domain
```

3. **Run database migrations** (if using Alembic):
```bash
cd backend && alembic upgrade head
```

4. **Run in production mode**:
```bash
docker-compose up -d
```

5. **Check service health**:
```bash
curl http://localhost:8000/api/health
```

### Security Considerations

- **API Keys**: Never commit API keys to version control. Use environment variables or secrets management.
- **CORS**: Configure `CORS_ORIGINS` appropriately for production to restrict access.
- **File Uploads**: File size limits are enforced (default 10MB). Adjust `MAX_FILE_SIZE` as needed.
- **Rate Limiting**: Consider adding rate limiting for production deployments.
- **HTTPS**: Always use HTTPS in production environments.
- **Database**: For production, use PostgreSQL or MySQL instead of SQLite.
- **Cloud Storage**: Configure S3 or other cloud storage for file persistence.
- **JWT Secret**: Use a strong, randomly generated secret key for JWT tokens in production.

## 💻 Development

### Project Structure

```
ResumeForge/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes (auth, resume, templates)
│   │   ├── models/       # Pydantic and data models
│   │   ├── services/     # Business logic (auth, storage, LLM, parser, etc.)
│   │   └── utils/        # Utilities
│   ├── alembic/          # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── templates/        # Resume templates (JSON)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/   # React components (auth, resume, UI primitives)
│   │   ├── context/      # React context (e.g. Toast)
│   │   ├── hooks/        # Custom hooks (e.g. useToast)
│   │   ├── services/     # API client
│   │   └── styles/       # Design system (variables, design-system.css)
│   ├── package.json
│   └── Dockerfile
├── .github/workflows/    # CI (backend lint, frontend build, Docker build)
├── docker-compose.yml
├── .env.example          # Environment variables template
├── CONTRIBUTING.md
├── LICENSE               # MIT
└── README.md
```

### Code Quality

- **Backend**: Python code follows PEP 8 style guide with type hints
- **Frontend**: React best practices with functional components
- **Logging**: Structured logging for debugging and monitoring
- **Error Handling**: Comprehensive error handling with meaningful messages

### Running Linters and Builds

```bash
# Backend: lint and verify imports
cd backend
pip install flake8
flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 app --max-line-length=100 --exit-zero
python -c "import app.main; print('Import OK')"

# Database migrations (when schema changes)
alembic upgrade head
# Create a new migration after editing app/database models:
# alembic revision --autogenerate -m "description"

# Frontend: build
cd frontend
npm run build
```

### Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style and standards
- Commit message conventions
- Pull request process
- Reporting issues

## 🔮 Roadmap

**Completed** (see [Project Status](#-project-status) for details): resume parsing, AI analysis, ATS optimization, templates & generation, version management, industry templates, cover letter, interview prep, auth, design system, toasts, migrations, and CI.

**Next (suggested order):**

1. **Reliability** – Rate limiting, run Alembic in Docker, deeper health checks, structured logging  
2. **React Router** – URL-based routes for shareable links and correct 401 flow  
3. **Backend tests** – pytest + TestClient for API and critical services  
4. **User value** – S3 for generated PDF/DOCX or export analysis as PDF  
5. **Frontend quality** – Vitest + React Testing Library, ESLint in CI  
6. **UX** – Password reset, dark mode, compare versions, duplicate resume, resume search  

**Also under consideration:** Backend and frontend unit tests, E2E tests (Playwright/Cypress), security headers, refresh tokens, pre-commit hooks, email verification.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📧 Support

For issues, questions, or feature requests, please open an issue on GitHub.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Embeddings powered by [sentence-transformers](https://www.sbert.net/)
- UI framework: [React](https://react.dev/)
- Resume generation: [python-docx](https://python-docx.readthedocs.io/) and [reportlab](https://www.reportlab.com/)

---

## 📊 Project Status

**Current Version**: 1.0.0

**Status**: Active Development

**Included**: JWT auth (secret from env), Alembic migrations, design system and responsive UI, toast notifications, error boundary, confirm dialogs, empty states, drag-and-drop upload, accessibility (focus, skip link), and CI (backend lint, frontend build, Docker build).

**Note**: ResumeForge is a portfolio project demonstrating AI-powered resume analysis, full-stack development, and ML integration. For production use, set `JWT_SECRET_KEY`, consider rate limiting, and use PostgreSQL/MySQL with HTTPS.

## 🎯 Roadmap (done)

- [x] Basic resume parsing (PDF/DOCX)
- [x] AI-powered analysis
- [x] ATS optimization
- [x] Template-based resume generation
- [x] Multiple resume versions management
- [x] Industry-specific templates
- [x] Cover letter generation
- [x] Interview question preparation
- [x] Advanced template customization
- [x] Resume version history
- [x] User authentication
- [x] Design system, toasts, error boundary, accessibility
- [x] Alembic migrations, JWT from env, CI fixes
