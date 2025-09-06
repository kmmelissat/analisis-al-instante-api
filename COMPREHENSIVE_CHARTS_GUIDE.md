# 📊 Comprehensive Charts Guide - Análisis al Instante API

**Complete reference for all 24+ chart types with detailed parameters, use cases, and implementation examples.**

---

## 🎯 Chart Categories Overview

### **Basic Charts** (6 types)

Essential charts for everyday data visualization

- Bar, Line, Pie, Scatter, Histogram, Box

### **Advanced Charts** (8 types)

Sophisticated visualizations for deeper insights

- Area, Donut, Violin, Heatmap, Bubble, Radar, Treemap, Sunburst

### **Statistical Charts** (4 types)

Specialized charts for statistical analysis

- Density, Ridgeline, Candlestick, Waterfall

### **Specialized Charts** (4 types)

Domain-specific visualizations

- Gantt, Sankey, Chord, Funnel

### **Multi-series Charts** (4 types)

Charts supporting multiple data series

- Stacked Bar, Grouped Bar, Multi-line, Stacked Area

---

## 📈 BASIC CHARTS

### 1. **Bar Charts** (`"bar"`)

**Purpose**: Compare categorical data, show rankings, display frequencies

**When to Use**:

- Comparing sales across regions
- Showing survey response counts
- Ranking products by performance
- Displaying demographic distributions

**Required Parameters**:

- `x_axis`: Categorical column (required)

**Optional Parameters**:

- `y_axis`: Numeric column (uses count if not provided)
- `aggregation`: "count", "sum", "mean", "median", "min", "max"
- `sort_by`: Column to sort by
- `sort_order`: "asc" or "desc"
- `limit`: Limit number of categories shown

**Example Request**:

```json
{
  "file_id": "sales-data-id",
  "chart_type": "bar",
  "parameters": {
    "x_axis": "region",
    "y_axis": "sales_amount",
    "aggregation": "sum",
    "sort_order": "desc",
    "limit": 10
  }
}
```

**Response Data Structure**:

```json
{
  "data": [
    { "region": "North", "sales_amount": 125000 },
    { "region": "South", "sales_amount": 98000 },
    { "region": "East", "sales_amount": 110000 }
  ],
  "metadata": {
    "x_column": "region",
    "y_column": "sales_amount",
    "aggregation": "sum",
    "total_points": 3
  }
}
```
---

### 2. **Line Charts** (`"line"`)

**Purpose**: Show trends over time, display continuous data progression

**When to Use**:

- Sales trends over months
- Stock price movements
- Website traffic patterns
- Temperature changes over time

**Required Parameters**:

- `x_axis`: Sequential/time column (required)
- `y_axis`: Numeric column (required)

**Optional Parameters**:

- `rolling_window`: Apply moving average
- `time_unit`: "day", "week", "month", "quarter", "year"
- `cumulative`: Show cumulative values

**Example Request**:

```json
{
  "file_id": "sales-data-id",
  "chart_type": "line",
  "parameters": {
    "x_axis": "date",
    "y_axis": "sales_amount",
    "rolling_window": 7,
    "time_unit": "day"
  }
}
```

**Use Cases by Data Type**:

- **Time Series**: Daily sales, monthly revenue, quarterly growth
- **Sequential Data**: Process steps, user journey stages
- **Continuous Variables**: Performance metrics over iterations

---

### 3. **Pie Charts** (`"pie"`)

**Purpose**: Show part-to-whole relationships, market share, category distribution

**When to Use**:

- Market share analysis
- Budget allocation
- Survey response distribution
- Demographic breakdowns

**Required Parameters**:

- `x_axis`: Categorical column (required)

**Optional Parameters**:

- `limit`: Limit number of slices (others grouped as "Other")
- `percentage`: Show as percentages instead of counts
- `sort_order`: "asc", "desc", or "none"

**Example Request**:

```json
{
  "file_id": "survey-data-id",
  "chart_type": "pie",
  "parameters": {
    "x_axis": "customer_type",
    "percentage": true,
    "limit": 5
  }
}
```

**Best Practices**:

- Limit to 5-7 categories for readability
- Use contrasting colors
- Consider donut chart for better label placement
- Avoid 3D effects that distort perception

---

### 4. **Scatter Plots** (`"scatter"`)

**Purpose**: Explore relationships between variables, identify correlations, detect outliers

**When to Use**:

