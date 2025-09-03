# Análisis al Instante API

A FastAPI-based REST API for instant data analysis and visualization with AI-powered insights.

## Features

- **File Upload & Processing**: Support for CSV, Excel, and JSON files with pandas processing
- **AI-Powered Analysis**: Uses OpenAI GPT-4 to analyze data and suggest optimal visualizations
- **Chart Data Generation**: Provides formatted data for various chart types (bar, line, pie, scatter, histogram, box plots)
- **Comprehensive Data Validation**: File type, size, and content validation
- **Structured API Responses**: Well-defined Pydantic models for all endpoints
- **Error Handling**: Comprehensive error handling with detailed logging
- **Service Layer Architecture**: Clean separation of concerns with dedicated service classes
- **CORS Support**: Configurable cross-origin resource sharing
- **Interactive Documentation**: Automatic API documentation with Swagger UI

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd analisis-al-instante-api
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

### Running the Application

1. Start the development server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Open your browser and navigate to:
   - API Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc
   - API Root: http://localhost:8000

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `POST /analyze` - Submit data for analysis
- `GET /analysis/{analysis_id}` - Retrieve analysis results

### Example Usage

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Submit Analysis

```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"data": "sample data to analyze", "analysis_type": "general"}'
```

#### Get Analysis Results

```bash
curl http://localhost:8000/analysis/analysis_001
```

## Development

### Project Structure

```
analisis-al-instante-api/
├── main.py              # Main FastAPI application with endpoints
├── models.py            # Pydantic models for request/response validation
├── services.py          # Business logic and service layer
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### Architecture Overview

The API follows a clean architecture pattern:

1. **`main.py`**: FastAPI application with endpoint definitions
2. **`models.py`**: Pydantic models for data validation and serialization
3. **`services.py`**: Business logic separated into service classes:
   - `FileProcessingService`: Handles file upload and processing
   - `AIAnalysisService`: Manages AI-powered data analysis
   - `ChartDataService`: Generates formatted data for visualizations

### Supported File Types

- **CSV**: Comma-separated values
- **Excel**: .xlsx and .xls files
- **JSON**: JavaScript Object Notation

### Supported Chart Types

- **Bar Charts**: Categorical data comparison
- **Line Charts**: Trends over time or continuous data
- **Pie Charts**: Part-to-whole relationships
- **Scatter Plots**: Correlation between two variables
- **Histograms**: Distribution of numerical data
- **Box Plots**: Statistical distribution summary

### Adding New Features

1. Define Pydantic models for request/response validation
2. Create new endpoints in `main.py`
3. Add proper error handling
4. Update documentation

### Testing

Install test dependencies and run tests:

```bash
pip install pytest pytest-asyncio
pytest
```

## Configuration

### Environment Variables

Create a `.env` file in the project root for environment-specific configuration:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Database (if needed)
DATABASE_URL=sqlite:///./test.db

# Security (if implementing authentication)
SECRET_KEY=your-secret-key-here
```

### CORS Configuration

Update the CORS middleware in `main.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Specify allowed methods
    allow_headers=["*"],
)
```

## Deployment

### Using Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t analisis-api .
docker run -p 8000:8000 analisis-api
```

### Production Deployment

For production deployment, consider:

1. Using a production ASGI server like Gunicorn with Uvicorn workers
2. Setting up proper logging
3. Implementing authentication and authorization
4. Adding rate limiting
5. Setting up monitoring and health checks
6. Using environment variables for configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
