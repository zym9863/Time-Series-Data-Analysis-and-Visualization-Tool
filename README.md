# 时序数据分析与可视化工具

一个基于Python和Streamlit的时序数据分析与可视化工具，专注于ACF/PACF分析和时序模型识别。

## 🚀 功能特性

### 核心功能
- **数据导入与预处理**: 支持多种格式的数据导入，提供完整的数据预处理功能
- **ACF/PACF分析**: 计算并可视化自相关函数和偏自相关函数
- **智能模型建议**: 基于ACF/PACF模式自动推荐ARIMA模型参数
- **交互式可视化**: 使用Plotly提供丰富的交互式图表

### 数据处理功能
- 📁 多格式文件支持 (CSV, Excel, TXT)
- 🧹 数据清洗和验证
- 🔧 缺失值处理 (插值、前向填充、后向填充等)
- 📊 异常值检测和移除
- 📈 数据变换 (差分、对数变换、标准化)
- 📋 详细的数据统计摘要

### 分析功能
- 🔍 ACF/PACF计算和可视化
- 📊 平稳性检验 (ADF检验、KPSS检验)
- 🤖 智能ARIMA模型参数建议
- 📈 Ljung-Box白噪声检验
- 📊 时序分解支持

### 可视化功能
- 📈 时序数据图表
- 📊 ACF/PACF图表
- 📋 数据分布图 (直方图、箱线图)
- 🎨 交互式图表支持

## 🛠️ 技术栈

- **Python 3.12+**
- **Streamlit**: Web界面框架
- **pandas**: 数据处理
- **numpy**: 数值计算
- **statsmodels**: 时序分析
- **plotly**: 交互式可视化
- **matplotlib/seaborn**: 静态图表
- **uv**: 包管理器

## 📦 安装和运行

### 环境要求
- Python 3.12 或更高版本
- uv 包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/zym9863/Time-Series-Data-Analysis-and-Visualization-Tool.git
cd Time-Series-Data-Analysis-and-Visualization-Tool
```

2. **安装依赖**
```bash
uv sync
```

3. **运行应用**
```bash
uv run streamlit run main.py
```

4. **访问应用**
打开浏览器访问 `http://localhost:8501`

## 📖 使用指南

### 1. 数据导入与预处理

#### 上传文件
- 支持CSV、Excel、TXT格式
- 自动检测和验证数据格式
- 提供数据预览和统计摘要

#### 使用示例数据
- 可配置数据点数量、趋势、季节性和噪声水平
- 快速生成测试数据进行分析

#### 数据预处理选项
- **缺失值处理**: 插值、前向填充、后向填充、均值填充、删除
- **异常值处理**: IQR方法、Z-score方法
- **数据变换**: 差分、对数变换、标准化

### 2. ACF/PACF分析

#### 分析参数
- 滞后阶数设置 (5-50)
- 置信水平选择 (99%, 95%, 90%)
- 支持原始数据和预处理后数据分析

#### 分析结果
- 交互式ACF/PACF图表
- 置信区间显示
- 自动模型参数建议
- 平稳性检验结果

### 3. 模型建议

基于经典的Box-Jenkins方法论：

#### AR模型识别
- PACF截断，ACF拖尾
- 适用于自回归过程

#### MA模型识别
- ACF截断，PACF拖尾
- 适用于移动平均过程

#### ARMA模型识别
- ACF和PACF都拖尾
- 适用于混合过程

### 4. 数据可视化

#### 时序图
- 原始数据和预处理后数据对比
- 交互式缩放和平移
- 数据点悬停信息

#### 分布图
- 直方图显示数据分布
- 箱线图识别异常值
- 统计信息展示

## 🧪 测试

运行测试套件验证功能：

```bash
uv run python tests/test_basic_functionality.py
```

测试覆盖：
- ✅ 数据加载器功能
- ✅ 数据预处理功能
- ✅ ACF/PACF分析功能
- ✅ 可视化功能
- ✅ 工具函数

## 📁 项目结构

```
Time-Series-Data-Analysis-and-Visualization-Tool/
├── main.py                 # Streamlit主应用
├── pyproject.toml         # 项目配置
├── uv.lock               # 依赖锁定文件
├── README.md             # 项目说明
├── src/                  # 源代码目录
│   ├── __init__.py
│   ├── data_processing/  # 数据处理模块
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   └── preprocessor.py
│   ├── analysis/         # 分析模块
│   │   ├── __init__.py
│   │   └── acf_pacf.py
│   ├── visualization/    # 可视化模块
│   │   ├── __init__.py
│   │   └── plots.py
│   └── utils/           # 工具模块
│       ├── __init__.py
│       └── helpers.py
└── tests/               # 测试目录
    └── test_basic_functionality.py
```

## 🎯 使用示例

### 基本工作流程

1. **导入数据**: 上传CSV文件或生成示例数据
2. **数据预处理**: 处理缺失值、异常值，进行必要的变换
3. **ACF/PACF分析**: 计算相关函数，查看图表
4. **模型识别**: 根据分析结果获取模型建议
5. **结果解释**: 理解模型特征和适用场景

### 典型分析场景

#### 场景1: 股票价格分析
- 导入股票价格数据
- 进行对数变换和差分
- 分析ACF/PACF模式
- 识别合适的ARIMA模型

#### 场景2: 销售数据分析
- 导入月度销售数据
- 处理季节性和趋势
- 分析相关性结构
- 建立预测模型

## 🤝 贡献指南

欢迎贡献代码和建议！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

## 🆘 支持

如果遇到问题或有建议，请：
- 查看文档和示例
- 运行测试验证环境
- 提交 Issue 描述问题