- Salary vs experience analysis
- Sales vs marketing spend correlation
- Performance vs training hours
- Quality vs price relationships

**Required Parameters**:

- `x_axis`: Numeric column (required)
- `y_axis`: Numeric column (required)

**Optional Parameters**:

- `color_by`: Categorical column for color coding
- `size_by`: Numeric column for bubble sizing
- `opacity_by`: Column for transparency encoding
- `shape_by`: Categorical column for shape encoding

**Advanced Example**:

```json
{
  "file_id": "employee-data-id",
  "chart_type": "scatter",
  "parameters": {
    "x_axis": "years_experience",
    "y_axis": "salary",
    "color_by": "department",
    "size_by": "performance_score",
    "opacity_by": "training_hours"
  }
}
```

**Correlation Interpretation**:

- **Positive**: Points trend upward (more X → more Y)
- **Negative**: Points trend downward (more X → less Y)
- **No Correlation**: Random scatter pattern
- **Non-linear**: Curved or complex patterns

---

### 5. **Histograms** (`"histogram"`)

**Purpose**: Show distribution of continuous data, identify patterns, detect skewness

**When to Use**:

- Age distribution analysis
- Salary range visualization
- Performance score patterns
- Quality measurements distribution

**Required Parameters**:

- `x_axis`: Numeric column (required)

**Optional Parameters**:

- `bins`: Number of bins (default: 20)
- `normalize`: Show as probability density
- `cumulative`: Show cumulative distribution

**Example Request**:

```json
{
  "file_id": "employee-data-id",
  "chart_type": "histogram",
  "parameters": {
    "x_axis": "salary",
    "bins": 15,
    "normalize": true
  }
}
```

**Distribution Types**:

- **Normal**: Bell curve, symmetric
- **Skewed Right**: Long tail to the right
- **Skewed Left**: Long tail to the left
- **Bimodal**: Two peaks
- **Uniform**: Flat distribution

---

### 6. **Box Plots** (`"box"`)

**Purpose**: Statistical summary, outlier detection, group comparisons

**When to Use**:

- Salary distribution by department
- Performance scores across teams
- Quality metrics comparison
- Identifying outliers in data

**Required Parameters**:

- `y_axis`: Numeric column (required)

**Optional Parameters**:

- `x_axis`: Categorical column for grouping
- `show_outliers`: Include outlier points

**Example Request**:

```json
{
  "file_id": "employee-data-id",
  "chart_type": "box",
  "parameters": {
    "y_axis": "salary",
    "x_axis": "department",
    "show_outliers": true
  }
}
```

**Box Plot Components**:

- **Box**: Interquartile range (Q1 to Q3)
- **Line in Box**: Median (Q2)
- **Whiskers**: 1.5 × IQR from box edges
- **Points**: Outliers beyond whiskers

---

## 🚀 ADVANCED CHARTS

### 7. **Area Charts** (`"area"`)

**Purpose**: Show trends with magnitude emphasis, compare multiple series

**When to Use**:

- Revenue growth over time
- Market share evolution
- Cumulative metrics
- Stacked category comparisons

**Required Parameters**:

- `x_axis`: Sequential column (required)
- `y_axis`: Numeric column (required)

**Optional Parameters**:

- `stack_by`: Column for stacking multiple series
- `normalize`: Show as percentages (100% stacked)
- `cumulative`: Show cumulative values

**Stacked Area Example**:

```json
{
  "file_id": "sales-data-id",
  "chart_type": "area",
  "parameters": {
    "x_axis": "date",
    "y_axis": "sales_amount",
    "stack_by": "product_category",
    "normalize": true
  }
}
```

---

### 8. **Donut Charts** (`"donut"`)

**Purpose**: Pie chart with center space for additional information

**When to Use**:

- When you need space for totals/labels
- Modern, clean aesthetic
- Multiple concentric data series
- Dashboard KPIs

**Same parameters as pie chart, with additional metadata**:

- `inner_radius`: 0.4 (40% of outer radius)

---

### 9. **Violin Plots** (`"violin"`)

**Purpose**: Combine box plot statistics with distribution shape

**When to Use**:

- Detailed distribution analysis
- Comparing distribution shapes across groups
- When box plots aren't detailed enough
- Statistical research presentations

**Required Parameters**:

- `y_axis`: Numeric column (required)

**Optional Parameters**:

- `x_axis`: Categorical column for grouping
- `bandwidth`: Kernel density bandwidth

**Response includes**:

