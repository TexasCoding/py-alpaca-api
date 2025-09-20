py_alpaca_api.models.asset_model
================================

.. py:module:: py_alpaca_api.models.asset_model


Classes
-------

.. autoapisummary::

   py_alpaca_api.models.asset_model.AssetModel


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.asset_model.asset_class_from_dict


Module Contents
---------------

.. py:class:: AssetModel

   .. py:attribute:: id
      :type:  str


   .. py:attribute:: asset_class
      :type:  str


   .. py:attribute:: easy_to_borrow
      :type:  bool


   .. py:attribute:: exchange
      :type:  str


   .. py:attribute:: fractionable
      :type:  bool


   .. py:attribute:: maintenance_margin_requirement
      :type:  float


   .. py:attribute:: marginable
      :type:  bool


   .. py:attribute:: name
      :type:  str


   .. py:attribute:: shortable
      :type:  bool


   .. py:attribute:: status
      :type:  str


   .. py:attribute:: symbol
      :type:  str


   .. py:attribute:: tradable
      :type:  bool


.. py:function:: asset_class_from_dict(data_dict: dict) -> AssetModel

   Create AssetModel from dictionary data.

   :param data_dict: A dictionary containing the data for creating an instance of
                     AssetModel.

   :returns: An instance of the AssetModel class.

   :raises None:
