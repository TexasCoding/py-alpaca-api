py_alpaca_api.models.account_activity_model
===========================================

.. py:module:: py_alpaca_api.models.account_activity_model


Classes
-------

.. autoapisummary::

   py_alpaca_api.models.account_activity_model.AccountActivityModel


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.account_activity_model.account_activity_class_from_dict


Module Contents
---------------

.. py:class:: AccountActivityModel

   .. py:attribute:: activity_type
      :type:  str


   .. py:attribute:: id
      :type:  str


   .. py:attribute:: cum_qty
      :type:  float


   .. py:attribute:: leaves_qty
      :type:  float


   .. py:attribute:: price
      :type:  float


   .. py:attribute:: qty
      :type:  float


   .. py:attribute:: side
      :type:  str


   .. py:attribute:: symbol
      :type:  str


   .. py:attribute:: transaction_time
      :type:  datetime.datetime


   .. py:attribute:: order_id
      :type:  str


   .. py:attribute:: type
      :type:  str


   .. py:attribute:: order_status
      :type:  str


   .. py:attribute:: date
      :type:  datetime.datetime


   .. py:attribute:: net_amount
      :type:  float


   .. py:attribute:: per_share_amount
      :type:  float


.. py:function:: account_activity_class_from_dict(data_dict: dict) -> AccountActivityModel

   Converts a dictionary into an instance of the `AccountActivityModel`.

   :param data_dict: A dictionary containing the data for creating an instance of AccountActivityModel.

   :returns: An instance of the AccountActivityModel class.

   :raises None:
