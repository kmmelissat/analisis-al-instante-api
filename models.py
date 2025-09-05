from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from enum import Enum

class ChartType(str, Enum):
    # Basic Charts
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"
    BOX = "box"
    
    # Advanced Charts
    AREA = "area"
    DONUT = "donut"
    VIOLIN = "violin"
    HEATMAP = "heatmap"
    BUBBLE = "bubble"
    RADAR = "radar"
    TREEMAP = "treemap"
    SUNBURST = "sunburst"
    
    # Statistical Charts
    DENSITY = "density"
    RIDGELINE = "ridgeline"
    CANDLESTICK = "candlestick"
    WATERFALL = "waterfall"
    
    # Specialized Charts
    GANTT = "gantt"
    SANKEY = "sankey"
    CHORD = "chord"
    FUNNEL = "funnel"
    
    # Multi-series Charts
    STACKED_BAR = "stacked_bar"
    GROUPED_BAR = "grouped_bar"
    MULTI_LINE = "multi_line"
    STACKED_AREA = "stacked_area"

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    columns: List[str]
    data_types: Dict[str, str]
    shape: tuple[int, int]
    summary_stats: Dict[str, Any]
    message: str

class ChartParameters(BaseModel):
    # Basic axes
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    z_axis: Optional[str] = None  # for 3D charts
    
    # Visual encoding
    color_by: Optional[str] = None
    size_by: Optional[str] = None
    shape_by: Optional[str] = None
    opacity_by: Optional[str] = None
    
    # Aggregation and grouping
    aggregation: Optional[str] = "sum"  # sum, mean, count, median, min, max, std, var
    group_by: Optional[str] = None
    stack_by: Optional[str] = None
    
    # Chart-specific parameters
    bins: Optional[int] = None  # for histograms
    bandwidth: Optional[float] = None  # for density plots
    threshold: Optional[float] = None  # for various charts
    
    # Formatting and display
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "asc"  # asc, desc
    limit: Optional[int] = None  # limit number of categories/points
    
    # Time series specific
    time_unit: Optional[str] = None  # day, week, month, quarter, year
    rolling_window: Optional[int] = None
    
    # Advanced parameters
    normalize: Optional[bool] = False
    percentage: Optional[bool] = False
    cumulative: Optional[bool] = False
    
    # Custom parameters for specific chart types
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
