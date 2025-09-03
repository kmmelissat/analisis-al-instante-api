from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from enum import Enum

class ChartType(str, Enum):
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"
    BOX = "box"
    HEATMAP = "heatmap"

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    columns: List[str]
    data_types: Dict[str, str]
    shape: tuple[int, int]
    summary_stats: Dict[str, Any]
    message: str

class ChartParameters(BaseModel):
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    color_by: Optional[str] = None
    size_by: Optional[str] = None
    aggregation: Optional[str] = "sum"  # sum, mean, count, etc.
    bins: Optional[int] = None  # for histograms
    additional_params: Optional[Dict[str, Any]] = {}

class ChartSuggestion(BaseModel):
    title: str
    chart_type: ChartType
    parameters: ChartParameters
    insight: str
    priority: Optional[int] = Field(default=1, description="Priority ranking (1-5)")

class AIAnalysisResponse(BaseModel):
    file_id: str
    suggestions: List[ChartSuggestion]
    data_overview: Dict[str, Any]
    analysis_timestamp: str

class ChartDataRequest(BaseModel):
    file_id: str
    chart_type: ChartType
    parameters: ChartParameters

class ChartDataResponse(BaseModel):
    chart_type: ChartType
    data: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    title: str

class ErrorResponse(BaseModel):
    error: str
    detail: str
    code: Optional[str] = None

class DataSummary(BaseModel):
    total_rows: int
    total_columns: int
    numeric_columns: List[str]
    categorical_columns: List[str]
    datetime_columns: List[str]
    missing_values: Dict[str, int]
    memory_usage: str
