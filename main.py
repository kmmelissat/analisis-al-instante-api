from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom modules
from models import (
    FileUploadResponse, AIAnalysisResponse, ChartDataRequest, 
    ChartDataResponse, ErrorResponse, ChartSuggestion, ChartType, ChartParameters
)
from services.file_processing import FileProcessingService, file_storage
from services.ai_analysis import AIAnalysisService
from services.chart_data import ChartDataService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI(
    title="Análisis al Instante API",
    description="API for instant data analysis and visualization with AI-powered insights",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ai_service = AIAnalysisService()

# Legacy models for backward compatibility
class HealthResponse(BaseModel):
    status: str
    message: str

class AnalysisRequest(BaseModel):
    data: str
    analysis_type: Optional[str] = "general"

class AnalysisResponse(BaseModel):
    id: str
    result: str
    analysis_type: str
    status: str

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint returning API information"""
    return {
        "message": "Welcome to Análisis al Instante API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="API is running successfully"
    )

# File upload endpoint
@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and process a data file (CSV, Excel, JSON)
    Returns file metadata and basic statistics
    """
    try:
        # Validate file
        file_size = 0
        if hasattr(file, 'size'):
            file_size = file.size
        
        is_valid, message = FileProcessingService.validate_file(file.filename, file_size)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Read file content
        content = await file.read()
        
        # Process file
        file_id, df, metadata = await FileProcessingService.process_file(content, file.filename)
        
        # Create response
        response = FileUploadResponse(
            file_id=file_id,
            filename=metadata["filename"],
            columns=metadata["columns"],
            data_types=metadata["data_types"],
            shape=metadata["shape"],
            summary_stats=metadata.get("summary_stats", {}),
            message=f"File processed successfully. {df.shape[0]} rows, {df.shape[1]} columns."
        )
        
        logger.info(f"File upload successful: {file.filename} -> {file_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# AI Analysis endpoint
@app.post("/analyze/{file_id}", response_model=AIAnalysisResponse)
async def analyze_file_with_ai(file_id: str):
    """
    Analyze uploaded file using AI to generate visualization suggestions
    """
    try:
        # Check if file exists
        if file_id not in file_storage:
            raise HTTPException(status_code=404, detail="File not found")
        
        df = file_storage[file_id]
        
        # Generate metadata for AI analysis
        metadata = FileProcessingService._generate_metadata(df, f"file_{file_id}")
        
        # Get AI suggestions
        suggestions = await ai_service.analyze_data(file_id, df, metadata)
        
        # Create response
        response = AIAnalysisResponse(
            file_id=file_id,
            suggestions=suggestions,
            data_overview={
                "total_rows": df.shape[0],
                "total_columns": df.shape[1],
                "numeric_columns": metadata.get("numeric_columns", []),
                "categorical_columns": metadata.get("categorical_columns", []),
                "missing_values_count": sum(metadata.get("missing_values", {}).values())
            },
            analysis_timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"AI analysis completed for file {file_id}: {len(suggestions)} suggestions")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing file: {str(e)}")

# Chart data endpoint
@app.post("/chart-data", response_model=ChartDataResponse)
async def get_chart_data(request: ChartDataRequest):
    """
    Get formatted data for a specific chart based on parameters
    """
    try:
        # Generate chart data
        chart_data = ChartDataService.get_chart_data(
            request.file_id, 
            request.chart_type, 
            request.parameters
        )
        
        # Create title based on chart type and parameters
        title = f"{request.chart_type.value.title()} Chart"
        if request.parameters.x_axis:
            title += f" - {request.parameters.x_axis}"
        if request.parameters.y_axis:
            title += f" vs {request.parameters.y_axis}"
        
        response = ChartDataResponse(
            chart_type=request.chart_type,
            data=chart_data["data"],
            metadata=chart_data["metadata"],
            title=title
        )
        
        logger.info(f"Chart data generated: {request.chart_type} for file {request.file_id}")
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Chart data error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating chart data: {str(e)}")

# Get file info endpoint
@app.get("/files/{file_id}")
async def get_file_info(file_id: str):
    """Get information about an uploaded file"""
    try:
        if file_id not in file_storage:
            raise HTTPException(status_code=404, detail="File not found")
        
        df = file_storage[file_id]
        metadata = FileProcessingService._generate_metadata(df, f"file_{file_id}")
        
        return {
            "file_id": file_id,
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "summary": metadata
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get file info error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving file info: {str(e)}")

# Legacy endpoints for backward compatibility
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_data(request: AnalysisRequest):
    """Legacy analyze endpoint - kept for backward compatibility"""
    return AnalysisResponse(
        id="legacy_analysis",
        result=f"Legacy analysis completed for: {request.data[:50]}...",
        analysis_type=request.analysis_type,
        status="completed"
    )

@app.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Legacy get analysis endpoint - kept for backward compatibility"""
    return {
        "id": analysis_id,
        "status": "completed",
        "result": "Legacy analysis result",
        "created_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
