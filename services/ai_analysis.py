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
                model="gpt-4-turbo-preview",
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
            # Return fallback suggestions
            return self._generate_fallback_suggestions(df, metadata)

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

    def _generate_fallback_suggestions(
        self, df: pd.DataFrame, metadata: Dict[str, Any]
    ) -> List[ChartSuggestion]:
        """Generate basic fallback suggestions when AI fails"""
        suggestions = []
        numeric_cols = metadata.get("numeric_columns", [])
        categorical_cols = metadata.get("categorical_columns", [])

        # Basic histogram for first numeric column
        if numeric_cols:
            suggestions.append(
                ChartSuggestion(
                    title=f"Distribution of {numeric_cols[0]}",
                    chart_type=ChartType.HISTOGRAM,
                    parameters=ChartParameters(x_axis=numeric_cols[0]),
                    insight=f"Shows the distribution pattern of {numeric_cols[0]} values",
                    priority=3,
                )
            )

        # Bar chart for first categorical column
        if categorical_cols:
            suggestions.append(
                ChartSuggestion(
                    title=f"Count by {categorical_cols[0]}",
                    chart_type=ChartType.BAR,
                    parameters=ChartParameters(
                        x_axis=categorical_cols[0], aggregation="count"
                    ),
                    insight=f"Shows the frequency of different {categorical_cols[0]} categories",
                    priority=3,
                )
            )

        # Scatter plot if we have at least 2 numeric columns
        if len(numeric_cols) >= 2:
            suggestions.append(
                ChartSuggestion(
                    title=f"{numeric_cols[0]} vs {numeric_cols[1]}",
                    chart_type=ChartType.SCATTER,
                    parameters=ChartParameters(
                        x_axis=numeric_cols[0], y_axis=numeric_cols[1]
                    ),
                    insight=f"Reveals the relationship between {numeric_cols[0]} and {numeric_cols[1]}",
                    priority=4,
                )
            )

        return suggestions

