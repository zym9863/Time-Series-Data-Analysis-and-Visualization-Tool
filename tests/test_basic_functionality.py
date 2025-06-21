"""
基本功能测试

测试各个模块的基本功能
"""

import sys
import os
import pandas as pd
import numpy as np

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processing.data_loader import DataLoader
from data_processing.preprocessor import TimeSeriesPreprocessor
from analysis.acf_pacf import ACFPACFAnalyzer
from visualization.plots import TimeSeriesPlotter
from utils.helpers import validate_time_series, format_data


def test_data_loader():
    """测试数据加载器"""
    print("测试数据加载器...")
    
    loader = DataLoader()
    
    # 测试示例数据生成
    df = loader.create_sample_data(n_points=100)
    assert len(df) == 100
    assert 'date' in df.columns
    assert 'value' in df.columns
    print("✓ 示例数据生成测试通过")
    
    # 测试数据验证
    is_valid = loader.validate_time_series_data(df, 'date', 'value')
    assert is_valid == True
    print("✓ 数据验证测试通过")


def test_preprocessor():
    """测试数据预处理器"""
    print("测试数据预处理器...")
    
    preprocessor = TimeSeriesPreprocessor()
    loader = DataLoader()
    
    # 创建测试数据
    df = loader.create_sample_data(n_points=50)
    
    # 测试数据清洗
    cleaned_df = preprocessor.clean_data(df, 'date', 'value')
    assert len(cleaned_df) == 50
    print("✓ 数据清洗测试通过")
    
    # 测试缺失值处理
    # 人工添加一些缺失值
    df_with_na = df.copy()
    df_with_na.loc[5:10, 'value'] = np.nan
    
    filled_df = preprocessor.handle_missing_values(df_with_na, 'value', 'interpolate')
    assert filled_df['value'].isnull().sum() == 0
    print("✓ 缺失值处理测试通过")
    
    # 测试差分
    diff_df = preprocessor.difference_series(df, 'value', 1)
    assert 'value_diff_1' in diff_df.columns
    print("✓ 差分测试通过")
    
    # 测试统计摘要
    summary = preprocessor.get_data_summary(df, 'value')
    assert '数据点数量' in summary
    assert summary['数据点数量'] == 50
    print("✓ 统计摘要测试通过")


def test_acf_pacf_analyzer():
    """测试ACF/PACF分析器"""
    print("测试ACF/PACF分析器...")
    
    analyzer = ACFPACFAnalyzer()
    loader = DataLoader()
    
    # 创建测试数据
    df = loader.create_sample_data(n_points=100)
    data = df['value']
    
    # 测试ACF计算
    acf_result = analyzer.calculate_acf(data, nlags=20)
    assert 'acf_values' in acf_result
    assert len(acf_result['acf_values']) == 21  # 包括lag=0
    print("✓ ACF计算测试通过")
    
    # 测试PACF计算
    pacf_result = analyzer.calculate_pacf(data, nlags=20)
    assert 'pacf_values' in pacf_result
    assert len(pacf_result['pacf_values']) == 21  # 包括lag=0
    print("✓ PACF计算测试通过")
    
    # 测试模型建议
    suggestions = analyzer.suggest_arima_order(acf_result, pacf_result)
    assert 'suggestions' in suggestions
    assert len(suggestions['suggestions']) > 0
    print("✓ 模型建议测试通过")
    
    # 测试平稳性检验
    stationarity_results = analyzer.test_stationarity(data)
    assert 'adf' in stationarity_results or 'kpss' in stationarity_results
    print("✓ 平稳性检验测试通过")


def test_time_series_plotter():
    """测试时序数据绘图器"""
    print("测试时序数据绘图器...")
    
    plotter = TimeSeriesPlotter()
    loader = DataLoader()
    analyzer = ACFPACFAnalyzer()
    
    # 创建测试数据
    df = loader.create_sample_data(n_points=50)
    data = df['value']
    
    # 测试时序图绘制
    fig = plotter.plot_time_series(df)
    assert fig is not None
    print("✓ 时序图绘制测试通过")
    
    # 测试ACF图绘制
    acf_result = analyzer.calculate_acf(data, nlags=10)
    fig_acf = plotter.plot_acf(acf_result)
    assert fig_acf is not None
    print("✓ ACF图绘制测试通过")
    
    # 测试PACF图绘制
    pacf_result = analyzer.calculate_pacf(data, nlags=10)
    fig_pacf = plotter.plot_pacf(pacf_result)
    assert fig_pacf is not None
    print("✓ PACF图绘制测试通过")
    
    # 测试组合图绘制
    fig_combined = plotter.plot_acf_pacf_combined(acf_result, pacf_result)
    assert fig_combined is not None
    print("✓ ACF/PACF组合图绘制测试通过")
    
    # 测试数据分布图
    fig_dist = plotter.plot_data_distribution(data)
    assert fig_dist is not None
    print("✓ 数据分布图绘制测试通过")


def test_utils():
    """测试工具函数"""
    print("测试工具函数...")
    
    # 测试时序数据验证
    valid_data = pd.Series([1, 2, 3, 4, 5])
    assert validate_time_series(valid_data) == True
    
    invalid_data = pd.Series([])
    assert validate_time_series(invalid_data) == False
    print("✓ 时序数据验证测试通过")
    
    # 测试数据格式化
    loader = DataLoader()
    df = loader.create_sample_data(n_points=20)
    formatted_df = format_data(df, 'date', 'value')
    assert 'date' in formatted_df.columns
    assert 'value' in formatted_df.columns
    print("✓ 数据格式化测试通过")


def run_all_tests():
    """运行所有测试"""
    print("开始运行所有测试...\n")
    
    try:
        test_data_loader()
        print()
        
        test_preprocessor()
        print()
        
        test_acf_pacf_analyzer()
        print()
        
        test_time_series_plotter()
        print()
        
        test_utils()
        print()
        
        print("🎉 所有测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    if not success:
        sys.exit(1)
