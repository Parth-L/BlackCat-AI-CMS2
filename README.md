# BlackCat AI CMS

[![Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)](https://github.com/yourusername/blackcat-ai/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

> **AI-Powered Content Research, Creation & Publishing Platform**

Build an AI-powered content operating system that researches viral content, extracts writing patterns (not copies), generates original branded content, designs post assets, schedules publishing, and tracks performance.

**Goal:** Reduce content creation time from 2 hours to under 5 minutes while maintaining originality.

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Database Schema](#-database-schema)
- [Version History](#-version-history)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/blackcat-ai.git
cd blackcat-ai/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Access API docs
open http://localhost:8000/docs
```

---

## ✨ Features

### Core Modules

| Module | Description | Status |
|--------|-------------|--------|
| **Idea Vault** | Store ideas, quotes, observations, Reddit posts, tweets, book notes | ✅ Implemented |
| **Pattern Analyzer** | Extract writing patterns from viral content | 🔄 In Progress |
| **AI Writer** | Generate original content from themes | 🔄 In Progress |
| **Series Manager** | Organize content into series with automatic numbering | ✅ Implemented |
| **Template Engine** | Create Instagram Reels, PNGs, MP4s, Carousels, Stories | 📋 Planned |
| **Caption Generator** | Generate captions with keywords, emojis, CTAs | 🔄 In Progress |
| **Audio Recommendation** | Suggest trending audio based on mood | ✅ Implemented |
| **Scheduler** | Calendar-based scheduling for multiple platforms | 🔄 In Progress |
| **Analytics Dashboard** | Track views, likes, comments, shares, saves | ✅ Implemented |
| **Experiment Manager** | A/B testing for content variations | ✅ Implemented |
| **Content Calendar** | Monthly view with upcoming posts | 📋 Planned |
| **AI Coach** | Weekly reports with recommendations | 📋 Planned |

### Key Capabilities

- **Original Content Generation**: Extracts patterns, doesn't copy
- **Multi-Platform Support**: Instagram, Threads, LinkedIn, X (Twitter)
- **Smart Scheduling**: Optimal posting times based on analytics
- **A/B Testing**: Experiment manager for content optimization
- **Automated Analytics**: AI-powered insights and recommendations

---

## 🏗️ Architecture

### Tech Stack

**Backend**
- Python 3.9+
- FastAPI (REST API)
- SQLAlchemy (ORM)
- SQLite → PostgreSQL (production)
- Pydantic (Data validation)

**Frontend** (Coming Soon)
- Next.js / React
- TailwindCSS
- TypeScript

**AI/ML**
- OpenAI GPT-4
- Anthropic Claude
- Google Gemini
- Ollama (local models)

**Infrastructure**
- Docker & Docker Compose
- AWS S3 (Storage)
- Redis (Caching & Queue)
- Celery (Async tasks)

### Project Structure

```
blackcat-ai/
├── backend/              # FastAPI backend
│   ├── main.py           # Application entry point
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── routers/          # API endpoints
│   │   ├── ideas.py      # Idea Vault endpoints
│   │   ├── series.py     # Series management
│   │   ├── posts.py      # Post CRUD operations
│   │   ├── analytics.py  # Analytics tracking
│   │   ├── experiments.py # A/B testing
│   │   └── assets.py     # Templates & Audio
│   ├── services/         # Business logic
│   └── requirements.txt  # Python dependencies
├── frontend/             # Next.js frontend (Coming Soon)
├── database/             # Migrations & seeds
├── templates/            # Post templates
├── assets/
│   ├── generated/        # Generated content
│   └── templates/        # Template files
├── scripts/              # Utility scripts
├── research/             # Scrapers & research tools
├── analytics/            # Analytics processing
├── docs/                 # Documentation
└── docker/               # Docker configuration
```

---

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/blackcat-ai.git
   cd blackcat-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   export DATABASE_URL=sqlite:///./blackcat.db
   export OPENAI_API_KEY=your_api_key_here
   export SECRET_KEY=your_secret_key_here
   ```

5. **Initialize database**
   ```bash
   python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
   ```

6. **Run development server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Production Deployment (Docker)

```bash
# Build Docker image
docker build -t blackcat-ai:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/blackcat \
  -e OPENAI_API_KEY=your_key \
  blackcat-ai:latest
```

---

## 💻 Usage

### Creating Your First Idea

```bash
curl -X POST "http://localhost:8000/ideas/" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Black Cat Files",
    "text": "Humans pretend they are resting. They are just changing apps.",
    "tags": ["observation", "technology", "behavior"]
  }'
```

### Creating a Content Series

```bash
curl -X POST "http://localhost:8000/series/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Black Cat Files",
    "description": "Daily observations about modern life",
    "prefix": "FILE",
    "number_format": "{prefix} #{number:03d}"
  }'
```

### Scheduling a Post

```bash
curl -X POST "http://localhost:8000/posts/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your post content here",
    "series_id": 1,
    "scheduled_at": "2024-01-15T10:00:00",
    "platforms": ["instagram", "threads"],
    "status": "scheduled"
  }'
```

### Tracking Analytics

```bash
curl -X POST "http://localhost:8000/analytics/" \
  -H "Content-Type: application/json" \
  -d '{
    "post_id": 1,
    "views": 1500,
    "likes": 230,
    "comments": 45,
    "shares": 67,
    "saves": 89
  }'
```

### Running Experiments

```bash
curl -X POST "http://localhost:8000/experiments/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cat GIF vs Dog GIF",
    "variant_a_post_id": 1,
    "variant_b_post_id": 2,
    "metric": "engagement_rate",
    "status": "running"
  }'
```

---

## 📚 API Documentation

Once the server is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/ideas/` | Create new idea |
| GET | `/ideas/` | List all ideas |
| GET | `/ideas/{idea_id}` | Get specific idea |
| PUT | `/ideas/{idea_id}` | Update idea |
| DELETE | `/ideas/{idea_id}` | Delete idea |
| POST | `/series/` | Create content series |
| GET | `/series/` | List all series |
| POST | `/posts/` | Create new post |
| GET | `/posts/` | List posts |
| POST | `/analytics/` | Record analytics |
| GET | `/analytics/post/{post_id}` | Get post analytics |
| POST | `/experiments/` | Create A/B test |
| GET | `/experiments/` | List experiments |
| POST | `/assets/templates/` | Upload template |
| POST | `/assets/audio/` | Add audio recommendation |

---

## 🗄️ Database Schema

### Tables Overview

```sql
-- Users table for authentication
users (
  id, email, username, hashed_password, 
  created_at, updated_at, is_active
)

-- Idea storage
ideas (
  id, category, text, source_url, source_type,
  tags, metadata, created_at, user_id
)

-- Content series with auto-numbering
series (
  id, name, description, prefix, 
  current_number, number_format, created_at
)

-- Posts with scheduling
posts (
  id, content, series_id, idea_id, status,
  scheduled_at, published_at, platforms,
  caption, hashtags, media_urls, created_at
)

-- Analytics tracking
analytics (
  id, post_id, views, likes, comments,
  shares, saves, watch_time, followers_gained,
  recorded_at
)

-- A/B testing experiments
experiments (
  id, name, variant_a_post_id, variant_b_post_id,
  metric, winner_id, status, started_at, ended_at
)

-- Templates for content generation
templates (
  id, name, type, config, thumbnail_url,
  is_active, created_at
)

-- Audio recommendations
audio (
  id, title, artist, mood, genre,
  duration, url, is_trending, created_at
)
```

---

## 📊 Version History

### v0.1.0 (Current) - 2024-01-15
**Initial Release**
- ✅ Backend infrastructure setup
- ✅ Database models (12 tables)
- ✅ REST API with 6 routers
- ✅ Idea Vault CRUD operations
- ✅ Series Manager with auto-numbering
- ✅ Post management & scheduling
- ✅ Analytics tracking
- ✅ Experiment Manager
- ✅ Asset management (Templates & Audio)
- ✅ Pydantic schemas for validation
- ✅ Comprehensive documentation

### v0.2.0 (Planned)
- 🔄 AI content generation integration
- 🔄 Pattern Analyzer module
- 🔄 Caption Generator with AI
- 🔄 Multi-platform adapters
- 🔄 Content approval workflow
- 🔄 Vector database for semantic search

### v0.3.0 (Planned)
- 📋 Frontend dashboard (Next.js)
- 📋 Reddit & X scrapers
- 📋 Trend detection system
- 📋 Automated research pipeline
- 📋 Brand voice training

### v1.0.0 (Target)
- 📋 Full AI-powered content creation
- 📋 Multi-language support
- 📋 Advanced analytics with AI insights
- 📋 Mobile app
- 📋 Team collaboration features

---

## 🛣️ Roadmap

### Q1 2024
- [x] Backend foundation
- [ ] AI integration (OpenAI, Claude)
- [ ] Pattern Analyzer
- [ ] Basic frontend

### Q2 2024
- [ ] Social media scrapers (Reddit, X)
- [ ] Content approval workflow
- [ ] Advanced scheduling
- [ ] Analytics dashboard

### Q3 2024
- [ ] A/B testing automation
- [ ] Brand voice training
- [ ] Multi-platform publishing
- [ ] Mobile responsiveness

### Q4 2024
- [ ] Team collaboration
- [ ] API for third-party integrations
- [ ] Performance optimization
- [ ] Production deployment

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation
- Use meaningful commit messages

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

- **Documentation**: https://blackcat-ai.readthedocs.io
- **Issues**: https://github.com/yourusername/blackcat-ai/issues
- **Discussions**: https://github.com/yourusername/blackcat-ai/discussions

---

## 🙏 Acknowledgments

- Inspired by content creators who spend too much time on manual tasks
- Built with FastAPI, SQLAlchemy, and Pydantic
- Powered by modern AI models

---

**Made with ❤️ for content creators everywhere**

*"Humans pretend they're resting. They're just changing apps."* - Black Cat Files #001
