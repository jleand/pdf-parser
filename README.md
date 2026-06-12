# PDF Parser

A production-ready FastAPI service that extracts text from PDF files. Automatically handles both text-based PDFs (using pypdf) and scanned documents (using Tesseract OCR).

## Features

- **Dual extraction mode**: Text extraction for digital PDFs, OCR for scanned documents
- **Production-ready**: Proper error handling, logging, CORS, rate limiting
- **Memory-safe**: Concurrency limits and page caps for OCR operations
- **Docker-ready**: Optimized image with health checks
- **Configurable**: Environment variables for customization

## Tech Stack

- **FastAPI** - Modern async web framework
- **pypdf** - Fast text extraction from digital PDFs
- **Tesseract OCR** - Optical character recognition for scanned PDFs
- **pdf2image** - PDF to image conversion
- **Docker** - Containerized deployment

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Build image
docker build -t pdf-parser .

# Run container
docker run -p 8000:8000 pdf-parser

# Or with custom settings
docker run -p 8000:8000 \
  -e MAX_FILE_SIZE=52428800 \
  -e MAX_CONCURRENT=8 \
  -e LOG_LEVEL=DEBUG \
  pdf-parser
```

## API Endpoints

### Parse PDF

**POST** `/parse`

Extracts text from an uploaded PDF file.

**Request:**
```bash
curl -X POST http://localhost:8000/parse \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "status": "ok",
  "data": "Extracted text content...",
  "error": null
}
```

**Error Response:**
```json
{
  "status": "error",
  "data": null,
  "error": "Only PDF files are accepted"
}
```

### Health Check

**GET** `/health`

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "data": "healthy",
  "error": null
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_FILE_SIZE` | `20971520` (20MB) | Maximum upload file size in bytes |
| `MAX_CONCURRENT` | `4` | Maximum concurrent OCR operations |
| `CORS_ORIGINS` | `*` | Comma-separated list of allowed origins |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Deployment

### Docker Hub

The image is automatically built and pushed to Docker Hub on pushes to main:

```bash
docker pull leandjoao/pdf-parser:latest
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pdf-parser
spec:
  replicas: 2
  selector:
    matchLabels:
      app: pdf-parser
  template:
    metadata:
      labels:
        app: pdf-parser
    spec:
      containers:
      - name: pdf-parser
        image: leandjoao/pdf-parser:latest
        ports:
        - containerPort: 8000
        env:
        - name: MAX_FILE_SIZE
          value: "52428800"
        - name: MAX_CONCURRENT
          value: "8"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
```

## Performance Notes

- Text-based PDFs are processed instantly using pypdf
- OCR is CPU-intensive and limited to 50 pages max
- OCR DPI is set to 200 for balance between quality and speed
- Concurrent OCR operations are limited to prevent memory exhaustion
- For high-volume OCR workloads, consider scaling horizontally

## License

MIT
