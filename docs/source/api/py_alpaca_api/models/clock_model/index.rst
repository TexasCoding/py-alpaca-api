py_alpaca_api.models.clock_model
================================

.. py:module:: py_alpaca_api.models.clock_model


Classes
-------

.. autoapisummary::

   py_alpaca_api.models.clock_model.ClockModel


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.clock_model.clock_class_from_dict


Module Contents
---------------

.. py:class:: ClockModel

   .. py:attribute:: market_time
      :type:  datetime.datetime


   .. py:attribute:: is_open
      :type:  bool


   .. py:attribute:: next_open
      :type:  datetime.datetime


   .. py:attribute:: next_close
      :type:  datetime.datetime


.. py:function:: clock_class_from_dict(data_dict: dict) -> ClockModel

   Create ClockModel from dictionary data.

   :param data_dict: A dictionary containing data for creating an instance of
                     `ClockModel`.

   :returns: An instance of `ClockModel` created using the data from `data_dict`.

   :raises None.:
