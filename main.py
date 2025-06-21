"""
时序数据分析与可视化工具

主应用程序入口
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os
import plotly.graph_objects as go

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_processing import DataLoader, TimeSeriesPreprocessor
from analysis import ACFPACFAnalyzer
from visualization import TimeSeriesPlotter
from utils import validate_time_series, format_data


def main():
    """主函数"""
    st.set_page_config(
        page_title="时序数据分析与可视化工具",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📈 时序数据分析与可视化工具")
    st.markdown("---")

    # 初始化组件
    data_loader = DataLoader()
    preprocessor = TimeSeriesPreprocessor()
    analyzer = ACFPACFAnalyzer()
    plotter = TimeSeriesPlotter()

    # 侧边栏
    st.sidebar.title("功能选择")

    # 主要功能选项
    main_option = st.sidebar.selectbox(
        "选择主要功能",
        ["数据导入与预处理", "ACF/PACF分析", "数据可视化", "模型建议"]
    )

    # 数据存储在session state中
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None

    # 根据选择的功能显示相应界面
    if main_option == "数据导入与预处理":
        show_data_import_page(data_loader, preprocessor)
    elif main_option == "ACF/PACF分析":
        show_acf_pacf_analysis_page(analyzer, plotter)
    elif main_option == "数据可视化":
        show_visualization_page(plotter)
    elif main_option == "模型建议":
        show_model_suggestion_page(analyzer)


def show_data_import_page(data_loader, preprocessor):
    """显示数据导入与预处理页面"""
    st.header("📊 数据导入与预处理")

    # 数据导入选项
    import_option = st.radio(
        "选择数据来源",
        ["上传文件", "使用示例数据"]
    )

    if import_option == "上传文件":
        uploaded_file = st.file_uploader(
            "选择时序数据文件",
            type=['csv', 'xlsx', 'xls', 'txt'],
            help="支持CSV、Excel和TXT格式文件"
        )

        if uploaded_file is not None:
            try:
                # 加载数据
                df = data_loader.load_from_uploaded_file(uploaded_file)
                st.success("文件上传成功！")

                # 显示数据预览
                st.subheader("数据预览")
                st.dataframe(df.head(10))

                # 列选择
                st.subheader("列选择")
                col1, col2 = st.columns(2)

                with col1:
                    date_column = st.selectbox("选择日期列", df.columns)
                with col2:
                    value_column = st.selectbox("选择数值列", df.columns)

                # 验证数据
                if data_loader.validate_time_series_data(df, date_column, value_column):
                    st.success("数据格式验证通过！")

                    # 清洗数据
                    cleaned_df = preprocessor.clean_data(df, date_column, value_column)
                    st.session_state.data = format_data(cleaned_df, date_column, value_column)

                    # 显示数据统计
                    show_data_statistics(preprocessor, st.session_state.data)

                else:
                    st.error("数据格式验证失败，请检查日期列和数值列的格式。")

            except Exception as e:
                st.error(f"文件加载失败: {str(e)}")

    else:  # 使用示例数据
        st.subheader("示例数据配置")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            n_points = st.slider("数据点数量", 50, 500, 200)
        with col2:
            trend = st.checkbox("包含趋势", True)
        with col3:
            seasonality = st.checkbox("包含季节性", True)
        with col4:
            noise_level = st.slider("噪声水平", 0.0, 1.0, 0.1)

        if st.button("生成示例数据"):
            df = data_loader.create_sample_data(n_points, trend, seasonality, noise_level)
            st.session_state.data = df
            st.success("示例数据生成成功！")

            # 显示数据预览
            st.subheader("数据预览")
            st.dataframe(df.head(10))

            # 显示数据统计
            show_data_statistics(preprocessor, df)

    # 数据预处理选项
    if st.session_state.data is not None:
        st.markdown("---")
        st.subheader("🔧 数据预处理")

        preprocessing_options = st.multiselect(
            "选择预处理操作",
            ["处理缺失值", "移除异常值", "差分", "对数变换", "标准化"]
        )

        processed_data = st.session_state.data.copy()

        for option in preprocessing_options:
            if option == "处理缺失值":
                method = st.selectbox(
                    "缺失值处理方法",
                    ["interpolate", "forward_fill", "backward_fill", "mean", "drop"]
                )
                processed_data = preprocessor.handle_missing_values(processed_data, 'value', method)

            elif option == "移除异常值":
                method = st.selectbox("异常值检测方法", ["iqr", "zscore"])
                threshold = st.slider("阈值", 1.0, 3.0, 1.5)
                processed_data = preprocessor.remove_outliers(processed_data, 'value', method, threshold)

            elif option == "差分":
                periods = st.slider("差分阶数", 1, 5, 1)
                processed_data = preprocessor.difference_series(processed_data, 'value', periods)

            elif option == "对数变换":
                processed_data = preprocessor.log_transform(processed_data, 'value')

            elif option == "标准化":
                processed_data = preprocessor.standardize(processed_data, 'value')

        if preprocessing_options:
            st.session_state.processed_data = processed_data
            st.success("数据预处理完成！")

            # 显示处理后的数据预览
            st.subheader("处理后数据预览")
            st.dataframe(processed_data.head(10))


def show_data_statistics(preprocessor, data):
    """显示数据统计信息"""
    st.subheader("📈 数据统计")

    stats = preprocessor.get_data_summary(data, 'value')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("数据点数量", f"{stats['数据点数量']:,}")
        st.metric("缺失值数量", f"{stats['缺失值数量']:,}")

    with col2:
        st.metric("均值", f"{stats['均值']:.4f}")
        st.metric("标准差", f"{stats['标准差']:.4f}")

    with col3:
        st.metric("最小值", f"{stats['最小值']:.4f}")
        st.metric("最大值", f"{stats['最大值']:.4f}")

    with col4:
        st.metric("中位数", f"{stats['中位数']:.4f}")
        st.metric("偏度", f"{stats['偏度']:.4f}")


def show_acf_pacf_analysis_page(analyzer, plotter):
    """显示ACF/PACF分析页面"""
    st.header("🔍 ACF/PACF分析")

    if st.session_state.data is None:
        st.warning("请先导入数据！")
        return

    # 选择要分析的数据
    data_option = st.radio(
        "选择分析数据",
        ["原始数据", "预处理后数据"] if st.session_state.processed_data is not None else ["原始数据"]
    )

    if data_option == "原始数据":
        analysis_data = st.session_state.data['value']
    else:
        analysis_data = st.session_state.processed_data['value']

    # 分析参数设置
    st.subheader("分析参数")
    col1, col2 = st.columns(2)

    with col1:
        nlags = st.slider("滞后阶数", 5, 50, 20)
    with col2:
        alpha = st.selectbox("置信水平", [0.01, 0.05, 0.10], index=1)

    if st.button("开始分析"):
        try:
            # 计算ACF和PACF
            acf_result = analyzer.calculate_acf(analysis_data, nlags, alpha)
            pacf_result = analyzer.calculate_pacf(analysis_data, nlags, alpha)

            # 显示结果
            st.subheader("分析结果")

            # 绘制ACF/PACF图
            fig = plotter.plot_acf_pacf_combined(acf_result, pacf_result)
            st.plotly_chart(fig, use_container_width=True)

            # 模型建议
            suggestions = analyzer.suggest_arima_order(acf_result, pacf_result)

            st.subheader("模型建议")
            for i, suggestion in enumerate(suggestions['suggestions']):
                st.info(f"**{suggestion['model']}模型**: {suggestion['explanation']}")

            # 平稳性检验
            st.subheader("平稳性检验")
            stationarity_results = analyzer.test_stationarity(analysis_data)

            col1, col2 = st.columns(2)

            with col1:
                if 'adf' in stationarity_results and 'error' not in stationarity_results['adf']:
                    adf = stationarity_results['adf']
                    st.write("**ADF检验结果:**")
                    st.write(f"- 检验统计量: {adf['statistic']:.4f}")
                    st.write(f"- p值: {adf['p_value']:.4f}")
                    st.write(f"- 结论: {adf['interpretation']}")

            with col2:
                if 'kpss' in stationarity_results and 'error' not in stationarity_results['kpss']:
                    kpss = stationarity_results['kpss']
                    st.write("**KPSS检验结果:**")
                    st.write(f"- 检验统计量: {kpss['statistic']:.4f}")
                    st.write(f"- p值: {kpss['p_value']:.4f}")
                    st.write(f"- 结论: {kpss['interpretation']}")

        except Exception as e:
            st.error(f"分析失败: {str(e)}")


def show_visualization_page(plotter):
    """显示数据可视化页面"""
    st.header("📊 数据可视化")

    if st.session_state.data is None:
        st.warning("请先导入数据！")
        return

    # 可视化选项
    viz_option = st.selectbox(
        "选择可视化类型",
        ["时序图", "数据分布"]
    )

    if viz_option == "时序图":
        st.subheader("时序数据图")

        # 选择要显示的数据
        data_to_plot = st.session_state.data

        if st.session_state.processed_data is not None:
            show_processed = st.checkbox("同时显示预处理后数据")
            if show_processed:
                # 创建组合图
                fig = plotter.plot_time_series(data_to_plot, title="原始数据")
                fig.add_trace(go.Scatter(
                    x=st.session_state.processed_data['date'],
                    y=st.session_state.processed_data['value'],
                    mode='lines',
                    name='预处理后数据',
                    line=dict(color='orange', width=2)
                ))
            else:
                fig = plotter.plot_time_series(data_to_plot)
        else:
            fig = plotter.plot_time_series(data_to_plot)

        st.plotly_chart(fig, use_container_width=True)

    elif viz_option == "数据分布":
        st.subheader("数据分布图")

        data_to_analyze = st.session_state.data['value']
        fig = plotter.plot_data_distribution(data_to_analyze)
        st.plotly_chart(fig, use_container_width=True)


def show_model_suggestion_page(analyzer):
    """显示模型建议页面"""
    st.header("🤖 模型建议")

    if st.session_state.data is None:
        st.warning("请先导入数据！")
        return

    st.info("基于ACF/PACF分析结果，系统将为您推荐合适的时序模型。")

    # 选择分析数据
    data_option = st.radio(
        "选择分析数据",
        ["原始数据", "预处理后数据"] if st.session_state.processed_data is not None else ["原始数据"]
    )

    if data_option == "原始数据":
        analysis_data = st.session_state.data['value']
    else:
        analysis_data = st.session_state.processed_data['value']

    if st.button("生成模型建议"):
        try:
            # 计算ACF和PACF
            acf_result = analyzer.calculate_acf(analysis_data, nlags=20)
            pacf_result = analyzer.calculate_pacf(analysis_data, nlags=20)

            # 获取模型建议
            suggestions = analyzer.suggest_arima_order(acf_result, pacf_result)

            st.subheader("推荐模型")

            for i, suggestion in enumerate(suggestions['suggestions'], 1):
                with st.expander(f"建议 {i}: {suggestion['model']}模型"):
                    st.write(f"**模型阶数**: {suggestion['order']}")
                    st.write(f"**说明**: {suggestion['explanation']}")

                    # 显示模型特点
                    if suggestion['model'] == 'AR':
                        st.write("**AR模型特点**:")
                        st.write("- 适用于具有自回归特性的时序数据")
                        st.write("- 当前值依赖于过去的值")
                        st.write("- PACF图显示截断特征")
                    elif suggestion['model'] == 'MA':
                        st.write("**MA模型特点**:")
                        st.write("- 适用于具有移动平均特性的时序数据")
                        st.write("- 当前值依赖于过去的误差项")
                        st.write("- ACF图显示截断特征")
                    elif suggestion['model'] == 'ARMA':
                        st.write("**ARMA模型特点**:")
                        st.write("- 结合了AR和MA模型的特点")
                        st.write("- 适用于复杂的时序数据")
                        st.write("- ACF和PACF都呈现拖尾特征")

            # 显示诊断信息
            st.subheader("诊断信息")
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**ACF截断点**: {suggestions.get('acf_cutoff', '无明显截断')}")
                st.write(f"**PACF截断点**: {suggestions.get('pacf_cutoff', '无明显截断')}")

            with col2:
                st.write(f"**显著性阈值**: ±{suggestions.get('threshold', 0):.4f}")
                st.write("**建议**: 可以尝试多个模型并比较其性能")

        except Exception as e:
            st.error(f"模型建议生成失败: {str(e)}")


if __name__ == "__main__":
    main()
