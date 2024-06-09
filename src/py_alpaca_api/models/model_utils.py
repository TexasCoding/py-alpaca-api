from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

import pendulum


def get_dict_str_value(data_dict: dict, key: str) -> str:
    """
    Returns the string value of a specific key within a dictionary.

    Args:
        data_dict (dict): The dictionary containing the data.
        key (str): The key to retrieve the value from.

    Returns:
        str: The string value associated with the specified key. If the key does not exist in the dictionary or
        its value is None, an empty string will be returned.
    """
    return str(data_dict[key]) if data_dict.get(key) else ""


def parse_date(data_dict: dict, key: str) -> datetime:
    """
    Parses a date value from a dictionary using a specified key.

    Args:
        data_dict (dict): The dictionary from which to extract the date value.
        key (str): The key in the dictionary representing the date value.

    Returns:
        datetime: The parsed date value as a `datetime` object.

    """
    return (
        pendulum.parse(data_dict[key], tz="America/New_York").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        if data_dict.get(key)
        else pendulum.DateTime.min.strftime("%Y-%m-%d")
    )


def get_dict_float_value(data_dict: dict, key: str) -> float:
    """
    Args:
        data_dict (dict): A dictionary containing the data.
        key (str): The key to look for in the data_dict.

    Returns:
        float: The value associated with the specified key in the data_dict as a float. If the key is not found or
        if the value is not of float type, returns 0.0.
    """
    return float(data_dict.get(key, 0.0)) if data_dict.get(key) else 0.0


def get_dict_int_value(data_dict: dict, key: str) -> int:
    """
    Args:
        data_dict: A dictionary containing key-value pairs.
        key: The key whose corresponding value is to be returned.

    Returns:
        int: The integer value associated with the given key in the data_dict. If the key is not present or
        the corresponding value is not an integer, 0 is returned.
    """
    return int(data_dict.get(key, 0)) if data_dict.get(key) else 0


KEY_PROCESSORS = {
    int: get_dict_int_value,
    str: get_dict_str_value,
    float: get_dict_float_value,
    datetime: parse_date,
    bool: lambda data_dict, key: bool(data_dict[key]),
    List[object]: lambda data_dict, key: (data_dict[key] if data_dict.get(key) else []),
}


############################################
# Data Class Extraction Functions
############################################
def extract_class_data(data_dict: dict, field_processors: Dict, data_class: dataclass):
    """
    Extracts and processes data from a dictionary based on a given data class and field processors.

    Args:
        data_dict (dict): The dictionary containing the data to be processed.
        field_processors (Dict): A dictionary of field processors.
        data_class (dataclass): The data class used to define the fields and types.

    Returns:
        dict: A dictionary containing processed data, with keys corresponding to the fields of the data class.

    Raises:
        KeyError: When a field processor is not found for a specific data type.
    """
    if "class" in data_dict:
        data_dict["asset_class"] = data_dict["class"]
        del data_dict["class"]
    return {
        field: field_processors[data_type](data_dict, field)
        for field, data_type in data_class.__annotations__.items()
        if field_processors.get(data_type, None)
    }