- Box plot statistics (quartiles, median)
- Density curve points
- Raw data values

---

### 10. **Heatmaps** (`"heatmap"`)

**Purpose**: Show relationships in 2D data, correlation matrices, pattern detection

**When to Use**:

- Correlation analysis
- Time-based patterns (hour vs day)
- Geographic data visualization
- Performance matrices

**Required Parameters**:

- `x_axis`: Categorical column (required)
- `y_axis`: Categorical column (required)

**Optional Parameters**:

- `z_axis` or `color_by`: Value column for color intensity
- `aggregation`: How to aggregate overlapping data

**Example Request**:

```json
{
  "file_id": "sales-data-id",
  "chart_type": "heatmap",
  "parameters": {
    "x_axis": "month",
    "y_axis": "region",
    "color_by": "sales_amount",
    "aggregation": "mean"
  }
}
```

---

### 11. **Bubble Charts** (`"bubble"`)

**Purpose**: 3-dimensional scatter plot with size encoding

**When to Use**:

- Market analysis (price vs quality vs market share)
- Portfolio analysis (risk vs return vs investment size)
- Performance metrics with impact sizing
- Multi-dimensional comparisons

**Required Parameters**:

- `x_axis`: Numeric column (required)
- `y_axis`: Numeric column (required)
- `size_by`: Numeric column for bubble size (required)

**Optional Parameters**:

- `color_by`: Categorical column for color coding

**Example Request**:

```json
{
  "file_id": "product-data-id",
  "chart_type": "bubble",
  "parameters": {
    "x_axis": "price",
    "y_axis": "quality_score",
    "size_by": "market_share",
    "color_by": "category"
  }
}
```

---

### 12. **Radar Charts** (`"radar"`)

**Purpose**: Multi-dimensional data comparison, profile analysis

**When to Use**:

- Employee skill assessments
- Product feature comparisons
- Performance dashboards
- Multi-criteria analysis

**Optional Parameters**:

- `group_by` or `color_by`: Compare multiple entities
- `limit`: Limit number of dimensions (max 8 recommended)
- `aggregation`: How to summarize numeric columns

**Automatically uses all numeric columns as dimensions**

**Example Request**:

```json
{
  "file_id": "employee-data-id",
  "chart_type": "radar",
  "parameters": {
    "group_by": "department",
    "aggregation": "mean",
    "limit": 6
  }
}
```

---

### 13. **Treemap Charts** (`"treemap"`)

**Purpose**: Hierarchical data visualization, space-efficient category comparison

**When to Use**:

- Budget allocation visualization
- File system analysis
- Market capitalization display
- Hierarchical organizational data

**Required Parameters**:

- `x_axis`: Category column (required)
- `y_axis`: Value column (required)

**Optional Parameters**:

- `color_by`: Subcategory for hierarchy

**Hierarchical Example**:

```json
{
  "file_id": "budget-data-id",
  "chart_type": "treemap",
  "parameters": {
    "x_axis": "department",
    "y_axis": "budget_amount",
    "color_by": "subcategory"
  }
}
```

---

### 14. **Sunburst Charts** (`"sunburst"`)

**Purpose**: Hierarchical data in circular format, drill-down visualization

**When to Use**:

- Organizational hierarchies
- File directory structures
- Multi-level categorization
- Nested data exploration

**Same parameters as treemap but with circular layout**

---

## 📊 STATISTICAL CHARTS

### 15. **Density Plots** (`"density"`)

**Purpose**: Smooth distribution curves, probability density estimation

**When to Use**:

- Comparing distribution shapes
- Smooth alternative to histograms
- Overlaying multiple distributions
- Statistical analysis presentations

**Required Parameters**:

- `x_axis`: Numeric column (required)

**Optional Parameters**:

- `color_by`: Group column for multiple curves
- `bandwidth`: Smoothing parameter

---

### 16. **Ridgeline Plots** (`"ridgeline"`)

**Purpose**: Multiple density plots stacked vertically

**When to Use**:

- Comparing distributions across many groups
- Time series of distributions
- Joy plots for aesthetic presentations
- Large categorical comparisons

---

### 17. **Waterfall Charts** (`"waterfall"`)

**Purpose**: Show cumulative effect of sequential changes

**When to Use**:

- Financial analysis (profit/loss breakdown)
- Budget variance analysis
- Process improvement tracking
- Step-by-step impact analysis

**Required Parameters**:

