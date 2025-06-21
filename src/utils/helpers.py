"""
工具函数模块

提供通用的辅助函数
"""

import pandas as pd
import numpy as np
from typing import Union, List, Tuple, Optional


def validate_time_series(data: Union[pd.Series, np.ndarray, List]) -> bool:
    """
    验证时序数据的有效性
    
    Args:
        data: 时序数据
        
    Returns:
        bool: 是否为有效的时序数据
    """
    try:
        # 转换为pandas Series
        if isinstance(data, (list, np.ndarray)):
            data = pd.Series(data)
        
        # 检查是否为空
        if len(data) == 0:
            return False
        
        # 检查是否包含数值
        if not pd.api.types.is_numeric_dtype(data):
            return False
        
        # 检查是否全为NaN
        if data.isnull().all():
            return False
        
        return True
    except:
        return False


def format_data(df: pd.DataFrame, 
                date_column: str, 
                value_column: str) -> pd.DataFrame:
    """
    格式化时序数据
    
    Args:
        df: 原始数据框
        date_column: 日期列名
        value_column: 数值列名
        
    Returns:
        pd.DataFrame: 格式化后的数据
    """
    formatted_df = df[[date_column, value_column]].copy()
    formatted_df.columns = ['date', 'value']
    
    # 确保日期列为datetime类型
    formatted_df['date'] = pd.to_datetime(formatted_df['date'])
    
    # 确保数值列为数值类型
    formatted_df['value'] = pd.to_numeric(formatted_df['value'], errors='coerce')
    
    # 按日期排序
    formatted_df = formatted_df.sort_values('date').reset_index(drop=True)
    
    return formatted_df


def calculate_statistics(data: pd.Series) -> dict:
    """
    计算基本统计信息
    
    Args:
        data: 时序数据
        
    Returns:
        dict: 统计信息
    """
    return {
        'count': len(data),
        'mean': data.mean(),
        'std': data.std(),
        'min': data.min(),
        'max': data.max(),
        'median': data.median(),
        'q25': data.quantile(0.25),
        'q75': data.quantile(0.75),
        'skewness': data.skew(),
        'kurtosis': data.kurtosis()
    }


def detect_frequency(dates: pd.Series) -> str:
    """
    检测时序数据的频率
    
    Args:
        dates: 日期序列
        
    Returns:
        str: 频率描述
    """
    try:
        # 计算日期差值
        diff = dates.diff().dropna()
        
        # 获取最常见的差值
        mode_diff = diff.mode().iloc[0]
        
        if mode_diff == pd.Timedelta(days=1):
            return "日频"
        elif mode_diff == pd.Timedelta(days=7):
            return "周频"
        elif mode_diff == pd.Timedelta(days=30):
            return "月频"
        elif mode_diff == pd.Timedelta(days=365):
            return "年频"
        else:
            return f"自定义频率: {mode_diff}"
    except:
        return "未知频率"


def check_stationarity_visual(data: pd.Series, window: int = 12) -> dict:
    """
    通过滚动统计检查平稳性
    
    Args:
        data: 时序数据
        window: 滚动窗口大小
        
    Returns:
        dict: 滚动统计结果
    """
    rolling_mean = data.rolling(window=window).mean()
    rolling_std = data.rolling(window=window).std()
    
    return {
        'rolling_mean': rolling_mean,
        'rolling_std': rolling_std,
        'original': data
    }


def prepare_data_for_analysis(df: pd.DataFrame, 
                             value_column: str = 'value') -> pd.Series:
    """
    为分析准备数据
    
    Args:
        df: 数据框
        value_column: 数值列名
        
    Returns:
        pd.Series: 准备好的时序数据
    """
    # 提取数值列
    data = df[value_column].copy()
    
    # 移除缺失值
    data = data.dropna()
    
    # 重置索引
    data = data.reset_index(drop=True)
    
    return data


def format_number(value: float, decimal_places: int = 4) -> str:
    """
    格式化数字显示
    
    Args:
        value: 数值
        decimal_places: 小数位数
        
    Returns:
        str: 格式化后的字符串
    """
    if pd.isna(value):
        return "N/A"
    
    return f"{value:.{decimal_places}f}"


def create_lag_features(data: pd.Series, max_lags: int = 10) -> pd.DataFrame:
    """
    创建滞后特征
    
    Args:
        data: 时序数据
        max_lags: 最大滞后阶数
        
    Returns:
        pd.DataFrame: 包含滞后特征的数据框
    """
    result_df = pd.DataFrame({'value': data})
    
    for lag in range(1, max_lags + 1):
        result_df[f'lag_{lag}'] = data.shift(lag)
    
    return result_df
