# ResumeForge

An intelligent resume analysis and optimization system that helps job seekers improve their resumes. Upload your resume, get AI-powered analysis, ATS optimization suggestions, skills gap analysis, format improvements, select from professional templates, and generate polished resumes in DOC or PDF format.

## 🚀 Features

- **Resume Parsing**: Extract structured data from PDF/DOCX resumes
- **AI-Powered Analysis**: Get strengths, weaknesses, and ATS compatibility scores
- **ATS Optimization**: Optimize your resume for Applicant Tracking Systems
- **Skills Gap Analysis**: Compare your resume against job descriptions
- **Format Improvement**: AI-powered format optimization suggestions
- **Template Selection**: Choose from 4 professional templates (Modern, Classic, ATS-Friendly, Minimalist)
- **Resume Generation**: Export polished resumes in DOC or PDF format
- **Job Matching**: Match your resume to specific job descriptions

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
- **sentence-transformers**: For resume/job description embeddings
- **ChromaDB**: Vector database for semantic matching
- **PyPDF2 / python-docx**: Resume parsing and DOC generation
- **reportlab**: PDF generation
- **OpenAI API**: LLM for analysis and suggestions

### Frontend
- **React + Vite**: UI framework
- **Axios**: HTTP client
- **Modern CSS**: Responsive design

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
cd Aiport2
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

5. Run the server:
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

### Supported File Types

- PDF (`.pdf`)
- Microsoft Word (`.docx`, `.doc`)

## 📖 Usage

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

- `GET /api/templates` - List available templates
- `GET /api/templates/{id}` - Get template details
- `POST /api/resume/{id}/improve-format` - Apply format improvements
- `POST /api/resume/{id}/generate` - Generate resume (query params: template_id, format=doc|pdf)

#### System

- `GET /api/health` - Health check

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
```

3. **Run in production mode**:
```bash
docker-compose up -d
```

## 💻 Development

### Project Structure

```
resume-forge/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # Data models
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   ├── templates/        # Resume templates
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   └── services/     # API clients
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🔮 Future Enhancements

- Multiple resume versions management
- Industry-specific templates
- Cover letter generation
- Interview question preparation
- Advanced template customization
- Resume version history

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Embeddings powered by [sentence-transformers](https://www.sbert.net/)
- UI framework: [React](https://react.dev/)
- Resume generation: [python-docx](https://python-docx.readthedocs.io/) and [reportlab](https://www.reportlab.com/)

---

**Note**: ResumeForge is a portfolio project demonstrating AI-powered resume analysis, full-stack development, and ML integration. For production use, consider additional security, scalability, and monitoring features.
