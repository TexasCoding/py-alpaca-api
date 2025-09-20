py_alpaca_api.models.quote_model
================================

.. py:module:: py_alpaca_api.models.quote_model


Classes
-------

.. autoapisummary::

   py_alpaca_api.models.quote_model.QuoteModel


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.quote_model.quote_class_from_dict


Module Contents
---------------

.. py:class:: QuoteModel

   .. py:attribute:: symbol
      :type:  str


   .. py:attribute:: timestamp
      :type:  datetime.datetime


   .. py:attribute:: ask
      :type:  float


   .. py:attribute:: ask_size
      :type:  int


   .. py:attribute:: bid
      :type:  float


   .. py:attribute:: bid_size
      :type:  int


.. py:function:: quote_class_from_dict(data_dict: dict) -> QuoteModel

   :param data_dict: A dictionary containing data for creating an instance of `QuoteModel`.

   :returns: An instance of `QuoteModel` created using the data from `data_dict`.

   :raises None.:
