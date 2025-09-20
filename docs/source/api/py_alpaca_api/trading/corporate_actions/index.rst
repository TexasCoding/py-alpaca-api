py_alpaca_api.trading.corporate_actions
=======================================

.. py:module:: py_alpaca_api.trading.corporate_actions


Classes
-------

.. autoapisummary::

   py_alpaca_api.trading.corporate_actions.CorporateActions


Module Contents
---------------

.. py:class:: CorporateActions(headers: dict[str, str], base_url: str)

   .. py:attribute:: headers


   .. py:attribute:: base_url


   .. py:method:: get_announcements(since: str, until: str, ca_types: list[str], symbol: str | None = None, cusip: str | None = None, date_type: Literal['declaration_date', 'ex_date', 'record_date', 'payable_date'] | None = None, page_limit: int = 100, page_token: str | None = None) -> list[py_alpaca_api.models.corporate_action_model.CorporateActionModel]

      Retrieve corporate action announcements.

      :param since: The start (inclusive) of the date range in YYYY-MM-DD format.
                    Date range is limited to 90 days.
      :param until: The end (inclusive) of the date range in YYYY-MM-DD format.
                    Date range is limited to 90 days.
      :param ca_types: List of corporate action types to return.
                       Valid types: dividend, merger, spinoff, split
      :param symbol: Optional filter by symbol
      :param cusip: Optional filter by CUSIP
      :param date_type: Optional date type for filtering (declaration_date, ex_date, record_date, payable_date)
      :param page_limit: Number of results per page (Note: API may return all results regardless)
      :param page_token: Token for pagination (currently not used by API)

      :returns: List of CorporateActionModel objects

      :raises ValidationError: If date range exceeds 90 days or invalid parameters
      :raises APIRequestError: If the API request fails



   .. py:method:: get_announcement_by_id(announcement_id: str) -> py_alpaca_api.models.corporate_action_model.CorporateActionModel

      Retrieve a specific corporate action announcement by ID.

      :param announcement_id: The unique ID of the announcement

      :returns: CorporateActionModel object

      :raises APIRequestError: If the API request fails or announcement not found



   .. py:method:: get_all_announcements(since: str, until: str, ca_types: list[str], symbol: str | None = None, cusip: str | None = None, date_type: Literal['declaration_date', 'ex_date', 'record_date', 'payable_date'] | None = None) -> list[py_alpaca_api.models.corporate_action_model.CorporateActionModel]

      Retrieve all corporate action announcements.

      Note: The API currently returns all results within the date range
      without pagination, so this method simply calls get_announcements.

      :param since: The start (inclusive) of the date range in YYYY-MM-DD format.
      :param until: The end (inclusive) of the date range in YYYY-MM-DD format.
      :param ca_types: List of corporate action types to return.
      :param symbol: Optional filter by symbol
      :param cusip: Optional filter by CUSIP
      :param date_type: Optional date type for filtering

      :returns: List of all CorporateActionModel objects

      :raises ValidationError: If date range exceeds 90 days or invalid parameters
      :raises APIRequestError: If the API request fails
