# AI PDF to Slide Generator

A scalable Python backend service that automatically generates slides from PDF documents or structured JSON data using AI.

![architecture-pdf-ai-slides-tool](https://github.com/user-attachments/assets/fe465935-2a4c-4dfb-ab6d-28cf7415c30a)

## 🚀 Features

- **FastAPI** built with FastAPI for presentation generation
- **PDF Text Extraction** to analyze uploaded documents
- **AI-Powered Content Generation** using OpenAI to create slides from PDFs
- **Asynchronous Processing** with Celery for improved scalability
- **Multiple Slide Types** including title slides, content, bullet points, two-column, and image layouts
- **Task Tracking** to monitor the status of your presentation generation
- **Containerized** with Docker and Docker Compose for easy deployment

## 📋 Requirements

- Python 3.12+
- Redis (for Celery message broker)
- Docker and Docker Compose (for containerized deployment)
- OpenAI API key (for AI-powered content generation)

## 🛠️ Installation

### Using Docker (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ai-presentation-generator.git
   cd ai-presentation-generator
   ```

2. Create a `.env` file with your OpenAI API key:

   ```
   APP_NAME=Presentation Generator
   REDIS_URL=redis://redis:6379/0
   RESULT_BACKEND=redis://redis:6379/0
   STORAGE_PATH=/app/storage
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

The service will be available at http://localhost:8000.

### Manual Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ai-presentation-generator.git
   cd ai-presentation-generator
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up your environment variables (create a `.env` file):

   ```
   APP_NAME=Presentation Generator
   REDIS_URL=redis://localhost:6379/0
   RESULT_BACKEND=redis://localhost:6379/0
   STORAGE_PATH=./storage
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Make sure Redis is running locally or update the configuration in `app/config.py`.

5. Run the FastAPI application:

   ```bash
   uvicorn app.main:app --reload
   ```

6. In a separate terminal, start the Celery worker:
   ```bash
   celery -A celery_app worker --loglevel=info
   ```

## 📊 API Usage

### Generate a Presentation from Structured Data

```bash
curl -X POST http://localhost:8000/api/presentations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Quarterly Report",
    "author": "Your Team",
    "slides": [
      {
        "type": "title",
        "title": "Q2 Performance Review",
        "content": "Finance Department"
      },
      {
        "type": "bullet_points",
        "title": "Key Achievements",
        "bullet_points": [
          "Revenue increased by 15%",
          "New client acquisition up 22%",
          "Operational costs reduced by 8%"
        ]
      }
    ]
  }'
```

Response:

```json
{
  "task_id": "b8f5e56a-915b-4c44-a784-2f86c1f0e3e9",
  "status": "pending"
}
```

### Generate a Presentation from PDF

```bash
curl -X POST http://localhost:8000/api/presentations/from-pdf \
  -F "pdf_file=@/path/to/your/document.pdf" \
  -F "title=AI Generated Presentation" \
  -F "author=Your Name" \
  -F "num_slides=7"
```

Response:

```json
{
  "task_id": "c7e4f45b-826a-4b33-a991-4f75d2f7e4a8",
  "status": "pending"
}
```

### Check Presentation Status

```bash
curl http://localhost:8000/api/presentations/{task_id}
```

Response:

```json
{
  "task_id": "c7e4f45b-826a-4b33-a991-4f75d2f7e4a8",
  "status": "completed",
  "file_url": "/download/f6e8d971-3841-4b2a-9e39-3e5fc3c8340b.pptx",
  "message": "Presentation generated successfully"
}
```

### Download the Presentation

```bash
curl -O http://localhost:8000/api/download/{file_id}
```

## 🧩 Supported Slide Types

| Type            | Description                                     |
| --------------- | ----------------------------------------------- |
| `title`         | Title slide with subtitle                       |
| `content`       | Standard content slide with title and body text |
| `bullet_points` | Slide with title and bulleted points            |
| `two_column`    | Two-column layout for comparing content         |
| `image`         | Image slide with a title                        |

## 📂 Project Structure

```
presentation_generator/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration
│   ├── ppt_generator.py     # PowerPoint generation logic
│   └── pdf_processor.py     # PDF processing and OpenAI integration
├── celery_app/
│   ├── __init__.py
│   ├── tasks.py             # Celery tasks
│   └── celery_config.py     # Celery configuration
├── requirements.txt
└── docker-compose.yml
```

## 🔧 Configuration

Configuration is managed through environment variables and defaults:

| Variable         | Default                  | Description                              |
| ---------------- | ------------------------ | ---------------------------------------- |
| `APP_NAME`       | "Presentation Generator" | Application name                         |
| `REDIS_URL`      | "redis://redis:6379/0"   | Redis URL for Celery broker              |
| `RESULT_BACKEND` | "redis://redis:6379/0"   | Result backend for Celery                |
| `STORAGE_PATH`   | "/app/storage"           | Path for storing generated presentations |
| `OPENAI_API_KEY` | ""                       | Your OpenAI API key                      |

## How It Works

### PDF Processing Workflow

1. **Upload PDF**: User uploads a PDF file via the API
2. **Text Extraction**: System extracts text content using PyPDF2
3. **AI Analysis**: OpenAI processes the text and identifies key points
4. **Content Generation**: AI generates slide content based on the analysis
5. **Presentation Creation**: System creates PowerPoint slides using python-pptx
6. **Notification**: User can check task status and download the presentation

## 🛣️ Roadmap

- [ ] Add authentication for API endpoints
- [ ] Support for custom PowerPoint templates
- [ ] Chart generation from data in PDFs
- [ ] Image extraction and inclusion from PDFs
- [ ] Web interface for easier usage
- [ ] Cloud storage integration (S3, GCS)
- [ ] Support for more file formats (Word, HTML, Markdown)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Documentation

For more detailed documentation, see the [API Documentation](http://localhost:8000/docs) when the service is running.
