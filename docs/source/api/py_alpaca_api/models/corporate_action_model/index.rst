py_alpaca_api.models.corporate_action_model
===========================================

.. py:module:: py_alpaca_api.models.corporate_action_model


Classes
-------

.. autoapisummary::

   py_alpaca_api.models.corporate_action_model.CorporateActionModel
   py_alpaca_api.models.corporate_action_model.DividendModel
   py_alpaca_api.models.corporate_action_model.SplitModel
   py_alpaca_api.models.corporate_action_model.MergerModel
   py_alpaca_api.models.corporate_action_model.SpinoffModel


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.corporate_action_model.corporate_action_class_from_dict
   py_alpaca_api.models.corporate_action_model.extract_corporate_action_data


Module Contents
---------------

.. py:class:: CorporateActionModel

   Base model for corporate action announcements.


   .. py:attribute:: id
      :type:  str


   .. py:attribute:: corporate_action_id
      :type:  str


   .. py:attribute:: ca_type
      :type:  str


   .. py:attribute:: ca_sub_type
      :type:  str | None


   .. py:attribute:: initiating_symbol
      :type:  str | None


   .. py:attribute:: initiating_original_cusip
      :type:  str | None


   .. py:attribute:: target_symbol
      :type:  str | None


   .. py:attribute:: target_original_cusip
      :type:  str | None


   .. py:attribute:: declaration_date
      :type:  str | None


   .. py:attribute:: ex_date
      :type:  str | None


   .. py:attribute:: record_date
      :type:  str | None


   .. py:attribute:: payable_date
      :type:  str | None


   .. py:attribute:: cash
      :type:  float | None


   .. py:attribute:: old_rate
      :type:  float | None


   .. py:attribute:: new_rate
      :type:  float | None


.. py:class:: DividendModel

   Bases: :py:obj:`CorporateActionModel`


   Model for dividend corporate actions.


   .. py:attribute:: cash_amount
      :type:  float | None


   .. py:attribute:: dividend_type
      :type:  str | None


   .. py:attribute:: frequency
      :type:  int | None


.. py:class:: SplitModel

   Bases: :py:obj:`CorporateActionModel`


   Model for stock split corporate actions.


   .. py:attribute:: split_from
      :type:  float | None


   .. py:attribute:: split_to
      :type:  float | None


.. py:class:: MergerModel

   Bases: :py:obj:`CorporateActionModel`


   Model for merger corporate actions.


   .. py:attribute:: acquirer_symbol
      :type:  str | None


   .. py:attribute:: acquirer_cusip
      :type:  str | None


   .. py:attribute:: cash_rate
      :type:  float | None


   .. py:attribute:: stock_rate
      :type:  float | None


.. py:class:: SpinoffModel

   Bases: :py:obj:`CorporateActionModel`


   Model for spinoff corporate actions.


   .. py:attribute:: new_symbol
      :type:  str | None


   .. py:attribute:: new_cusip
      :type:  str | None


   .. py:attribute:: ratio
      :type:  float | None


.. py:function:: corporate_action_class_from_dict(data: dict[str, Any]) -> CorporateActionModel

   Create appropriate corporate action model from dictionary.

   :param data: Dictionary containing corporate action data

   :returns: CorporateActionModel or one of its subclasses based on ca_type


.. py:function:: extract_corporate_action_data(data: dict[str, Any]) -> dict[str, Any]

   Extract and transform corporate action data from API response.

   :param data: Raw API response data

   :returns: Transformed dictionary ready for model creation
