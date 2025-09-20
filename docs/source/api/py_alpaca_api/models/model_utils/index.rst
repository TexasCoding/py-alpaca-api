py_alpaca_api.models.model_utils
================================

.. py:module:: py_alpaca_api.models.model_utils


Attributes
----------

.. autoapisummary::

   py_alpaca_api.models.model_utils.KEY_PROCESSORS


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.model_utils.get_dict_str_value
   py_alpaca_api.models.model_utils.parse_date
   py_alpaca_api.models.model_utils.get_dict_float_value
   py_alpaca_api.models.model_utils.get_dict_int_value
   py_alpaca_api.models.model_utils.extract_class_data


Module Contents
---------------

.. py:function:: get_dict_str_value(data_dict: dict, key: str) -> str

   Returns the string value of a specific key within a dictionary.

   :param data_dict: The dictionary containing the data.
   :type data_dict: dict
   :param key: The key to retrieve the value from.
   :type key: str

   :returns: The string value associated with the specified key. If the key does not exist in the dictionary or
             its value is None, an empty string will be returned.
   :rtype: str


.. py:function:: parse_date(data_dict: dict, key: str) -> str

   Parses a date value from a dictionary using a specified key.

   :param data_dict: The dictionary from which to extract the date value.
   :type data_dict: dict
   :param key: The key in the dictionary representing the date value.
   :type key: str

   :returns: The parsed date value as a formatted string.
   :rtype: str


.. py:function:: get_dict_float_value(data_dict: dict, key: str) -> float

   :param data_dict: A dictionary containing the data.
   :type data_dict: dict
   :param key: The key to look for in the data_dict.
   :type key: str

   :returns: The value associated with the specified key in the data_dict as a float. If the key is not found or
             if the value is not of float type, returns 0.0.
   :rtype: float


.. py:function:: get_dict_int_value(data_dict: dict, key: str) -> int

   :param data_dict: A dictionary containing key-value pairs.
   :param key: The key whose corresponding value is to be returned.

   :returns: The integer value associated with the given key in the data_dict. If the key is not present or
             the corresponding value is not an integer, 0 is returned.
   :rtype: int


.. py:data:: KEY_PROCESSORS

.. py:function:: extract_class_data(data_dict: dict, field_processors: dict, data_class: type[Any])

   Extracts and processes data from a dictionary based on a given data class and field processors.

   :param data_dict: The dictionary containing the data to be processed.
   :type data_dict: dict
   :param field_processors: A dictionary of field processors.
   :type field_processors: Dict
   :param data_class: The data class used to define the fields and types.
   :type data_class: type[Any]

   :returns: A dictionary containing processed data, with keys corresponding to the fields of the data class.
   :rtype: dict

   :raises KeyError: When a field processor is not found for a specific data type.
