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

### TL;DR - Get Running in 5 Minutes

```bash
# 1. Clone and setup
git clone <your-repo-url>
cd analisis-al-instante-api
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install fastapi "uvicorn[standard]" pydantic python-multipart python-dotenv httpx pandas numpy openpyxl xlrd openai aiofiles

# 3. Setup environment
cp .env.example .env
# Edit .env and add your OpenAI API key: OPENAI_API_KEY=sk-...

# 4. Run the server
python main.py

# 5. Visit http://localhost:8000/docs to explore the API
```

### Prerequisites

- Python 3.8 or higher (Python 3.13+ recommended)
- pip (Python package installer)
- OpenAI API key (get from https://platform.openai.com/api-keys)

### Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd analisis-al-instante-api
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

**Note**: If you encounter issues with pandas installation on Python 3.13, install dependencies individually:

```bash
pip install fastapi "uvicorn[standard]" pydantic python-multipart python-dotenv httpx pandas numpy openpyxl xlrd openai aiofiles
```

4. Set up environment variables:

Copy the example environment file and add your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Important**: Get your OpenAI API key from https://platform.openai.com/api-keys

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
- `POST /upload` - Upload data files (CSV, Excel, JSON)
- `POST /analyze/{file_id}` - AI-powered analysis of uploaded file
- `POST /chart-data` - Generate chart data for visualization
- `GET /files/{file_id}` - Get information about uploaded file

### Example Usage

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Upload a File

```bash
curl -X POST "http://localhost:8000/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_data_file.csv"
```

#### Get AI Analysis

```bash
curl -X POST "http://localhost:8000/analyze/{file_id}" \
     -H "accept: application/json"
```

#### Generate Chart Data

```bash
curl -X POST "http://localhost:8000/chart-data" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "file_id": "your_file_id",
       "chart_type": "scatter",
       "parameters": {
         "x_axis": "age",
         "y_axis": "salary",
         "color_by": "department"
       }
     }'
```

## Development

### Project Structure

```
analisis-al-instante-api/
├── main.py              # Main FastAPI application with endpoints
├── models.py            # Pydantic models for request/response validation
├── services/            # Business logic and service layer
│   ├── __init__.py
│   ├── ai_analysis.py   # OpenAI integration for data analysis
│   ├── chart_data.py    # Chart data generation service
│   └── file_processing.py # File upload and processing service
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your environment variables (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### Architecture Overview

The API follows a clean architecture pattern:

1. **`main.py`**: FastAPI application with endpoint definitions and environment setup
2. **`models.py`**: Pydantic models for data validation and serialization
3. **`services/`**: Business logic separated into service classes:
   - `file_processing.py`: Handles file upload, validation, and processing
   - `ai_analysis.py`: Manages OpenAI GPT-4 integration for data analysis
   - `chart_data.py`: Generates formatted data for various chart types

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

The `.env` file contains all necessary configuration. Key variables include:

```env
# OpenAI API Configuration (REQUIRED)
OPENAI_API_KEY=your_openai_api_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# File Upload Configuration
MAX_FILE_SIZE_MB=50
ALLOWED_FILE_EXTENSIONS=.csv,.xlsx,.xls,.json

# Logging Configuration
LOG_LEVEL=INFO

# CORS Configuration
ALLOWED_ORIGINS=*
```

**Important**: The `OPENAI_API_KEY` is required for the AI analysis features to work.

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
