"""
Persistence script
"""
import logging
from enum import Enum
from typing import Union, Optional
import pandas as pd
from core.config import ENCODING, NUMERICS

logger: logging.Logger = logging.getLogger(__name__)


class DataType(Enum):
    """
    Data Type class based on Enum
    """
    RAW: str = 'data/raw/'
    PROCESSED: str = 'data/processed/'
    FIGURES: str = 'reports/figures/'


class PersistenceManager:
    """
    Persistence Manager class
    """

    @staticmethod
    def save_to_csv(
            data: Union[list[dict], pd.DataFrame],
            data_type: DataType = DataType.PROCESSED, filename: str = 'data'
    ) -> bool:
        """
        Save list of dictionaries as csv file
        :param data: list of tweets as dictionaries
        :type data: list[dict]
        :param data_type: folder where data will be saved
        :type data_type: DataType
        :param filename: name of the file
        :type filename: str
        :return: confirmation for csv file created
        :rtype: bool
        """
        dataframe: pd.DataFrame
        if isinstance(data, pd.DataFrame):
            dataframe = data
        else:
            if not data:
                return False
            dataframe = pd.DataFrame(data)
        dataframe.to_csv(f'{str(data_type.value)}{filename}.csv', index=False,
                         encoding=ENCODING)
        return True

    @staticmethod
    def load_from_xlsx(
            filename: str, sheet_name: str, data_type: DataType,
            dtypes: Optional[dict] = None, converter: Optional[dict] = None,
            parse_dates: Optional[list[str]] = None
    ) -> pd.DataFrame:
        """
        Load dataframe from XLSX using chunk scheme
        :param filename: name of the file
        :type filename: str
        :param sheet_name: Name of the sheet to load
        :type sheet_name: str
        :param data_type: Path where data will be saved
        :type data_type: DataType
        :param dtypes: Dictionary of columns and datatypes
        :type dtypes: dict
        :param converter: Dictionary with converter functions
        :type converter: dict
        :param parse_dates: List of date columns to parse
        :type parse_dates: list[str]
        :return: dataframe retrieved from XLSX after optimization with chunks
        :rtype: pd.DataFrame
        """
        filepath: str = f'{data_type.value}{filename}'
        dataframe: pd.DataFrame = pd.read_excel(
            filepath, sheet_name=sheet_name,
            converters=converter, parse_dates=parse_dates)
        if dtypes:
            for key, value in dtypes.items():
                if value in NUMERICS:
                    dataframe[key] = pd.to_numeric(
                        dataframe[key], errors='coerce')
                    dataframe[key] = dataframe[key].astype(value)
                else:
                    dataframe[key] = dataframe[key].astype(value)
        return dataframe

    @staticmethod
    def save_to_pickle(
            dataframe: pd.DataFrame, filename: str = 'optimized_df.pkl'
    ) -> None:
        """
        Save dataframe to pickle file
        :param dataframe: dataframe
        :type dataframe: pd.DataFrame
        :param filename: name of the file
        :type filename: str
        :return: None
        :rtype: NoneType
        """
        dataframe.to_pickle(f'data/processed/{filename}')

    @staticmethod
    def load_from_pickle(filename: str = 'optimized_df.pkl') -> pd.DataFrame:
        """
        Load dataframe from Pickle file
        :param filename: name of the file to search and load
        :type filename: str
        :return: dataframe read from pickle
        :rtype: pd.DataFrame
        """
        dataframe: pd.DataFrame = pd.read_pickle(f'data/processed/{filename}')
        return dataframe
