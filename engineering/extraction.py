"""
Extraction script
"""
from typing import Optional
import pandas as pd
from numpy import float32
from analysis import find_missing_values
from engineering.persistence_manager import PersistenceManager, DataType
from engineering.transformation import remove_product_prefix, \
    remove_dollar_prefix, remove_family_prefix

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 101)


def extract_raw_data(
        filename: str = 'Base_de_Ventas.xlsx',
        data_type: DataType = DataType.RAW, converter: Optional[dict] = None
) -> pd.DataFrame:
    """
    Engineering method to extract raw data from csv file
    :param filename: Filename to extract data from. The default is
     'drugs_train.csv'
    :type filename: str
    :param data_type: Path where data will be saved: RAW or
     PROCESSED. The default is RAW
    :type data_type: DataType
    :param converter: Dictionary with converter functions. The default
     is None
    :type converter: dict
    :return: Dataframe with raw data
    :rtype: pd.DataFrame
    """
    sales_types = {
        'Cliente - Territorio': str, 'SKU': str,
        'Cantidad facturada': float32, 'Bodega': str}
    parse_dates: list[str] = [
        'Fecha de Pedido', 'Fecha de Entrega']
    if not converter:
        converter: dict = {
            'Producto': remove_product_prefix,
            'Familia': remove_family_prefix,
            'PVP': remove_dollar_prefix}
    df_sales: pd.DataFrame = PersistenceManager.load_from_xlsx(
        filename=filename, sheet_name='Ventas', data_type=data_type,
        dtypes=sales_types, parse_dates=parse_dates)
    df_sales = df_sales.rename(columns={
        'Fecha de Pedido': 'Fecha_Pedido',
        'Fecha de Entrega': 'Fecha_Entrega',
        'Cantidad facturada': 'Cantidad_Facturada'})
    df_products: pd.DataFrame = PersistenceManager.load_from_xlsx(
        filename=filename, sheet_name='Producto', data_type=data_type,
        converter=converter)
    df_sales = find_missing_values(df_sales)
    df_products = find_missing_values(df_products)
    dataframe = df_sales.merge(
        df_products, left_on='SKU', right_on='Producto', how='left')
    print("dataframe")
    print(dataframe.columns)
    print(dataframe.head)
    return dataframe
