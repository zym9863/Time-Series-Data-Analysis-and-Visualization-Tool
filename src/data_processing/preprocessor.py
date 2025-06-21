"""
时序数据预处理模块

提供数据清洗、缺失值处理、差分等预处理功能
"""

import pandas as pd
import numpy as np
from typing import Optional, Union, Tuple
from scipy import stats


class TimeSeriesPreprocessor:
    """时序数据预处理器"""
    
    def __init__(self):
        pass
    
    def clean_data(self, df: pd.DataFrame, 
                   date_column: str, 
                   value_column: str) -> pd.DataFrame:
        """
        清洗时序数据
        
        Args:
            df: 原始数据框
            date_column: 日期列名
            value_column: 数值列名
            
        Returns:
            pd.DataFrame: 清洗后的数据
        """
        # 复制数据
        cleaned_df = df.copy()
        
        # 转换日期列
        cleaned_df[date_column] = pd.to_datetime(cleaned_df[date_column])
        
        # 转换数值列
        cleaned_df[value_column] = pd.to_numeric(cleaned_df[value_column], errors='coerce')
        
        # 按日期排序
        cleaned_df = cleaned_df.sort_values(date_column)
        
        # 重置索引
        cleaned_df = cleaned_df.reset_index(drop=True)
        
        return cleaned_df
    
    def handle_missing_values(self, df: pd.DataFrame, 
                             value_column: str, 
                             method: str = 'interpolate') -> pd.DataFrame:
        """
        处理缺失值
        
        Args:
            df: 数据框
            value_column: 数值列名
            method: 处理方法 ('drop', 'forward_fill', 'backward_fill', 'interpolate', 'mean')
            
        Returns:
            pd.DataFrame: 处理后的数据
        """
        result_df = df.copy()
        
        if method == 'drop':
            result_df = result_df.dropna(subset=[value_column])
        elif method == 'forward_fill':
            result_df[value_column] = result_df[value_column].fillna(method='ffill')
        elif method == 'backward_fill':
            result_df[value_column] = result_df[value_column].fillna(method='bfill')
        elif method == 'interpolate':
            result_df[value_column] = result_df[value_column].interpolate()
        elif method == 'mean':
            mean_value = result_df[value_column].mean()
            result_df[value_column] = result_df[value_column].fillna(mean_value)
        else:
            raise ValueError(f"不支持的缺失值处理方法: {method}")
        
        return result_df
    
    def remove_outliers(self, df: pd.DataFrame, 
                       value_column: str, 
                       method: str = 'iqr',
                       threshold: float = 1.5) -> pd.DataFrame:
        """
        移除异常值
        
        Args:
            df: 数据框
            value_column: 数值列名
            method: 异常值检测方法 ('iqr', 'zscore')
            threshold: 阈值
            
        Returns:
            pd.DataFrame: 移除异常值后的数据
        """
        result_df = df.copy()
        values = result_df[value_column]
        
        if method == 'iqr':
            Q1 = values.quantile(0.25)
            Q3 = values.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            mask = (values >= lower_bound) & (values <= upper_bound)
        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(values))
            mask = z_scores < threshold
        else:
            raise ValueError(f"不支持的异常值检测方法: {method}")
        
        return result_df[mask]
    
    def difference_series(self, df: pd.DataFrame, 
                         value_column: str, 
                         periods: int = 1) -> pd.DataFrame:
        """
        对时序数据进行差分
        
        Args:
            df: 数据框
            value_column: 数值列名
            periods: 差分阶数
            
        Returns:
            pd.DataFrame: 差分后的数据
        """
        result_df = df.copy()
        result_df[f'{value_column}_diff_{periods}'] = result_df[value_column].diff(periods)
        return result_df
    
    def log_transform(self, df: pd.DataFrame, 
                     value_column: str) -> pd.DataFrame:
        """
        对数变换
        
        Args:
            df: 数据框
            value_column: 数值列名
            
        Returns:
            pd.DataFrame: 对数变换后的数据
        """
        result_df = df.copy()
        
        # 确保所有值都为正数
        min_value = result_df[value_column].min()
        if min_value <= 0:
            result_df[value_column] = result_df[value_column] - min_value + 1
        
        result_df[f'{value_column}_log'] = np.log(result_df[value_column])
        return result_df
    
    def standardize(self, df: pd.DataFrame, 
                   value_column: str) -> pd.DataFrame:
        """
        标准化数据
        
        Args:
            df: 数据框
            value_column: 数值列名
            
        Returns:
            pd.DataFrame: 标准化后的数据
        """
        result_df = df.copy()
        values = result_df[value_column]
        result_df[f'{value_column}_standardized'] = (values - values.mean()) / values.std()
        return result_df
    
    def get_data_summary(self, df: pd.DataFrame, 
                        value_column: str) -> dict:
        """
        获取数据摘要统计
        
        Args:
            df: 数据框
            value_column: 数值列名
            
        Returns:
            dict: 统计摘要
        """
        values = df[value_column]
        
        return {
            '数据点数量': len(values),
            '缺失值数量': values.isnull().sum(),
            '均值': values.mean(),
            '标准差': values.std(),
            '最小值': values.min(),
            '最大值': values.max(),
            '中位数': values.median(),
            '偏度': values.skew(),
            '峰度': values.kurtosis()
        }
