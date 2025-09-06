import json
import logging
import os
from typing import Any, Dict, List

import pandas as pd
from openai import AsyncOpenAI

from models import ChartParameters, ChartSuggestion, ChartType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# In-memory cache for analysis results
analysis_cache: Dict[str, Any] = {}


class AIAnalysisService:
    """Service for AI-powered data analysis"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def analyze_data(
        self, file_id: str, df: pd.DataFrame, metadata: Dict[str, Any]
    ) -> List[ChartSuggestion]:
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
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert data analyst. Analyze the provided dataset and suggest the most insightful visualizations.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=2000,
            )

            # Parse AI response
            suggestions = self._parse_ai_response(
                response.choices[0].message.content
            )

            # Cache results
            analysis_cache[cache_key] = suggestions

            logger.info(
                f"Generated {len(suggestions)} chart suggestions for {file_id}"
            )
            return suggestions

        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            # Return empty list when AI fails
            return []

    def _prepare_data_summary(
        self, df: pd.DataFrame, metadata: Dict[str, Any]
    ) -> str:
        """Prepare a concise data summary for AI analysis"""
        summary_parts = [
            f"Dataset: {metadata.get('filename', 'Unknown')}",
            f"Shape: {df.shape[0]} rows, {df.shape[1]} columns",
            f"Columns: {', '.join(df.columns.tolist())}",
        ]

        # Add data types
        if metadata.get("numeric_columns"):
            summary_parts.append(
                f"Numeric columns: {', '.join(metadata['numeric_columns'])}"
            )
        if metadata.get("categorical_columns"):
            summary_parts.append(
                f"Categorical columns: {', '.join(metadata['categorical_columns'])}"
            )
        if metadata.get("datetime_columns"):
            summary_parts.append(
                f"DateTime columns: {', '.join(metadata['datetime_columns'])}"
            )

        # Add statistical summary
        if metadata.get("summary_stats"):
            summary_parts.append("Statistical Summary:")
            for col, stats in list(metadata["summary_stats"].items())[:3]:
                summary_parts.append(
                    f"  {col}: mean={stats.get('mean', 'N/A'):.2f}, std={stats.get('std', 'N/A'):.2f}"
                )

        # Add sample data
        if metadata.get("sample_data"):
            summary_parts.append("Sample data (first 3 rows):")
            for i, row in enumerate(metadata["sample_data"][:3]):
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
            start_idx = response_text.find("[")
            end_idx = response_text.rfind("]") + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")

            json_str = response_text[start_idx:end_idx]
            suggestions_data = json.loads(json_str)

            suggestions = []
            for item in suggestions_data:
                try:
                    chart_params = ChartParameters(**item.get("parameters", {}))
                    suggestion = ChartSuggestion(
                        title=item["title"],
                        chart_type=ChartType(item["chart_type"]),
                        parameters=chart_params,
                        insight=item["insight"],
                        priority=item.get("priority", 3),
                    )
                    suggestions.append(suggestion)
                except Exception as e:
                    logger.warning(f"Skipping invalid suggestion: {e}")
                    continue

            return suggestions

        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return []


    async def generate_chart_insight(
        self, 
        file_id: str, 
        chart_type: ChartType, 
        parameters: ChartParameters, 
        chart_data: Dict[str, Any],
        df: pd.DataFrame
    ) -> Dict[str, str]:
        """Generate AI insights for a specific chart"""
        try:
            # Prepare chart context
            chart_context = self._prepare_chart_context(
                chart_type, parameters, chart_data, df
            )
            
            # Create AI prompt for chart interpretation
            prompt = self._create_chart_insight_prompt(chart_context)
            
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a data analyst expert. Analyze the provided chart and data to generate meaningful insights."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse response
            ai_response = response.choices[0].message.content
            
            return {
                "insight": self._extract_insight(ai_response),
                "interpretation": self._extract_interpretation(ai_response)
            }
            
        except Exception as e:
            logger.error(f"Error generating chart insight: {e}")
            return {
                "insight": None,
                "interpretation": None
            }

    def _prepare_chart_context(self, chart_type, parameters, chart_data, df):
        """Prepare context about the chart for AI analysis"""
        context_parts = [
            f"Chart Type: {chart_type.value}",
            f"Data Points: {len(chart_data['data'])}",
        ]
        
        if parameters.x_axis:
            context_parts.append(f"X-axis: {parameters.x_axis}")
        if parameters.y_axis:
            context_parts.append(f"Y-axis: {parameters.y_axis}")
        if parameters.aggregation:
            context_parts.append(f"Aggregation: {parameters.aggregation}")
        
        # Add sample data points
        sample_data = chart_data['data'][:5]  # First 5 data points
        context_parts.append(f"Sample Data: {sample_data}")
        
        # Add statistical info from metadata
        if 'total_points' in chart_data['metadata']:
            context_parts.append(f"Total Points: {chart_data['metadata']['total_points']}")
        
        return "\n".join(context_parts)

    def _create_chart_insight_prompt(self, chart_context):
        """Create AI prompt for chart insight generation"""
        return f"""
Analyze this data visualization and provide insights:

{chart_context}

Please provide:
1. INSIGHT: A brief, actionable insight about what this chart reveals (1-2 sentences)
2. INTERPRETATION: A detailed explanation of the patterns, trends, or relationships shown (2-3 sentences)

Focus on:
- Key patterns or trends visible in the data
- Notable outliers or anomalies
- Business implications or actionable insights
- Relationships between variables

Format your response as:
INSIGHT: [your insight here]
INTERPRETATION: [your interpretation here]
"""

    def _extract_insight(self, ai_response):
        """Extract insight from AI response"""
        try:
            lines = ai_response.split('\n')
            for line in lines:
                if line.startswith('INSIGHT:'):
                    return line.replace('INSIGHT:', '').strip()
            return None
        except:
            return None

    def _extract_interpretation(self, ai_response):
        """Extract interpretation from AI response"""
        try:
            lines = ai_response.split('\n')
            for line in lines:
                if line.startswith('INTERPRETATION:'):
                    return line.replace('INTERPRETATION:', '').strip()
            return None
        except:
            return None


