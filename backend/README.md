# BlackCat AI Backend

FastAPI backend for the BlackCat AI CMS platform.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn main:app --reload
```

4. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Ideas
- `POST /ideas/` - Create a new idea
- `GET /ideas/` - Get all ideas
- `GET /ideas/{idea_id}` - Get a specific idea
- `PUT /ideas/{idea_id}` - Update an idea
- `DELETE /ideas/{idea_id}` - Delete an idea

### Posts
- `POST /posts/` - Create a new post
- `GET /posts/` - Get all posts
- `GET /posts/{post_id}` - Get a specific post
- `PUT /posts/{post_id}` - Update a post
- `DELETE /posts/{post_id}` - Delete a post

### Series
- `POST /series/` - Create a new series
- `GET /series/` - Get all series
- `GET /series/{series_id}` - Get a specific series
- `PUT /series/{series_id}` - Update a series
- `DELETE /series/{series_id}` - Delete a series

### Analytics
- `POST /analytics/` - Create analytics for a post
- `GET /analytics/post/{post_id}` - Get analytics for a post
- `PUT /analytics/post/{post_id}` - Update analytics
- `GET /analytics/summary` - Get overall analytics summary

### Experiments
- `POST /experiments/` - Create a new A/B test
- `GET /experiments/` - Get all experiments
- `GET /experiments/{experiment_id}` - Get a specific experiment
- `PUT /experiments/{experiment_id}/result` - Set experiment winner
- `DELETE /experiments/{experiment_id}` - Delete an experiment

### Assets
- `POST /assets/templates/` - Create a template
- `GET /assets/templates/` - Get all templates
- `GET /assets/templates/{template_id}` - Get a specific template
- `DELETE /assets/templates/{template_id}` - Delete a template
- `POST /assets/audio/` - Add an audio track
- `GET /assets/audio/` - Get all audio tracks
- `GET /assets/audio/trending/` - Get trending audio
- `DELETE /assets/audio/{audio_id}` - Delete an audio track

## Database

The application uses SQLite by default (blackcat.db). To switch to PostgreSQL, update the DATABASE_URL in database.py.

## Environment Variables

Create a `.env` file in the backend directory:

```
DATABASE_URL=sqlite:///./blackcat.db
OPENAI_API_KEY=your_api_key
```