- `x_axis`: Category/step column (required)
- `y_axis`: Value column (required)

**Response includes**:

- Individual values
- Cumulative totals
- Start and end positions for each step

---

## 🎯 SPECIALIZED CHARTS

### 18. **Funnel Charts** (`"funnel"`)

**Purpose**: Show conversion rates through process stages

**When to Use**:

- Sales pipeline analysis
- Website conversion tracking
- Process efficiency analysis
- Customer journey mapping

**Required Parameters**:

- `x_axis`: Stage column (required)
- `y_axis`: Value column (required)

**Example Request**:

```json
{
  "file_id": "conversion-data-id",
  "chart_type": "funnel",
  "parameters": {
    "x_axis": "stage",
    "y_axis": "user_count",
    "aggregation": "sum"
  }
}
```

---

## 🔄 MULTI-SERIES CHARTS

### 19. **Stacked Bar Charts** (`"stacked_bar"`)

**Purpose**: Show part-to-whole relationships across categories

**Required Parameters**:

- `x_axis`: Category column (required)
- `y_axis`: Value column (required)
- `stack_by`: Stacking dimension (required)

**Example Request**:

```json
{
  "file_id": "sales-data-id",
  "chart_type": "stacked_bar",
  "parameters": {
    "x_axis": "region",
    "y_axis": "sales_amount",
    "stack_by": "product_category",
    "aggregation": "sum"
  }
}
```

---

### 20. **Grouped Bar Charts** (`"grouped_bar"`)

**Purpose**: Compare multiple series side-by-side

**Same parameters as stacked bar, but bars are grouped rather than stacked**

---

### 21. **Multi-line Charts** (`"multi_line"`)

**Purpose**: Compare trends across multiple series

**Required Parameters**:

- `x_axis`: Sequential column (required)
- `y_axis`: Value column (required)
- `group_by`: Series grouping column (required)

---

### 22. **Stacked Area Charts** (`"stacked_area"`)

**Purpose**: Show cumulative trends with category breakdown

**Same parameters as area chart with stacking enabled**

---

## 🛠️ Advanced Parameters Reference

### **Visual Encoding Parameters**

| Parameter    | Type   | Description               | Use Cases                                      |
| ------------ | ------ | ------------------------- | ---------------------------------------------- |
| `color_by`   | string | Column for color coding   | Group identification, categorical encoding     |
| `size_by`    | string | Column for size encoding  | Magnitude representation, importance weighting |
| `shape_by`   | string | Column for shape encoding | Additional categorical dimension               |
| `opacity_by` | string | Column for transparency   | Confidence levels, data quality indicators     |

### **Aggregation Options**

| Function   | Description        | Best For                                 |
| ---------- | ------------------ | ---------------------------------------- |
| `"count"`  | Count records      | Frequency analysis, occurrence counting  |
| `"sum"`    | Sum values         | Total amounts, cumulative metrics        |
| `"mean"`   | Average values     | Performance indicators, typical values   |
| `"median"` | Middle value       | Robust central tendency, skewed data     |
| `"min"`    | Minimum value      | Worst-case scenarios, lower bounds       |
| `"max"`    | Maximum value      | Best-case scenarios, upper bounds        |
| `"std"`    | Standard deviation | Variability measurement, risk assessment |
| `"var"`    | Variance           | Spread analysis, consistency metrics     |

### **Formatting Parameters**

| Parameter    | Type    | Description            | Example Values              |
| ------------ | ------- | ---------------------- | --------------------------- |
| `sort_by`    | string  | Column to sort by      | "value", "category", "date" |
| `sort_order` | string  | Sort direction         | "asc", "desc"               |
| `limit`      | integer | Limit results          | 10, 20, 50                  |
| `normalize`  | boolean | Show as percentages    | true, false                 |
| `cumulative` | boolean | Show cumulative values | true, false                 |
| `percentage` | boolean | Convert to percentages | true, false                 |

### **Time Series Parameters**

| Parameter        | Type    | Description            | Use Cases                                 |
| ---------------- | ------- | ---------------------- | ----------------------------------------- |
| `time_unit`      | string  | Time aggregation level | "day", "week", "month", "quarter", "year" |
| `rolling_window` | integer | Moving average window  | 7, 30, 90 (days)                          |

---

## 📋 Chart Selection Matrix

### **By Data Types**

