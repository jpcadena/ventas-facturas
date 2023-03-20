"""
Transformation script
"""
import pandas as pd
from numpy import uint8

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 101)


def remove_product_prefix(value: str) -> str:
    """
    Removes the 'Producto' prefix
    :param value: The cell value
    :type value: str
    :return: The new product cell value
    :rtype: str
    """
    return value.replace('Producto ', '')


def remove_family_prefix(value: str) -> str:
    """
    Removes the 'Familia ' prefix
    :param value: The cell value
    :type value: str
    :return: The new family cell value
    :rtype: str
    """
    return value.replace('Familia ', '')


def remove_dollar_prefix(value: str) -> str:
    """
    Removes the '$' prefix
    :param value: The cell value
    :type value: str
    :return: The new pvp cell value
    :rtype: str
    """
    return value.replace('$', '')


def feature_engineering(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Performs a feature engineering by generating new columns
    :param dataframe: The dataframe to transform
    :type dataframe: pd.DataFrame
    :return: The new dataframe
    :rtype: pd.DataFrame
    """
    dataframe['ID_Cliente'] = dataframe[
        'Cliente - Territorio'].str.split(' ').str[1]
    dataframe['ID_Territorio'] = dataframe[
        'Cliente - Territorio'].str.split(' ').str[-1].astype(uint8)
    dataframe['Monto_Facturado $'] = dataframe[
                                         'Cantidad_Facturada'] * dataframe[
        'PVP']
    dataframe['ID_Bodega'] = dataframe['Bodega'].str.split('-').str[-1]
    dataframe = dataframe.rename(columns={
        'SKU': 'ID_SKU',
        'Familia': 'Familia_SKU'})
    return dataframe


def filter_desired_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Filter the dataframe by desired columns
    :param dataframe: The dataframe to filter
    :type dataframe: pd.DataFrame
    :return: The filtered dataframe
    :rtype: pd.DataFrame
    """
    return dataframe[
        ['ID_Cliente', 'ID_Territorio', 'ID_Bodega', 'ID_SKU', 'Familia_SKU',
         'Cantidad_Facturada', 'Monto_Facturado $', 'Fecha_Pedido',
         'Fecha_Entrega']]
