import pandas as pd
import numpy as np
import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
import io
import logging
from openai import AsyncOpenAI
import os
from models import ChartSuggestion, ChartType, ChartParameters, DataSummary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for demo purposes - use Redis/Database in production
file_storage: Dict[str, pd.DataFrame] = {}
analysis_cache: Dict[str, Any] = {}

class FileProcessingService:
    """Service for handling file uploads and processing"""
    
    ALLOWED_EXTENSIONS = {'.csv', '.xlsx', '.xls', '.json'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    @staticmethod
    def validate_file(filename: str, file_size: int) -> tuple[bool, str]:
        """Validate file extension and size"""
        if not filename:
            return False, "Filename is required"
        
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in FileProcessingService.ALLOWED_EXTENSIONS:
            return False, f"File type {file_ext} not supported. Allowed: {', '.join(FileProcessingService.ALLOWED_EXTENSIONS)}"
        
        if file_size > FileProcessingService.MAX_FILE_SIZE:
            return False, f"File size exceeds maximum allowed size of {FileProcessingService.MAX_FILE_SIZE // (1024*1024)}MB"
        
        return True, "Valid file"
    
    @staticmethod
    async def process_file(file_content: bytes, filename: str) -> tuple[str, pd.DataFrame, Dict[str, Any]]:
        """Process uploaded file and return DataFrame with metadata"""
        try:
            file_ext = os.path.splitext(filename)[1].lower()
            
            # Read file based on extension
            if file_ext == '.csv':
                df = pd.read_csv(io.BytesIO(file_content))
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(io.BytesIO(file_content))
            elif file_ext == '.json':
                df = pd.read_json(io.BytesIO(file_content))
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
            
            # Generate unique file ID
            file_id = str(uuid.uuid4())
            
            # Store DataFrame
            file_storage[file_id] = df
            
            # Generate metadata
            metadata = FileProcessingService._generate_metadata(df, filename)
            
            logger.info(f"Successfully processed file {filename} with ID {file_id}")
            return file_id, df, metadata
            
        except Exception as e:
            logger.error(f"Error processing file {filename}: {str(e)}")
            raise ValueError(f"Error processing file: {str(e)}")
    
    @staticmethod
    def _generate_metadata(df: pd.DataFrame, filename: str) -> Dict[str, Any]:
        """Generate comprehensive metadata for the DataFrame"""
        try:
            # Basic info
            metadata = {
                "filename": filename,
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "data_types": df.dtypes.astype(str).to_dict(),
            }
            
            # Categorize columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
            
            metadata.update({
                "numeric_columns": numeric_cols,
                "categorical_columns": categorical_cols,
                "datetime_columns": datetime_cols,
                "missing_values": df.isnull().sum().to_dict(),
                "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
            })
            
            # Statistical summary for numeric columns
            if numeric_cols:
                metadata["summary_stats"] = df[numeric_cols].describe().to_dict()
            
            # Sample data (first 5 rows)
            metadata["sample_data"] = df.head().to_dict('records')
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error generating metadata: {str(e)}")
            return {"error": f"Error generating metadata: {str(e)}"}

class AIAnalysisService:
    """Service for AI-powered data analysis"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def analyze_data(self, file_id: str, df: pd.DataFrame, metadata: Dict[str, Any]) -> List[ChartSuggestion]:
        """Analyze data and generate chart suggestions using AI"""
        try:
            # Check cache first
            cache_key = f"analysis_{file_id}"
            if cache_key in analysis_cache:
                logger.info(f"Returning cached analysis for {file_id}")
                return analysis_cache[cache_key]
            
            # Prepare data summary for AI
            data_summary = self._prepare_data_summary(df, metadata)
            
            # Generate AI prompt
            prompt = self._create_analysis_prompt(data_summary)
            
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert data analyst. Analyze the provided dataset and suggest the most insightful visualizations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse AI response
            suggestions = self._parse_ai_response(response.choices[0].message.content)
            
            # Cache results
            analysis_cache[cache_key] = suggestions
            
            logger.info(f"Generated {len(suggestions)} chart suggestions for {file_id}")
            return suggestions
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            # Return fallback suggestions
            return self._generate_fallback_suggestions(df, metadata)
    
    def _prepare_data_summary(self, df: pd.DataFrame, metadata: Dict[str, Any]) -> str:
        """Prepare a concise data summary for AI analysis"""
        summary_parts = [
            f"Dataset: {metadata.get('filename', 'Unknown')}",
            f"Shape: {df.shape[0]} rows, {df.shape[1]} columns",
            f"Columns: {', '.join(df.columns.tolist())}",
        ]
        
        # Add data types
        if metadata.get('numeric_columns'):
            summary_parts.append(f"Numeric columns: {', '.join(metadata['numeric_columns'])}")
        if metadata.get('categorical_columns'):
            summary_parts.append(f"Categorical columns: {', '.join(metadata['categorical_columns'])}")
        if metadata.get('datetime_columns'):
            summary_parts.append(f"DateTime columns: {', '.join(metadata['datetime_columns'])}")
        
        # Add statistical summary
        if metadata.get('summary_stats'):
            summary_parts.append("Statistical Summary:")
            for col, stats in list(metadata['summary_stats'].items())[:3]:  # Limit to first 3 columns
                summary_parts.append(f"  {col}: mean={stats.get('mean', 'N/A'):.2f}, std={stats.get('std', 'N/A'):.2f}")
        
        # Add sample data
        if metadata.get('sample_data'):
            summary_parts.append("Sample data (first 3 rows):")
            for i, row in enumerate(metadata['sample_data'][:3]):
                summary_parts.append(f"  Row {i+1}: {str(row)[:100]}...")
        
        return "\n".join(summary_parts)
    
    def _create_analysis_prompt(self, data_summary: str) -> str:
        """Create a structured prompt for AI analysis"""
        return f"""
Analyze this dataset and suggest 3-5 specific visualizations that would reveal the most interesting patterns and insights:

{data_summary}

Please respond with a JSON array where each object represents a chart suggestion with these exact keys:
- "title": A descriptive title for the chart
- "chart_type": One of: "bar", "line", "pie", "scatter", "histogram", "box", "heatmap"
- "parameters": An object with chart parameters like {{"x_axis": "column_name", "y_axis": "column_name", "aggregation": "sum"}}
- "insight": A brief explanation of what this visualization would reveal
- "priority": A number from 1-5 indicating importance (5 being most important)

Focus on:
1. Identifying relationships between variables
2. Highlighting distributions and outliers
3. Showing trends over time (if applicable)
4. Comparing categories or groups
5. Revealing correlations

Ensure the suggested columns exist in the dataset and the chart types are appropriate for the data types.
"""
    
    def _parse_ai_response(self, response_text: str) -> List[ChartSuggestion]:
        """Parse AI response and convert to ChartSuggestion objects"""
        try:
            # Extract JSON from response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")
            
            json_str = response_text[start_idx:end_idx]
            suggestions_data = json.loads(json_str)
            
            suggestions = []
            for item in suggestions_data:
                try:
                    chart_params = ChartParameters(**item.get('parameters', {}))
                    suggestion = ChartSuggestion(
                        title=item['title'],
                        chart_type=ChartType(item['chart_type']),
                        parameters=chart_params,
                        insight=item['insight'],
                        priority=item.get('priority', 3)
                    )
                    suggestions.append(suggestion)
                except Exception as e:
                    logger.warning(f"Skipping invalid suggestion: {e}")
                    continue
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return []
    
    def _generate_fallback_suggestions(self, df: pd.DataFrame, metadata: Dict[str, Any]) -> List[ChartSuggestion]:
        """Generate basic fallback suggestions when AI fails"""
        suggestions = []
        numeric_cols = metadata.get('numeric_columns', [])
        categorical_cols = metadata.get('categorical_columns', [])
        
        # Basic histogram for first numeric column
        if numeric_cols:
            suggestions.append(ChartSuggestion(
                title=f"Distribution of {numeric_cols[0]}",
                chart_type=ChartType.HISTOGRAM,
                parameters=ChartParameters(x_axis=numeric_cols[0]),
                insight=f"Shows the distribution pattern of {numeric_cols[0]} values",
                priority=3
            ))
        
        # Bar chart for first categorical column
        if categorical_cols:
            suggestions.append(ChartSuggestion(
                title=f"Count by {categorical_cols[0]}",
                chart_type=ChartType.BAR,
                parameters=ChartParameters(x_axis=categorical_cols[0], aggregation="count"),
                insight=f"Shows the frequency of different {categorical_cols[0]} categories",
                priority=3
            ))
        
        # Scatter plot if we have at least 2 numeric columns
        if len(numeric_cols) >= 2:
            suggestions.append(ChartSuggestion(
                title=f"{numeric_cols[0]} vs {numeric_cols[1]}",
                chart_type=ChartType.SCATTER,
                parameters=ChartParameters(x_axis=numeric_cols[0], y_axis=numeric_cols[1]),
                insight=f"Reveals the relationship between {numeric_cols[0]} and {numeric_cols[1]}",
                priority=4
            ))
        
        return suggestions

class ChartDataService:
    """Service for generating chart-specific data"""
    
    @staticmethod
    def get_chart_data(file_id: str, chart_type: ChartType, parameters: ChartParameters) -> Dict[str, Any]:
        """Generate formatted data for specific chart type"""
        if file_id not in file_storage:
            raise ValueError(f"File {file_id} not found")
        
        df = file_storage[file_id]
        
        try:
            if chart_type == ChartType.BAR:
                return ChartDataService._generate_bar_data(df, parameters)
            elif chart_type == ChartType.LINE:
                return ChartDataService._generate_line_data(df, parameters)
            elif chart_type == ChartType.PIE:
                return ChartDataService._generate_pie_data(df, parameters)
            elif chart_type == ChartType.SCATTER:
                return ChartDataService._generate_scatter_data(df, parameters)
            elif chart_type == ChartType.HISTOGRAM:
                return ChartDataService._generate_histogram_data(df, parameters)
            elif chart_type == ChartType.BOX:
                return ChartDataService._generate_box_data(df, parameters)
            else:
                raise ValueError(f"Chart type {chart_type} not implemented")
                
        except Exception as e:
            logger.error(f"Error generating chart data: {e}")
            raise ValueError(f"Error generating chart data: {str(e)}")
    
    @staticmethod
    def _generate_bar_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for bar charts"""
        x_col = params.x_axis
        y_col = params.y_axis
        agg_func = params.aggregation or "count"
        
        if not x_col:
            raise ValueError("x_axis is required for bar charts")
        
        if y_col:
            # Aggregate y_col by x_col
            if agg_func == "count":
                data = df.groupby(x_col)[y_col].count().reset_index()
            elif agg_func == "sum":
                data = df.groupby(x_col)[y_col].sum().reset_index()
            elif agg_func == "mean":
                data = df.groupby(x_col)[y_col].mean().reset_index()
            else:
                data = df.groupby(x_col)[y_col].agg(agg_func).reset_index()
        else:
            # Count occurrences of x_col
            data = df[x_col].value_counts().reset_index()
            data.columns = [x_col, 'count']
            y_col = 'count'
        
        return {
            "data": data.to_dict('records'),
            "metadata": {
                "x_column": x_col,
                "y_column": y_col,
                "aggregation": agg_func,
                "total_points": len(data)
            }
        }
    
    @staticmethod
    def _generate_scatter_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for scatter plots"""
        x_col = params.x_axis
        y_col = params.y_axis
        color_col = params.color_by
        
        if not x_col or not y_col:
            raise ValueError("Both x_axis and y_axis are required for scatter plots")
        
        # Select relevant columns
        cols = [x_col, y_col]
        if color_col and color_col in df.columns:
            cols.append(color_col)
        
        data = df[cols].dropna()
        
        return {
            "data": data.to_dict('records'),
            "metadata": {
                "x_column": x_col,
                "y_column": y_col,
                "color_column": color_col,
                "total_points": len(data)
            }
        }
    
    @staticmethod
    def _generate_histogram_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for histograms"""
        x_col = params.x_axis
        bins = params.bins or 20
        
        if not x_col:
            raise ValueError("x_axis is required for histograms")
        
        data = df[x_col].dropna()
        hist, bin_edges = np.histogram(data, bins=bins)
        
        # Create bin labels
        bin_labels = [f"{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}" for i in range(len(hist))]
        
        chart_data = [{"bin": label, "count": int(count)} for label, count in zip(bin_labels, hist)]
        
        return {
            "data": chart_data,
            "metadata": {
                "column": x_col,
                "bins": bins,
                "total_values": len(data),
                "min_value": float(data.min()),
                "max_value": float(data.max())
            }
        }
    
    @staticmethod
    def _generate_pie_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for pie charts"""
        x_col = params.x_axis
        
        if not x_col:
            raise ValueError("x_axis is required for pie charts")
        
        data = df[x_col].value_counts()
        chart_data = [{"label": str(label), "value": int(value)} for label, value in data.items()]
        
        return {
            "data": chart_data,
            "metadata": {
                "column": x_col,
                "total_categories": len(chart_data),
                "total_values": int(data.sum())
            }
        }
    
    @staticmethod
    def _generate_line_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for line charts"""
        x_col = params.x_axis
        y_col = params.y_axis
        
        if not x_col or not y_col:
            raise ValueError("Both x_axis and y_axis are required for line charts")
        
        data = df[[x_col, y_col]].dropna().sort_values(x_col)
        
        return {
            "data": data.to_dict('records'),
            "metadata": {
                "x_column": x_col,
                "y_column": y_col,
                "total_points": len(data)
            }
        }
    
    @staticmethod
    def _generate_box_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for box plots"""
        y_col = params.y_axis
        group_col = params.x_axis
        
        if not y_col:
            raise ValueError("y_axis is required for box plots")
        
        if group_col:
            # Grouped box plot
            groups = df.groupby(group_col)[y_col].apply(list).to_dict()
            chart_data = [{"group": str(group), "values": values} for group, values in groups.items()]
        else:
            # Single box plot
            values = df[y_col].dropna().tolist()
            chart_data = [{"group": y_col, "values": values}]
        
        return {
            "data": chart_data,
            "metadata": {
                "y_column": y_col,
                "group_column": group_col,
                "total_groups": len(chart_data)
            }
        }