| X-Axis Type         | Y-Axis Type | Recommended Charts            |
| ------------------- | ----------- | ----------------------------- |
| **Categorical**     | **Numeric** | Bar, Box, Violin, Stacked Bar |
| **Numeric**         | **Numeric** | Scatter, Bubble, Heatmap      |
| **Time/Sequential** | **Numeric** | Line, Area, Multi-line        |
| **Categorical**     | **None**    | Pie, Donut, Treemap           |
| **Numeric**         | **None**    | Histogram, Density            |

### **By Analysis Goal**

| Goal                   | Primary Charts     | Secondary Options        |
| ---------------------- | ------------------ | ------------------------ |
| **Compare Categories** | Bar, Grouped Bar   | Box, Violin              |
| **Show Trends**        | Line, Area         | Multi-line, Stacked Area |
| **Find Relationships** | Scatter, Bubble    | Heatmap                  |
| **Show Distributions** | Histogram, Density | Box, Violin              |
| **Part-to-Whole**      | Pie, Donut         | Treemap, Stacked Bar     |
| **Hierarchical Data**  | Treemap, Sunburst  | Sankey                   |
| **Multi-dimensional**  | Radar, Bubble      | Heatmap                  |
| **Process Flow**       | Funnel, Waterfall  | Sankey                   |

### **By Data Size**

| Data Size               | Recommended Charts                   | Avoid                   |
| ----------------------- | ------------------------------------ | ----------------------- |
| **Small (< 50 points)** | All charts work well                 | -                       |
| **Medium (50-1000)**    | Most charts, consider aggregation    | Pie with many slices    |
| **Large (1000+)**       | Aggregated charts, heatmaps, density | Individual point charts |

---


## 🔍 Error Handling & Troubleshooting

### **Common Errors**

| Error Message                                                  | Cause                           | Solution                                  |
| -------------------------------------------------------------- | ------------------------------- | ----------------------------------------- |
| `"x_axis is required"`                                         | Missing required parameter      | Add x_axis parameter                      |
| `"Both x_axis and y_axis are required"`                        | Missing required parameters     | Add both parameters                       |
| `"File {file_id} not found"`                                   | Invalid file ID                 | Use valid file ID from upload             |
| `"Chart type {type} not implemented"`                          | Unsupported chart type          | Use supported chart types                 |
| `"Radar charts require at least 3 numeric columns"`            | Insufficient numeric data       | Ensure dataset has enough numeric columns |
| `"x_axis, y_axis, and size_by are required for bubble charts"` | Missing bubble chart parameters | Provide all required parameters           |

### **Data Quality Issues**

| Issue                   | Symptoms                                | Solutions                                        |
| ----------------------- | --------------------------------------- | ------------------------------------------------ |
| **Missing Values**      | Gaps in charts, reduced data points     | Use `dropna()` preprocessing, imputation         |
| **Wrong Data Types**    | Categorical treated as numeric          | Verify column data types in upload response      |
| **Too Many Categories** | Cluttered pie charts, unreadable labels | Use `limit` parameter, group small categories    |
| **Outliers**            | Skewed scales, hidden patterns          | Use box plots to identify, consider filtering    |
| **Insufficient Data**   | Empty charts, single points             | Verify data filtering, check aggregation results |

### **Performance Optimization**

| Scenario              | Recommendation                     | Implementation                            |
| --------------------- | ---------------------------------- | ----------------------------------------- |
| **Large Datasets**    | Use aggregation, sampling          | Set `limit` parameter, pre-aggregate data |
| **Many Categories**   | Limit categories, group others     | Use `limit` parameter, "Other" grouping   |
| **Time Series**       | Appropriate time units             | Use `time_unit` parameter for aggregation |
| **Real-time Updates** | Cache results, incremental updates | Implement caching strategy                |

---

## 💡 Best Practices & Tips

### **Chart Selection Guidelines**

1. **Start Simple**: Begin with basic charts (bar, line, scatter) before advanced ones
2. **Know Your Audience**: Technical audiences can handle complex charts, general audiences prefer simple ones
3. **Consider Data Size**: Large datasets need aggregation or sampling
4. **Match Chart to Question**: Each chart type answers specific questions best

### **Parameter Optimization**

1. **Aggregation Choice**:

   - Use `mean` for typical values
   - Use `sum` for totals
   - Use `median` for skewed data
   - Use `count` for frequencies

2. **Visual Encoding**:

   - `color_by` for categories (max 8-10 colors)
   - `size_by` for continuous importance
   - `shape_by` for additional categories (max 5-6 shapes)

