import logging
from typing import Any, Dict

import numpy as np
import pandas as pd

from models import ChartParameters, ChartType
from .file_processing import file_storage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChartDataService:
    """Service for generating chart-specific data"""

    @staticmethod
    def get_chart_data(
        file_id: str, chart_type: ChartType, parameters: ChartParameters
    ) -> Dict[str, Any]:
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
            data.columns = [x_col, "count"]
            y_col = "count"

        return {
            "data": data.to_dict("records"),
            "metadata": {
                "x_column": x_col,
                "y_column": y_col,
                "aggregation": agg_func,
                "total_points": len(data),
            },
        }

    @staticmethod
    def _generate_scatter_data(
        df: pd.DataFrame, params: ChartParameters
    ) -> Dict[str, Any]:
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
            "data": data.to_dict("records"),
            "metadata": {
                "x_column": x_col,
                "y_column": y_col,
                "color_column": color_col,
                "total_points": len(data),
            },
        }

    @staticmethod
    def _generate_histogram_data(
        df: pd.DataFrame, params: ChartParameters
    ) -> Dict[str, Any]:
        """Generate data for histograms"""
        x_col = params.x_axis
        bins = params.bins or 20

        if not x_col:
            raise ValueError("x_axis is required for histograms")

        data = df[x_col].dropna()
        hist, bin_edges = np.histogram(data, bins=bins)

        # Create bin labels
        bin_labels = [f"{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}" for i in range(len(hist))]

        chart_data = [
            {"bin": label, "count": int(count)} for label, count in zip(bin_labels, hist)
        ]

        return {
            "data": chart_data,
            "metadata": {
                "column": x_col,
                "bins": bins,
                "total_values": len(data),
                "min_value": float(data.min()),
                "max_value": float(data.max()),
            },
        }

    @staticmethod
    def _generate_pie_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for pie charts"""
        x_col = params.x_axis

        if not x_col:
            raise ValueError("x_axis is required for pie charts")

        data = df[x_col].value_counts()
        chart_data = [
            {"label": str(label), "value": int(value)} for label, value in data.items()
        ]

        return {
            "data": chart_data,
            "metadata": {
                "column": x_col,
                "total_categories": len(chart_data),
                "total_values": int(data.sum()),
            },
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
            "data": data.to_dict("records"),
            "metadata": {
                "x_column": x_col,
                "y_column": y_col,
                "total_points": len(data),
            },
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
            chart_data = [
                {"group": str(group), "values": values}
                for group, values in groups.items()
            ]
        else:
            # Single box plot
            values = df[y_col].dropna().tolist()
            chart_data = [{"group": y_col, "values": values}]

        return {
            "data": chart_data,
            "metadata": {
                "y_column": y_col,
                "group_column": group_col,
                "total_groups": len(chart_data),
            },
        }

