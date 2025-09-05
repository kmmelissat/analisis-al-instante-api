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
            elif chart_type == ChartType.AREA:
                return ChartDataService._generate_area_data(df, parameters)
            elif chart_type == ChartType.DONUT:
                return ChartDataService._generate_donut_data(df, parameters)
            elif chart_type == ChartType.VIOLIN:
                return ChartDataService._generate_violin_data(df, parameters)
            elif chart_type == ChartType.HEATMAP:
                return ChartDataService._generate_heatmap_data(df, parameters)
            elif chart_type == ChartType.BUBBLE:
                return ChartDataService._generate_bubble_data(df, parameters)
            elif chart_type == ChartType.RADAR:
                return ChartDataService._generate_radar_data(df, parameters)
            elif chart_type == ChartType.TREEMAP:
                return ChartDataService._generate_treemap_data(df, parameters)
            elif chart_type == ChartType.SUNBURST:
                return ChartDataService._generate_sunburst_data(df, parameters)
            elif chart_type == ChartType.DENSITY:
                return ChartDataService._generate_density_data(df, parameters)
            elif chart_type == ChartType.RIDGELINE:
                return ChartDataService._generate_ridgeline_data(df, parameters)
            elif chart_type == ChartType.CANDLESTICK:
                return ChartDataService._generate_candlestick_data(df, parameters)
            elif chart_type == ChartType.WATERFALL:
                return ChartDataService._generate_waterfall_data(df, parameters)
            elif chart_type == ChartType.GANTT:
                return ChartDataService._generate_gantt_data(df, parameters)
            elif chart_type == ChartType.SANKEY:
                return ChartDataService._generate_sankey_data(df, parameters)
            elif chart_type == ChartType.CHORD:
                return ChartDataService._generate_chord_data(df, parameters)
            elif chart_type == ChartType.FUNNEL:
                return ChartDataService._generate_funnel_data(df, parameters)
            elif chart_type == ChartType.STACKED_BAR:
                return ChartDataService._generate_stacked_bar_data(df, parameters)
            elif chart_type == ChartType.GROUPED_BAR:
                return ChartDataService._generate_grouped_bar_data(df, parameters)
            elif chart_type == ChartType.MULTI_LINE:
                return ChartDataService._generate_multi_line_data(df, parameters)
            elif chart_type == ChartType.STACKED_AREA:
                return ChartDataService._generate_stacked_area_data(df, parameters)
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

    # ===== ADVANCED CHART TYPES =====

    @staticmethod
    def _generate_area_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for area charts"""
        x_col = params.x_axis
        y_col = params.y_axis
        stack_by = params.stack_by

        if not x_col or not y_col:
            raise ValueError("Both x_axis and y_axis are required for area charts")

        if stack_by:
            # Stacked area chart
            pivot_data = df.pivot_table(
                values=y_col, index=x_col, columns=stack_by, 
                aggfunc=params.aggregation or "sum", fill_value=0
            )
            
            chart_data = []
            for idx in pivot_data.index:
                row_data = {"x": str(idx)}
                cumulative = 0
                for col in pivot_data.columns:
                    value = pivot_data.loc[idx, col]
                    cumulative += value
                    row_data[f"{col}_value"] = float(value)
                    row_data[f"{col}_cumulative"] = float(cumulative)
                chart_data.append(row_data)
        else:
            # Simple area chart
            data = df[[x_col, y_col]].dropna().sort_values(x_col)
            chart_data = data.to_dict("records")

        return {
            "data": chart_data,
            "metadata": {
                "x_column": x_col,
                "y_column": y_col,
                "stack_column": stack_by,
                "total_points": len(chart_data),
                "chart_subtype": "stacked" if stack_by else "simple"
            },
        }

    @staticmethod
    def _generate_donut_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for donut charts (pie chart with hole in center)"""
        # Same as pie chart but with different metadata
        pie_data = ChartDataService._generate_pie_data(df, params)
        pie_data["metadata"]["chart_subtype"] = "donut"
        pie_data["metadata"]["inner_radius"] = 0.4  # 40% inner radius
        return pie_data

    @staticmethod
    def _generate_violin_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for violin plots (combination of box plot and density)"""
        y_col = params.y_axis
        group_col = params.x_axis

        if not y_col:
            raise ValueError("y_axis is required for violin plots")

        if group_col:
            # Grouped violin plot
            groups = df.groupby(group_col)[y_col].apply(list).to_dict()
            chart_data = []
            
            for group, values in groups.items():
                values = [v for v in values if pd.notna(v)]
                if values:
                    # Calculate density estimation points
                    values_array = np.array(values)
                    min_val, max_val = values_array.min(), values_array.max()
                    x_points = np.linspace(min_val, max_val, 50)
                    
                    # Simple kernel density estimation
                    bandwidth = params.bandwidth or (max_val - min_val) / 20
                    density = []
                    for x in x_points:
                        kde_sum = sum(np.exp(-0.5 * ((x - v) / bandwidth) ** 2) for v in values)
                        density.append(kde_sum / (len(values) * bandwidth * np.sqrt(2 * np.pi)))
                    
                    chart_data.append({
                        "group": str(group),
                        "values": values,
                        "density_x": x_points.tolist(),
                        "density_y": density,
                        "quartiles": {
                            "q1": float(np.percentile(values, 25)),
                            "median": float(np.percentile(values, 50)),
                            "q3": float(np.percentile(values, 75)),
                            "min": float(min_val),
                            "max": float(max_val)
                        }
                    })
        else:
            # Single violin plot
            values = df[y_col].dropna().tolist()
            values_array = np.array(values)
            min_val, max_val = values_array.min(), values_array.max()
            x_points = np.linspace(min_val, max_val, 50)
            
            bandwidth = params.bandwidth or (max_val - min_val) / 20
            density = []
            for x in x_points:
                kde_sum = sum(np.exp(-0.5 * ((x - v) / bandwidth) ** 2) for v in values)
                density.append(kde_sum / (len(values) * bandwidth * np.sqrt(2 * np.pi)))
            
            chart_data = [{
                "group": y_col,
                "values": values,
                "density_x": x_points.tolist(),
                "density_y": density,
                "quartiles": {
                    "q1": float(np.percentile(values, 25)),
                    "median": float(np.percentile(values, 50)),
                    "q3": float(np.percentile(values, 75)),
                    "min": float(min_val),
                    "max": float(max_val)
                }
            }]

        return {
            "data": chart_data,
            "metadata": {
                "y_column": y_col,
                "group_column": group_col,
                "total_groups": len(chart_data),
                "bandwidth": bandwidth
            },
        }

    @staticmethod
    def _generate_heatmap_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for heatmaps"""
        x_col = params.x_axis
        y_col = params.y_axis
        value_col = params.z_axis or params.color_by

        if not x_col or not y_col:
            raise ValueError("Both x_axis and y_axis are required for heatmaps")

        if value_col:
            # Pivot table with values
            heatmap_data = df.pivot_table(
                values=value_col, index=y_col, columns=x_col,
                aggfunc=params.aggregation or "mean", fill_value=0
            )
        else:
            # Count-based heatmap
            heatmap_data = df.pivot_table(
                index=y_col, columns=x_col, aggfunc='size', fill_value=0
            )

        # Convert to list of dictionaries
        chart_data = []
        for y_idx, y_val in enumerate(heatmap_data.index):
            for x_idx, x_val in enumerate(heatmap_data.columns):
                chart_data.append({
                    "x": str(x_val),
                    "y": str(y_val),
                    "value": float(heatmap_data.iloc[y_idx, x_idx]),
                    "x_index": x_idx,
                    "y_index": y_idx
                })

        return {
            "data": chart_data,
            "metadata": {
                "x_column": x_col,
                "y_column": y_col,
                "value_column": value_col,
                "x_categories": [str(x) for x in heatmap_data.columns],
                "y_categories": [str(y) for y in heatmap_data.index],
                "min_value": float(heatmap_data.min().min()),
                "max_value": float(heatmap_data.max().max())
            },
        }

    @staticmethod
    def _generate_bubble_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for bubble charts (scatter plot with size dimension)"""
        x_col = params.x_axis
        y_col = params.y_axis
        size_col = params.size_by
        color_col = params.color_by

        if not x_col or not y_col or not size_col:
            raise ValueError("x_axis, y_axis, and size_by are required for bubble charts")

        # Select relevant columns
        cols = [x_col, y_col, size_col]
        if color_col and color_col in df.columns:
            cols.append(color_col)

        data = df[cols].dropna()

        # Normalize bubble sizes for better visualization
        size_values = data[size_col]
        min_size, max_size = size_values.min(), size_values.max()
        normalized_sizes = 10 + 40 * (size_values - min_size) / (max_size - min_size) if max_size > min_size else [25] * len(size_values)

        chart_data = []
        for idx, row in data.iterrows():
            bubble = {
                "x": float(row[x_col]),
                "y": float(row[y_col]),
                "size": float(normalized_sizes.iloc[idx] if hasattr(normalized_sizes, 'iloc') else normalized_sizes[idx]),
                "original_size": float(row[size_col])
            }
            if color_col:
                bubble["color"] = str(row[color_col])
            chart_data.append(bubble)

        return {
            "data": chart_data,
            "metadata": {
                "x_column": x_col,
                "y_column": y_col,
                "size_column": size_col,
                "color_column": color_col,
                "total_points": len(chart_data),
                "size_range": {"min": float(min_size), "max": float(max_size)}
            },
        }

    @staticmethod
    def _generate_radar_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for radar/spider charts"""
        group_col = params.group_by or params.color_by
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if params.x_axis and params.x_axis in numeric_cols:
            numeric_cols = [col for col in numeric_cols if col != params.x_axis]
        
        if len(numeric_cols) < 3:
            raise ValueError("Radar charts require at least 3 numeric columns")

        # Limit to reasonable number of dimensions
        if params.limit:
            numeric_cols = numeric_cols[:params.limit]
        else:
            numeric_cols = numeric_cols[:8]  # Max 8 dimensions for readability

        if group_col and group_col in df.columns:
            # Multiple series radar chart
            chart_data = []
            for group_value in df[group_col].unique():
                if pd.isna(group_value):
                    continue
                    
                group_data = df[df[group_col] == group_value]
                series_data = {
                    "group": str(group_value),
                    "values": []
                }
                
                for col in numeric_cols:
                    if params.aggregation == "mean":
                        value = group_data[col].mean()
                    elif params.aggregation == "sum":
                        value = group_data[col].sum()
                    elif params.aggregation == "median":
                        value = group_data[col].median()
                    else:
                        value = group_data[col].mean()
                    
                    series_data["values"].append({
                        "axis": col,
                        "value": float(value) if pd.notna(value) else 0
                    })
                
                chart_data.append(series_data)
        else:
            # Single series radar chart
            series_data = {
                "group": "Data",
                "values": []
            }
            
            for col in numeric_cols:
                if params.aggregation == "mean":
                    value = df[col].mean()
                elif params.aggregation == "sum":
                    value = df[col].sum()
                elif params.aggregation == "median":
                    value = df[col].median()
                else:
                    value = df[col].mean()
                
                series_data["values"].append({
                    "axis": col,
                    "value": float(value) if pd.notna(value) else 0
                })
            
            chart_data = [series_data]

        return {
            "data": chart_data,
            "metadata": {
                "axes": numeric_cols,
                "group_column": group_col,
                "total_series": len(chart_data),
                "aggregation": params.aggregation or "mean"
            },
        }

    @staticmethod
    def _generate_treemap_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for treemap charts"""
        category_col = params.x_axis
        value_col = params.y_axis
        subcategory_col = params.color_by

        if not category_col or not value_col:
            raise ValueError("Both x_axis (category) and y_axis (value) are required for treemaps")

        if subcategory_col and subcategory_col in df.columns:
            # Hierarchical treemap
            grouped = df.groupby([category_col, subcategory_col])[value_col].agg(params.aggregation or "sum").reset_index()
            
            chart_data = []
            for category in grouped[category_col].unique():
                if pd.isna(category):
                    continue
                    
                category_data = grouped[grouped[category_col] == category]
                total_value = category_data[value_col].sum()
                
                children = []
                for _, row in category_data.iterrows():
                    children.append({
                        "name": str(row[subcategory_col]),
                        "value": float(row[value_col]),
                        "percentage": float(row[value_col] / total_value * 100) if total_value > 0 else 0
                    })
                
                chart_data.append({
                    "name": str(category),
                    "value": float(total_value),
                    "children": children
                })
        else:
            # Simple treemap
            grouped = df.groupby(category_col)[value_col].agg(params.aggregation or "sum").reset_index()
            total_value = grouped[value_col].sum()
            
            chart_data = []
            for _, row in grouped.iterrows():
                chart_data.append({
                    "name": str(row[category_col]),
                    "value": float(row[value_col]),
                    "percentage": float(row[value_col] / total_value * 100) if total_value > 0 else 0
                })

        return {
            "data": chart_data,
            "metadata": {
                "category_column": category_col,
                "value_column": value_col,
                "subcategory_column": subcategory_col,
                "total_categories": len(chart_data),
                "hierarchical": bool(subcategory_col)
            },
        }

    @staticmethod
    def _generate_sunburst_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for sunburst charts (hierarchical pie chart)"""
        # Similar to treemap but with circular hierarchy
        return ChartDataService._generate_treemap_data(df, params)

    @staticmethod
    def _generate_density_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for density plots"""
        x_col = params.x_axis
        group_col = params.color_by

        if not x_col:
            raise ValueError("x_axis is required for density plots")

        bandwidth = params.bandwidth or 0.1
        
        if group_col and group_col in df.columns:
            # Multiple density curves
            chart_data = []
            for group_value in df[group_col].unique():
                if pd.isna(group_value):
                    continue
                    
                group_data = df[df[group_col] == group_value][x_col].dropna()
                if len(group_data) == 0:
                    continue
                    
                min_val, max_val = group_data.min(), group_data.max()
                x_points = np.linspace(min_val, max_val, 100)
                
                density = []
                for x in x_points:
                    kde_sum = sum(np.exp(-0.5 * ((x - v) / bandwidth) ** 2) for v in group_data)
                    density.append(kde_sum / (len(group_data) * bandwidth * np.sqrt(2 * np.pi)))
                
                chart_data.append({
                    "group": str(group_value),
                    "x": x_points.tolist(),
                    "density": density
                })
        else:
            # Single density curve
            data = df[x_col].dropna()
            min_val, max_val = data.min(), data.max()
            x_points = np.linspace(min_val, max_val, 100)
            
            density = []
            for x in x_points:
                kde_sum = sum(np.exp(-0.5 * ((x - v) / bandwidth) ** 2) for v in data)
                density.append(kde_sum / (len(data) * bandwidth * np.sqrt(2 * np.pi)))
            
            chart_data = [{
                "group": x_col,
                "x": x_points.tolist(),
                "density": density
            }]

        return {
            "data": chart_data,
            "metadata": {
                "x_column": x_col,
                "group_column": group_col,
                "bandwidth": bandwidth,
                "total_curves": len(chart_data)
            },
        }

    # ===== PLACEHOLDER METHODS FOR COMPLEX CHARTS =====
    # These would require more sophisticated implementations

    @staticmethod
    def _generate_ridgeline_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for ridgeline plots (multiple density plots stacked)"""
        # Simplified implementation - would need more sophisticated layout
        density_data = ChartDataService._generate_density_data(df, params)
        density_data["metadata"]["chart_subtype"] = "ridgeline"
        return density_data

    @staticmethod
    def _generate_candlestick_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for candlestick charts (OHLC financial data)"""
        date_col = params.x_axis
        
        # Assume we have OHLC columns or calculate them from a single price column
        if not date_col:
            raise ValueError("x_axis (date) is required for candlestick charts")
        
        # Placeholder implementation
        return {
            "data": [{"error": "Candlestick charts require OHLC data structure"}],
            "metadata": {"chart_type": "candlestick", "status": "not_implemented"}
        }

    @staticmethod
    def _generate_waterfall_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for waterfall charts"""
        category_col = params.x_axis
        value_col = params.y_axis
        
        if not category_col or not value_col:
            raise ValueError("Both x_axis and y_axis are required for waterfall charts")
        
        # Simple waterfall implementation
        data = df[[category_col, value_col]].dropna()
        cumulative = 0
        chart_data = []
        
        for _, row in data.iterrows():
            value = float(row[value_col])
            chart_data.append({
                "category": str(row[category_col]),
                "value": value,
                "cumulative": cumulative + value,
                "start": cumulative,
                "end": cumulative + value
            })
            cumulative += value
        
        return {
            "data": chart_data,
            "metadata": {
                "category_column": category_col,
                "value_column": value_col,
                "total_change": cumulative,
                "total_steps": len(chart_data)
            }
        }

    @staticmethod
    def _generate_gantt_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for Gantt charts"""
        # Placeholder - would need start_date, end_date, task columns
        return {
            "data": [{"error": "Gantt charts require start_date, end_date, and task columns"}],
            "metadata": {"chart_type": "gantt", "status": "not_implemented"}
        }

    @staticmethod
    def _generate_sankey_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for Sankey diagrams"""
        # Placeholder - would need source, target, value columns
        return {
            "data": [{"error": "Sankey diagrams require source, target, and value columns"}],
            "metadata": {"chart_type": "sankey", "status": "not_implemented"}
        }

    @staticmethod
    def _generate_chord_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for chord diagrams"""
        # Placeholder - would need matrix data
        return {
            "data": [{"error": "Chord diagrams require matrix data structure"}],
            "metadata": {"chart_type": "chord", "status": "not_implemented"}
        }

    @staticmethod
    def _generate_funnel_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for funnel charts"""
        stage_col = params.x_axis
        value_col = params.y_axis
        
        if not stage_col or not value_col:
            raise ValueError("Both x_axis (stage) and y_axis (value) are required for funnel charts")
        
        # Aggregate data by stage
        data = df.groupby(stage_col)[value_col].agg(params.aggregation or "sum").reset_index()
        data = data.sort_values(value_col, ascending=False)
        
        total_value = data[value_col].sum()
        chart_data = []
        
        for idx, row in data.iterrows():
            value = float(row[value_col])
            chart_data.append({
                "stage": str(row[stage_col]),
                "value": value,
                "percentage": (value / total_value * 100) if total_value > 0 else 0,
                "order": idx
            })
        
        return {
            "data": chart_data,
            "metadata": {
                "stage_column": stage_col,
                "value_column": value_col,
                "total_stages": len(chart_data),
                "total_value": float(total_value)
            }
        }

    # ===== MULTI-SERIES CHART TYPES =====

    @staticmethod
    def _generate_stacked_bar_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for stacked bar charts"""
        x_col = params.x_axis
        y_col = params.y_axis
        stack_col = params.stack_by or params.color_by
        
        if not x_col or not y_col or not stack_col:
            raise ValueError("x_axis, y_axis, and stack_by are required for stacked bar charts")
        
        # Create pivot table
        pivot_data = df.pivot_table(
            values=y_col, index=x_col, columns=stack_col,
            aggfunc=params.aggregation or "sum", fill_value=0
        )
        
        chart_data = []
        for category in pivot_data.index:
            row_data = {"category": str(category)}
            cumulative = 0
            
            for stack_value in pivot_data.columns:
                value = float(pivot_data.loc[category, stack_value])
                row_data[f"{stack_value}_value"] = value
                row_data[f"{stack_value}_start"] = cumulative
                row_data[f"{stack_value}_end"] = cumulative + value
                cumulative += value
            
            row_data["total"] = cumulative
            chart_data.append(row_data)
        
        return {
            "data": chart_data,
            "metadata": {
                "x_column": x_col,
                "y_column": y_col,
                "stack_column": stack_col,
                "stack_categories": list(pivot_data.columns),
                "total_categories": len(chart_data)
            }
        }

    @staticmethod
    def _generate_grouped_bar_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for grouped bar charts"""
        # Similar to stacked but without cumulative positioning
        stacked_data = ChartDataService._generate_stacked_bar_data(df, params)
        stacked_data["metadata"]["chart_subtype"] = "grouped"
        return stacked_data

    @staticmethod
    def _generate_multi_line_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for multi-line charts"""
        x_col = params.x_axis
        y_col = params.y_axis
        group_col = params.group_by or params.color_by
        
        if not x_col or not y_col or not group_col:
            raise ValueError("x_axis, y_axis, and group_by are required for multi-line charts")
        
        chart_data = []
        for group_value in df[group_col].unique():
            if pd.isna(group_value):
                continue
                
            group_data = df[df[group_col] == group_value][[x_col, y_col]].dropna().sort_values(x_col)
            
            line_data = {
                "series": str(group_value),
                "points": group_data.to_dict("records")
            }
            chart_data.append(line_data)
        
        return {
            "data": chart_data,
            "metadata": {
                "x_column": x_col,
                "y_column": y_col,
                "group_column": group_col,
                "total_series": len(chart_data)
            }
        }

    @staticmethod
    def _generate_stacked_area_data(df: pd.DataFrame, params: ChartParameters) -> Dict[str, Any]:
        """Generate data for stacked area charts"""
        # Similar to area chart but with stacking
        area_data = ChartDataService._generate_area_data(df, params)
        area_data["metadata"]["chart_subtype"] = "stacked"
        return area_data

