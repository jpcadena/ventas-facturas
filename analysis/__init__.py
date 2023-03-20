"""
Analysis package initialization
"""
import logging
import pandas as pd
from analysis.analysis import analyze_dataframe, find_missing_values
from analysis.visualization import plot_count, plot_distribution, \
    boxplot_dist, plot_scatter, plot_heatmap

logger: logging.Logger = logging.getLogger(__name__)


def numerical_eda(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    EDA based on numerical values for dataset
    :param dataframe: Dataframe to analyze
    :type dataframe: pd.DataFrame
    :return: The dataframe without missing values
    :rtype: pd.DataFrame
    """
    logger.info("Running Exploratory Data Analysis")
    analyze_dataframe(dataframe)
    # dataframe = find_missing_values(dataframe)
    return dataframe


def visualize_data(dataframe: pd.DataFrame) -> None:
    """
    Basic visualization of the dataframe
    :param dataframe: Dataframe to visualize
    :type dataframe: pd.DataFrame
    :return: None
    :rtype: NoneType
    """
    logger.info("Running visualization")
    plot_heatmap(dataframe)
    plot_scatter(dataframe, 'Monto_Facturado $', 'ID_Territorio', 'ID_Cliente')
    plot_distribution(dataframe['ID_Cliente'], 'lightskyblue')
    plot_distribution(dataframe['ID_Territorio'], 'palegreen')
    plot_distribution(dataframe['ID_Bodega'], 'coral')
    plot_count(
        dataframe, ['Cantidad_Facturada', 'Monto_Facturado $'],
        'ID_Territorio')
    plot_distribution(dataframe['ID_SKU'], 'palegreen')
    boxplot_dist(dataframe, 'Monto_Facturado $', 'ID_Territorio')
    boxplot_dist(dataframe, 'Monto_Facturado $', 'Familia_SKU')
    # plot_distribution(dataframe['Familia_SKU'], 'lightskyblue')
