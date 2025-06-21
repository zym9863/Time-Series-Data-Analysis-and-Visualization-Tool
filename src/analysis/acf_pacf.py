"""
ACF/PACF分析模块

实现自相关函数和偏自相关函数的计算
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional, Dict, List
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller, kpss
import warnings


class ACFPACFAnalyzer:
    """ACF/PACF分析器"""
    
    def __init__(self):
        self.confidence_level = 0.05  # 95%置信区间
    
    def calculate_acf(self, 
                     data: pd.Series, 
                     nlags: int = 40, 
                     alpha: float = 0.05) -> Dict:
        """
        计算自相关函数(ACF)
        
        Args:
            data: 时序数据
            nlags: 滞后阶数
            alpha: 显著性水平
            
        Returns:
            Dict: ACF结果
        """
        try:
            # 计算ACF
            acf_values, confint = acf(data, 
                                    nlags=nlags, 
                                    alpha=alpha, 
                                    fft=False)
            
            # 计算置信区间
            lower_bound = confint[:, 0] - acf_values
            upper_bound = confint[:, 1] - acf_values
            
            return {
                'acf_values': acf_values,
                'lags': np.arange(len(acf_values)),
                'confidence_interval': confint,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'alpha': alpha
            }
        except Exception as e:
            raise ValueError(f"ACF计算失败: {str(e)}")
    
    def calculate_pacf(self, 
                      data: pd.Series, 
                      nlags: int = 40, 
                      alpha: float = 0.05,
                      method: str = 'ywm') -> Dict:
        """
        计算偏自相关函数(PACF)
        
        Args:
            data: 时序数据
            nlags: 滞后阶数
            alpha: 显著性水平
            method: 计算方法 ('ywm', 'ols')
            
        Returns:
            Dict: PACF结果
        """
        try:
            # 计算PACF
            pacf_values, confint = pacf(data, 
                                      nlags=nlags, 
                                      alpha=alpha, 
                                      method=method)
            
            # 计算置信区间
            lower_bound = confint[:, 0] - pacf_values
            upper_bound = confint[:, 1] - pacf_values
            
            return {
                'pacf_values': pacf_values,
                'lags': np.arange(len(pacf_values)),
                'confidence_interval': confint,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'alpha': alpha,
                'method': method
            }
        except Exception as e:
            raise ValueError(f"PACF计算失败: {str(e)}")
    
    def suggest_arima_order(self, 
                           acf_result: Dict, 
                           pacf_result: Dict,
                           max_order: int = 5) -> Dict:
        """
        基于ACF/PACF结果建议ARIMA模型阶数
        
        Args:
            acf_result: ACF计算结果
            pacf_result: PACF计算结果
            max_order: 最大阶数
            
        Returns:
            Dict: 建议的模型阶数和解释
        """
        acf_values = acf_result['acf_values'][1:]  # 排除lag=0
        pacf_values = pacf_result['pacf_values'][1:]  # 排除lag=0
        
        # 计算显著性阈值
        n = len(acf_values)
        threshold = 1.96 / np.sqrt(n)  # 95%置信区间
        
        # 找到ACF和PACF显著截断的位置
        acf_cutoff = self._find_cutoff(acf_values, threshold, max_order)
        pacf_cutoff = self._find_cutoff(pacf_values, threshold, max_order)
        
        # 基于经典模式识别规则
        suggestions = []
        
        # AR模型: PACF截断，ACF拖尾
        if pacf_cutoff is not None and acf_cutoff is None:
            suggestions.append({
                'model': 'AR',
                'order': (pacf_cutoff, 0, 0),
                'explanation': f'PACF在滞后{pacf_cutoff}处截断，ACF拖尾，建议AR({pacf_cutoff})模型'
            })
        
        # MA模型: ACF截断，PACF拖尾
        elif acf_cutoff is not None and pacf_cutoff is None:
            suggestions.append({
                'model': 'MA',
                'order': (0, 0, acf_cutoff),
                'explanation': f'ACF在滞后{acf_cutoff}处截断，PACF拖尾，建议MA({acf_cutoff})模型'
            })
        
        # ARMA模型: 两者都拖尾
        elif acf_cutoff is None and pacf_cutoff is None:
            suggestions.append({
                'model': 'ARMA',
                'order': (1, 0, 1),
                'explanation': 'ACF和PACF都拖尾，建议ARMA(1,1)模型'
            })
        
        # 混合情况
        else:
            if pacf_cutoff and acf_cutoff:
                suggestions.append({
                    'model': 'ARMA',
                    'order': (pacf_cutoff, 0, acf_cutoff),
                    'explanation': f'建议ARMA({pacf_cutoff},{acf_cutoff})模型'
                })
        
        # 如果没有明确的模式，提供一些常见的选择
        if not suggestions:
            suggestions.extend([
                {
                    'model': 'AR',
                    'order': (1, 0, 0),
                    'explanation': '默认建议: AR(1)模型'
                },
                {
                    'model': 'MA',
                    'order': (0, 0, 1),
                    'explanation': '默认建议: MA(1)模型'
                },
                {
                    'model': 'ARMA',
                    'order': (1, 0, 1),
                    'explanation': '默认建议: ARMA(1,1)模型'
                }
            ])
        
        return {
            'suggestions': suggestions,
            'acf_cutoff': acf_cutoff,
            'pacf_cutoff': pacf_cutoff,
            'threshold': threshold
        }
    
    def _find_cutoff(self, values: np.ndarray, threshold: float, max_order: int) -> Optional[int]:
        """
        找到序列的截断点
        
        Args:
            values: 相关系数值
            threshold: 显著性阈值
            max_order: 最大阶数
            
        Returns:
            Optional[int]: 截断点位置
        """
        for i in range(min(len(values), max_order)):
            if abs(values[i]) < threshold:
                # 检查后续几个值是否也不显著
                if i < len(values) - 2:
                    if all(abs(values[j]) < threshold for j in range(i, min(i+3, len(values)))):
                        return i + 1  # 返回1-based索引
                else:
                    return i + 1
        return None
    
    def test_stationarity(self, data: pd.Series) -> Dict:
        """
        检验时序数据的平稳性
        
        Args:
            data: 时序数据
            
        Returns:
            Dict: 平稳性检验结果
        """
        results = {}
        
        # ADF检验
        try:
            adf_result = adfuller(data.dropna())
            results['adf'] = {
                'statistic': adf_result[0],
                'p_value': adf_result[1],
                'critical_values': adf_result[4],
                'is_stationary': adf_result[1] < 0.05,
                'interpretation': '平稳' if adf_result[1] < 0.05 else '非平稳'
            }
        except Exception as e:
            results['adf'] = {'error': str(e)}
        
        # KPSS检验
        try:
            kpss_result = kpss(data.dropna())
            results['kpss'] = {
                'statistic': kpss_result[0],
                'p_value': kpss_result[1],
                'critical_values': kpss_result[3],
                'is_stationary': kpss_result[1] > 0.05,
                'interpretation': '平稳' if kpss_result[1] > 0.05 else '非平稳'
            }
        except Exception as e:
            results['kpss'] = {'error': str(e)}
        
        return results
    
    def ljung_box_test(self, data: pd.Series, lags: int = 10) -> Dict:
        """
        Ljung-Box白噪声检验
        
        Args:
            data: 时序数据
            lags: 检验的滞后阶数
            
        Returns:
            Dict: 检验结果
        """
        try:
            result = acorr_ljungbox(data.dropna(), lags=lags, return_df=True)
            
            return {
                'statistics': result['lb_stat'].values,
                'p_values': result['lb_pvalue'].values,
                'lags': np.arange(1, lags + 1),
                'is_white_noise': all(result['lb_pvalue'] > 0.05),
                'interpretation': '白噪声' if all(result['lb_pvalue'] > 0.05) else '非白噪声'
            }
        except Exception as e:
            return {'error': str(e)}
