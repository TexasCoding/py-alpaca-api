py_alpaca_api.models.order_model
================================

.. py:module:: py_alpaca_api.models.order_model


Classes
-------

.. autoapisummary::

   py_alpaca_api.models.order_model.OrderModel


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.order_model.process_legs
   py_alpaca_api.models.order_model.order_class_from_dict


Module Contents
---------------

.. py:class:: OrderModel

   .. py:attribute:: id
      :type:  str


   .. py:attribute:: client_order_id
      :type:  str


   .. py:attribute:: created_at
      :type:  datetime.datetime


   .. py:attribute:: updated_at
      :type:  datetime.datetime


   .. py:attribute:: submitted_at
      :type:  datetime.datetime


   .. py:attribute:: filled_at
      :type:  datetime.datetime


   .. py:attribute:: expired_at
      :type:  datetime.datetime


   .. py:attribute:: canceled_at
      :type:  datetime.datetime


   .. py:attribute:: failed_at
      :type:  datetime.datetime


   .. py:attribute:: replaced_at
      :type:  datetime.datetime


   .. py:attribute:: replaced_by
      :type:  str


   .. py:attribute:: replaces
      :type:  str


   .. py:attribute:: asset_id
      :type:  str


   .. py:attribute:: symbol
      :type:  str


   .. py:attribute:: asset_class
      :type:  str


   .. py:attribute:: notional
      :type:  float


   .. py:attribute:: qty
      :type:  float


   .. py:attribute:: filled_qty
      :type:  float


   .. py:attribute:: filled_avg_price
      :type:  float


   .. py:attribute:: order_class
      :type:  str


   .. py:attribute:: order_type
      :type:  str


   .. py:attribute:: type
      :type:  str


   .. py:attribute:: side
      :type:  str


   .. py:attribute:: time_in_force
      :type:  str


   .. py:attribute:: limit_price
      :type:  float


   .. py:attribute:: stop_price
      :type:  float


   .. py:attribute:: status
      :type:  str


   .. py:attribute:: extended_hours
      :type:  bool


   .. py:attribute:: legs
      :type:  list[object]


   .. py:attribute:: trail_percent
      :type:  float


   .. py:attribute:: trail_price
      :type:  float


   .. py:attribute:: hwm
      :type:  float


   .. py:attribute:: subtag
      :type:  str


   .. py:attribute:: source
      :type:  str


.. py:function:: process_legs(legs: list[dict]) -> list[OrderModel]

   Process the legs and create a list of OrderModel objects based on the provided data.

   :param legs: A list of dictionaries representing the legs.
   :type legs: List[Dict]

   :returns: A list of OrderModel objects generated from the leg data.
   :rtype: List[OrderModel]

   .. note:: If the legs parameter is empty, an empty list will be returned.


.. py:function:: order_class_from_dict(data_dict: dict) -> OrderModel

   Creates an instance of `OrderModel` using the provided dictionary data.

   :param data_dict: A dictionary containing the data used to create the `OrderModel` instance.
   :type data_dict: Dict

   :returns: An instance of `OrderModel` created using the provided data.
   :rtype: OrderModel

   :raises None:
