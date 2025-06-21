"""
数据加载器模块

支持多种格式的时序数据导入
"""

import pandas as pd
import numpy as np
from typing import Optional, Union, List
import io
import streamlit as st


class DataLoader:
    """时序数据加载器"""
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.txt']
    
    def load_from_file(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        从文件加载数据
        
        Args:
            file_path: 文件路径
            **kwargs: 传递给pandas读取函数的参数
            
        Returns:
            pd.DataFrame: 加载的数据
        """
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension == 'csv':
            return pd.read_csv(file_path, **kwargs)
        elif file_extension in ['xlsx', 'xls']:
            return pd.read_excel(file_path, **kwargs)
        elif file_extension == 'txt':
            return pd.read_csv(file_path, sep='\t', **kwargs)
        else:
            raise ValueError(f"不支持的文件格式: {file_extension}")
    
    def load_from_uploaded_file(self, uploaded_file, **kwargs) -> pd.DataFrame:
        """
        从Streamlit上传的文件加载数据
        
        Args:
            uploaded_file: Streamlit上传的文件对象
            **kwargs: 传递给pandas读取函数的参数
            
        Returns:
            pd.DataFrame: 加载的数据
        """
        if uploaded_file is None:
            raise ValueError("未选择文件")
        
        file_extension = uploaded_file.name.lower().split('.')[-1]
        
        if file_extension == 'csv':
            return pd.read_csv(uploaded_file, **kwargs)
        elif file_extension in ['xlsx', 'xls']:
            return pd.read_excel(uploaded_file, **kwargs)
        elif file_extension == 'txt':
            return pd.read_csv(uploaded_file, sep='\t', **kwargs)
        else:
            raise ValueError(f"不支持的文件格式: {file_extension}")
    
    def create_sample_data(self, 
                          n_points: int = 100, 
                          trend: bool = True, 
                          seasonality: bool = True, 
                          noise_level: float = 0.1) -> pd.DataFrame:
        """
        创建示例时序数据
        
        Args:
            n_points: 数据点数量
            trend: 是否包含趋势
            seasonality: 是否包含季节性
            noise_level: 噪声水平
            
        Returns:
            pd.DataFrame: 示例数据
        """
        dates = pd.date_range(start='2020-01-01', periods=n_points, freq='D')
        
        # 基础值
        values = np.zeros(n_points)
        
        # 添加趋势
        if trend:
            values += np.linspace(0, 10, n_points)
        
        # 添加季节性
        if seasonality:
            values += 3 * np.sin(2 * np.pi * np.arange(n_points) / 30)
        
        # 添加噪声
        values += np.random.normal(0, noise_level, n_points)
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    def validate_time_series_data(self, df: pd.DataFrame, 
                                 date_column: str, 
                                 value_column: str) -> bool:
        """
        验证时序数据格式
        
        Args:
            df: 数据框
            date_column: 日期列名
            value_column: 数值列名
            
        Returns:
            bool: 是否为有效的时序数据
        """
        try:
            # 检查列是否存在
            if date_column not in df.columns or value_column not in df.columns:
                return False
            
            # 检查日期列是否可以转换为日期类型
            pd.to_datetime(df[date_column])
            
            # 检查数值列是否为数值类型
            pd.to_numeric(df[value_column])
            
            return True
        except:
            return False