3. **Sorting and Limiting**:
   - Always sort bar charts by value for clarity
   - Limit pie charts to 5-7 slices
   - Use `limit` parameter for top-N analysis

### **Frontend Integration Tips**

1. **Responsive Design**: Always set `responsive: true` in chart configs
2. **Color Consistency**: Use consistent color schemes across related charts
3. **Tooltips**: Provide detailed information on hover
4. **Accessibility**: Include alt text, keyboard navigation, color-blind friendly palettes
5. **Performance**: Debounce updates, use canvas for large datasets

### **API Usage Patterns**

1. **Exploration Workflow**:

   ```
   Upload → Get AI Suggestions → Try Different Chart Types → Refine Parameters
   ```

2. **Dashboard Creation**:

   ```
   Upload → Generate Multiple Chart Types → Cache Results → Update Periodically
   ```

3. **Analysis Deep-Dive**:
   ```
   Start with Overview Charts → Drill Down with Filters → Use Statistical Charts
   ```

---

## 🚀 Advanced Use Cases

### **Business Intelligence Dashboard**

```javascript
// Multi-chart dashboard example
const dashboardCharts = [
  {
    type: "bar",
    title: "Sales by Region",
    parameters: { x_axis: "region", y_axis: "sales", aggregation: "sum" },
  },
  {
    type: "line",
    title: "Monthly Trends",
    parameters: { x_axis: "date", y_axis: "sales", time_unit: "month" },
  },
  {
    type: "pie",
    title: "Product Mix",
    parameters: { x_axis: "product_category", limit: 5 },
  },
  {
    type: "scatter",
    title: "Price vs Quality",
    parameters: { x_axis: "price", y_axis: "quality", color_by: "category" },
  },
];
```

### **Statistical Analysis Workflow**

```javascript
// Comprehensive data exploration
const analysisCharts = [
  // Distribution analysis
  { type: "histogram", parameters: { x_axis: "value", bins: 20 } },
  { type: "box", parameters: { y_axis: "value", x_axis: "category" } },
  { type: "violin", parameters: { y_axis: "value", x_axis: "category" } },

  // Relationship analysis
  { type: "scatter", parameters: { x_axis: "var1", y_axis: "var2" } },
  {
    type: "heatmap",
    parameters: { x_axis: "var1", y_axis: "var2", color_by: "correlation" },
  },

  // Multi-dimensional analysis
  { type: "radar", parameters: { group_by: "category", aggregation: "mean" } },
  {
    type: "bubble",
    parameters: { x_axis: "var1", y_axis: "var2", size_by: "importance" },
  },
];
```

---

## 📚 Additional Resources

### **Chart Type Quick Reference**

| Need to...          | Use Chart Type                   | Key Parameters                         |
| ------------------- | -------------------------------- | -------------------------------------- |
| Compare categories  | `bar`, `grouped_bar`             | x_axis (categorical), y_axis (numeric) |
| Show trends         | `line`, `area`                   | x_axis (time), y_axis (numeric)        |
| Find correlations   | `scatter`, `bubble`              | x_axis, y_axis (both numeric)          |
| Show distributions  | `histogram`, `density`, `violin` | x_axis (numeric)                       |
| Part-to-whole       | `pie`, `donut`, `treemap`        | x_axis (categorical)                   |
| Multi-dimensional   | `radar`, `bubble`, `heatmap`     | Multiple numeric columns               |
| Statistical summary | `box`, `violin`                  | y_axis (numeric), x_axis (categorical) |
| Process flow        | `funnel`, `waterfall`, `sankey`  | Sequential data                        |

### **Parameter Combinations**

| Chart Type  | Required                | Optional                        | Advanced             |
| ----------- | ----------------------- | ------------------------------- | -------------------- |
| **Bar**     | x_axis                  | y_axis, aggregation, sort_order | limit, normalize     |
| **Scatter** | x_axis, y_axis          | color_by, size_by               | opacity_by, shape_by |
| **Heatmap** | x_axis, y_axis          | color_by, aggregation           | normalize, threshold |
| **Radar**   | -                       | group_by, aggregation           | limit, normalize     |
| **Bubble**  | x_axis, y_axis, size_by | color_by                        | opacity_by           |

Happy charting! 📊✨

_This comprehensive guide covers all 24+ chart types supported by the Análisis al Instante API. For specific implementation questions or advanced use cases, refer to the interactive API documentation at `/docs`._
