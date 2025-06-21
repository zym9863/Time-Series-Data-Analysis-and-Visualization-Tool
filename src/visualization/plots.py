"""
可视化模块

提供时序数据和分析结果的可视化功能
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple, List
import streamlit as st

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


class TimeSeriesPlotter:
    """时序数据可视化器"""
    
    def __init__(self):
        self.color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        self.figure_size = (12, 6)
    
    def plot_time_series(self, 
                        df: pd.DataFrame, 
                        date_column: str = 'date', 
                        value_column: str = 'value',
                        title: str = '时序数据',
                        interactive: bool = True) -> go.Figure:
        """
        绘制时序数据图
        
        Args:
            df: 数据框
            date_column: 日期列名
            value_column: 数值列名
            title: 图表标题
            interactive: 是否使用交互式图表
            
        Returns:
            plotly图表对象
        """
        if interactive:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df[date_column],
                y=df[value_column],
                mode='lines',
                name='时序数据',
                line=dict(color=self.color_palette[0], width=2)
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title='时间',
                yaxis_title='数值',
                hovermode='x unified',
                template='plotly_white'
            )
            
            return fig
        else:
            fig, ax = plt.subplots(figsize=self.figure_size)
            ax.plot(df[date_column], df[value_column], 
                   color=self.color_palette[0], linewidth=2)
            ax.set_title(title)
            ax.set_xlabel('时间')
            ax.set_ylabel('数值')
            plt.xticks(rotation=45)
            plt.tight_layout()
            return fig
    
    def plot_acf(self, 
                acf_result: Dict, 
                title: str = '自相关函数 (ACF)',
                interactive: bool = True) -> go.Figure:
        """
        绘制ACF图
        
        Args:
            acf_result: ACF计算结果
            title: 图表标题
            interactive: 是否使用交互式图表
            
        Returns:
            plotly图表对象
        """
        lags = acf_result['lags']
        acf_values = acf_result['acf_values']
        upper_bound = acf_result['upper_bound']
        lower_bound = acf_result['lower_bound']
        
        if interactive:
            fig = go.Figure()
            
            # ACF值
            fig.add_trace(go.Scatter(
                x=lags,
                y=acf_values,
                mode='markers+lines',
                name='ACF',
                line=dict(color=self.color_palette[0], width=2),
                marker=dict(size=6)
            ))
            
            # 置信区间
            fig.add_trace(go.Scatter(
                x=lags,
                y=upper_bound,
                mode='lines',
                name='95%置信区间上界',
                line=dict(color='red', dash='dash', width=1),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=lags,
                y=lower_bound,
                mode='lines',
                name='95%置信区间下界',
                line=dict(color='red', dash='dash', width=1),
                fill='tonexty',
                fillcolor='rgba(255,0,0,0.1)',
                showlegend=False
            ))
            
            # 零线
            fig.add_hline(y=0, line_dash="solid", line_color="black", line_width=1)
            
            fig.update_layout(
                title=title,
                xaxis_title='滞后阶数',
                yaxis_title='自相关系数',
                template='plotly_white',
                hovermode='x unified'
            )
            
            return fig
        else:
            fig, ax = plt.subplots(figsize=self.figure_size)
            
            # 绘制ACF值
            ax.plot(lags, acf_values, 'o-', color=self.color_palette[0], 
                   linewidth=2, markersize=4)
            
            # 绘制置信区间
            ax.fill_between(lags, lower_bound, upper_bound, 
                           alpha=0.2, color='red')
            ax.plot(lags, upper_bound, '--', color='red', linewidth=1)
            ax.plot(lags, lower_bound, '--', color='red', linewidth=1)
            
            # 零线
            ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
            
            ax.set_title(title)
            ax.set_xlabel('滞后阶数')
            ax.set_ylabel('自相关系数')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            return fig
    
    def plot_pacf(self, 
                 pacf_result: Dict, 
                 title: str = '偏自相关函数 (PACF)',
                 interactive: bool = True) -> go.Figure:
        """
        绘制PACF图
        
        Args:
            pacf_result: PACF计算结果
            title: 图表标题
            interactive: 是否使用交互式图表
            
        Returns:
            plotly图表对象
        """
        lags = pacf_result['lags']
        pacf_values = pacf_result['pacf_values']
        upper_bound = pacf_result['upper_bound']
        lower_bound = pacf_result['lower_bound']
        
        if interactive:
            fig = go.Figure()
            
            # PACF值
            fig.add_trace(go.Scatter(
                x=lags,
                y=pacf_values,
                mode='markers+lines',
                name='PACF',
                line=dict(color=self.color_palette[1], width=2),
                marker=dict(size=6)
            ))
            
            # 置信区间
            fig.add_trace(go.Scatter(
                x=lags,
                y=upper_bound,
                mode='lines',
                name='95%置信区间上界',
                line=dict(color='red', dash='dash', width=1),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=lags,
                y=lower_bound,
                mode='lines',
                name='95%置信区间下界',
                line=dict(color='red', dash='dash', width=1),
                fill='tonexty',
                fillcolor='rgba(255,0,0,0.1)',
                showlegend=False
            ))
            
            # 零线
            fig.add_hline(y=0, line_dash="solid", line_color="black", line_width=1)
            
            fig.update_layout(
                title=title,
                xaxis_title='滞后阶数',
                yaxis_title='偏自相关系数',
                template='plotly_white',
                hovermode='x unified'
            )
            
            return fig
        else:
            fig, ax = plt.subplots(figsize=self.figure_size)
            
            # 绘制PACF值
            ax.plot(lags, pacf_values, 'o-', color=self.color_palette[1], 
                   linewidth=2, markersize=4)
            
            # 绘制置信区间
            ax.fill_between(lags, lower_bound, upper_bound, 
                           alpha=0.2, color='red')
            ax.plot(lags, upper_bound, '--', color='red', linewidth=1)
            ax.plot(lags, lower_bound, '--', color='red', linewidth=1)
            
            # 零线
            ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
            
            ax.set_title(title)
            ax.set_xlabel('滞后阶数')
            ax.set_ylabel('偏自相关系数')
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            return fig
    
    def plot_acf_pacf_combined(self, 
                              acf_result: Dict, 
                              pacf_result: Dict,
                              interactive: bool = True) -> go.Figure:
        """
        绘制ACF和PACF组合图
        
        Args:
            acf_result: ACF计算结果
            pacf_result: PACF计算结果
            interactive: 是否使用交互式图表
            
        Returns:
            plotly图表对象
        """
        if interactive:
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('自相关函数 (ACF)', '偏自相关函数 (PACF)'),
                vertical_spacing=0.1
            )
            
            # ACF图
            fig.add_trace(
                go.Scatter(
                    x=acf_result['lags'],
                    y=acf_result['acf_values'],
                    mode='markers+lines',
                    name='ACF',
                    line=dict(color=self.color_palette[0], width=2),
                    marker=dict(size=6)
                ),
                row=1, col=1
            )
            
            # ACF置信区间
            fig.add_trace(
                go.Scatter(
                    x=acf_result['lags'],
                    y=acf_result['upper_bound'],
                    mode='lines',
                    line=dict(color='red', dash='dash', width=1),
                    showlegend=False
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=acf_result['lags'],
                    y=acf_result['lower_bound'],
                    mode='lines',
                    line=dict(color='red', dash='dash', width=1),
                    fill='tonexty',
                    fillcolor='rgba(255,0,0,0.1)',
                    showlegend=False
                ),
                row=1, col=1
            )
            
            # PACF图
            fig.add_trace(
                go.Scatter(
                    x=pacf_result['lags'],
                    y=pacf_result['pacf_values'],
                    mode='markers+lines',
                    name='PACF',
                    line=dict(color=self.color_palette[1], width=2),
                    marker=dict(size=6)
                ),
                row=2, col=1
            )
            
            # PACF置信区间
            fig.add_trace(
                go.Scatter(
                    x=pacf_result['lags'],
                    y=pacf_result['upper_bound'],
                    mode='lines',
                    line=dict(color='red', dash='dash', width=1),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=pacf_result['lags'],
                    y=pacf_result['lower_bound'],
                    mode='lines',
                    line=dict(color='red', dash='dash', width=1),
                    fill='tonexty',
                    fillcolor='rgba(255,0,0,0.1)',
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # 添加零线
            fig.add_hline(y=0, line_dash="solid", line_color="black", line_width=1, row=1, col=1)
            fig.add_hline(y=0, line_dash="solid", line_color="black", line_width=1, row=2, col=1)
            
            fig.update_xaxes(title_text="滞后阶数", row=2, col=1)
            fig.update_yaxes(title_text="自相关系数", row=1, col=1)
            fig.update_yaxes(title_text="偏自相关系数", row=2, col=1)
            
            fig.update_layout(
                title="ACF/PACF分析",
                template='plotly_white',
                height=800
            )
            
            return fig
        else:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            
            # ACF图
            ax1.plot(acf_result['lags'], acf_result['acf_values'], 'o-', 
                    color=self.color_palette[0], linewidth=2, markersize=4)
            ax1.fill_between(acf_result['lags'], acf_result['lower_bound'], 
                           acf_result['upper_bound'], alpha=0.2, color='red')
            ax1.axhline(y=0, color='black', linestyle='-', linewidth=1)
            ax1.set_title('自相关函数 (ACF)')
            ax1.set_ylabel('自相关系数')
            ax1.grid(True, alpha=0.3)
            
            # PACF图
            ax2.plot(pacf_result['lags'], pacf_result['pacf_values'], 'o-', 
                    color=self.color_palette[1], linewidth=2, markersize=4)
            ax2.fill_between(pacf_result['lags'], pacf_result['lower_bound'], 
                           pacf_result['upper_bound'], alpha=0.2, color='red')
            ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
            ax2.set_title('偏自相关函数 (PACF)')
            ax2.set_xlabel('滞后阶数')
            ax2.set_ylabel('偏自相关系数')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            return fig

    def plot_data_distribution(self,
                              data: pd.Series,
                              title: str = '数据分布',
                              interactive: bool = True) -> go.Figure:
        """
        绘制数据分布图

        Args:
            data: 时序数据
            title: 图表标题
            interactive: 是否使用交互式图表

        Returns:
            plotly图表对象
        """
        if interactive:
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('直方图', '箱线图'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}]]
            )

            # 直方图
            fig.add_trace(
                go.Histogram(
                    x=data,
                    nbinsx=30,
                    name='频数分布',
                    marker_color=self.color_palette[0],
                    opacity=0.7
                ),
                row=1, col=1
            )

            # 箱线图
            fig.add_trace(
                go.Box(
                    y=data,
                    name='数据分布',
                    marker_color=self.color_palette[1],
                    boxpoints='outliers'
                ),
                row=1, col=2
            )

            fig.update_layout(
                title=title,
                template='plotly_white',
                showlegend=False
            )

            return fig
        else:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

            # 直方图
            ax1.hist(data, bins=30, color=self.color_palette[0], alpha=0.7)
            ax1.set_title('直方图')
            ax1.set_xlabel('数值')
            ax1.set_ylabel('频数')

            # 箱线图
            ax2.boxplot(data)
            ax2.set_title('箱线图')
            ax2.set_ylabel('数值')

            plt.tight_layout()
            return fig
