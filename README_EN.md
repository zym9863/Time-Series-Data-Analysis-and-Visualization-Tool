# Time Series Data Analysis and Visualization Tool

[中文文档 (Chinese README)](README.md)

A Python and Streamlit-based tool for time series data analysis and visualization, focusing on ACF/PACF analysis and time series model identification.

## 🚀 Features

### Core Features
- **Data Import & Preprocessing**: Supports multiple data formats and provides comprehensive preprocessing
- **ACF/PACF Analysis**: Compute and visualize autocorrelation and partial autocorrelation functions
- **Smart Model Suggestion**: Automatically recommends ARIMA model parameters based on ACF/PACF patterns
- **Interactive Visualization**: Rich interactive charts powered by Plotly

### Data Processing Features
- 📁 Multi-format file support (CSV, Excel, TXT)
- 🧹 Data cleaning and validation
- 🔧 Missing value handling (interpolation, forward fill, backward fill, etc.)
- 📊 Outlier detection and removal
- 📈 Data transformation (differencing, log transform, standardization)
- 📋 Detailed data summary statistics

### Analysis Features
- 🔍 ACF/PACF calculation and visualization
- 📊 Stationarity tests (ADF, KPSS)
- 🤖 Smart ARIMA parameter suggestion
- 📈 Ljung-Box white noise test
- 📊 Time series decomposition support

### Visualization Features
- 📈 Time series plots
- 📊 ACF/PACF plots
- 📋 Data distribution plots (histogram, boxplot)
- 🎨 Interactive chart support

## 🛠️ Tech Stack

- **Python 3.12+**
- **Streamlit**: Web UI framework
- **pandas**: Data processing
- **numpy**: Numerical computation
- **statsmodels**: Time series analysis
- **plotly**: Interactive visualization
- **matplotlib/seaborn**: Static charts
- **uv**: Package manager

## 📦 Installation & Run

### Requirements
- Python 3.12 or higher
- uv package manager

### Installation Steps

1. **Clone the project**
```bash
git clone https://github.com/zym9863/Time-Series-Data-Analysis-and-Visualization-Tool.git
cd Time-Series-Data-Analysis-and-Visualization-Tool
```

2. **Install dependencies**
```bash
uv sync
```

3. **Run the app**
```bash
uv run streamlit run main.py
```

4. **Access the app**
Open your browser and visit `http://localhost:8501`

## 📖 User Guide

### 1. Data Import & Preprocessing

#### Upload File
- Supports CSV, Excel, TXT formats
- Auto-detects and validates data format
- Provides data preview and summary

#### Use Sample Data
- Configurable data points, trend, seasonality, and noise
- Quickly generate test data for analysis

#### Preprocessing Options
- **Missing value handling**: Interpolation, forward fill, backward fill, mean fill, removal
- **Outlier handling**: IQR method, Z-score method
- **Data transformation**: Differencing, log transform, standardization

### 2. ACF/PACF Analysis

#### Analysis Parameters
- Lag order setting (5-50)
- Confidence level selection (99%, 95%, 90%)
- Supports analysis on raw and preprocessed data

#### Analysis Results
- Interactive ACF/PACF plots
- Confidence interval display
- Automatic model parameter suggestion
- Stationarity test results

### 3. Model Suggestion

Based on the classic Box-Jenkins methodology:

#### AR Model Identification
- PACF cutoff, ACF tailing
- For autoregressive processes

#### MA Model Identification
- ACF cutoff, PACF tailing
- For moving average processes

#### ARMA Model Identification
- Both ACF and PACF tailing
- For mixed processes

### 4. Data Visualization

#### Time Series Plot
- Compare raw and preprocessed data
- Interactive zoom and pan
- Data point hover info

#### Distribution Plot
- Histogram for data distribution
- Boxplot for outlier detection
- Statistical info display

## 🧪 Testing

Run the test suite to verify functionality:

```bash
uv run python tests/test_basic_functionality.py
```

Test coverage:
- ✅ Data loader
- ✅ Data preprocessing
- ✅ ACF/PACF analysis
- ✅ Visualization
- ✅ Utility functions

## 📁 Project Structure

```
Time-Series-Data-Analysis-and-Visualization-Tool/
├── main.py                 # Streamlit main app
├── pyproject.toml         # Project config
├── uv.lock               # Dependency lock file
├── README.md             # Project documentation (Chinese)
├── README_EN.md          # Project documentation (English)
├── src/                  # Source code
│   ├── __init__.py
│   ├── data_processing/  # Data processing module
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   └── preprocessor.py
│   ├── analysis/         # Analysis module
│   │   ├── __init__.py
│   │   └── acf_pacf.py
│   ├── visualization/    # Visualization module
│   │   ├── __init__.py
│   │   └── plots.py
│   └── utils/           # Utility module
│       ├── __init__.py
│       └── helpers.py
└── tests/               # Tests
    └── test_basic_functionality.py
```

## 🎯 Usage Example

### Basic Workflow

1. **Import data**: Upload CSV or generate sample data
2. **Preprocess data**: Handle missing/outlier values, apply transformations
3. **ACF/PACF analysis**: Compute correlations, view plots
4. **Model identification**: Get model suggestions based on analysis
5. **Result interpretation**: Understand model features and scenarios

### Typical Analysis Scenarios

#### Scenario 1: Stock Price Analysis
- Import stock price data
- Apply log transform and differencing
- Analyze ACF/PACF patterns
- Identify suitable ARIMA model

#### Scenario 2: Sales Data Analysis
- Import monthly sales data
- Handle seasonality and trend
- Analyze correlation structure
- Build forecasting model

## 🤝 Contributing

Contributions are welcome!

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter issues or have suggestions:
- Check the docs and examples
- Run tests to verify your environment
- Submit an Issue with details
