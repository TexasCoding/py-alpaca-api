# # pytest
# import json
# from unittest.mock import patch

# import pandas as pd

# from py_alpaca_api.src.account import Account

# mocked_activities = [
#     {
#         "id": "20240524144325589::2f303c1e-277b-4de1-bc9c-2f0c62330138",
#         "activity_type": "FILL",
#         "transaction_time": "2021-05-24T18:43:25.58947Z",
#         "type": "fill",
#         "price": "46.412",
#         "qty": "0.459411125",
#         "side": "sell",
#         "symbol": "KOLD",
#         "leaves_qty": "0",
#         "order_id": "8ceb3115-b234-47c8-8c22-bed3f787e537",
#         "cum_qty": "0.459411125",
#         "order_status": "filled",
#     },
# ]


# def test_account_activity_both_dates():
#     with patch("requests.get") as mocked_get:
#         mocked_account = Account("trade_url", {"header": "header"})
#         mocked_get.return_value.status_code = 200
#         mocked_get.return_value.text = json.dumps(mocked_activities)

#         try:
#             mocked_account.activity("FILL", "2021-10-16", "2021-10-18")
#             assert False, "Expected an Exception"
#         except ValueError as err:
#             assert str(err) == "One of the Date and Until Date are required, not both or neither."


# def test_account_activity_no_dates():
#     with patch("requests.get") as mocked_get:
#         mocked_account = Account("trade_url", {"header": "header"})
#         mocked_get.return_value.status_code = 200
#         mocked_get.return_value.text = json.dumps(mocked_activities)

#         try:
#             mocked_account.activity("FILL")
#             assert False, "Expected an Exception"
#         except ValueError as err:
#             assert str(err) == "One of the Date and Until Date are required, not both or neither."


# def test_account_activity_no_activity_type():
#     with patch("requests.get") as mocked_get:
#         mocked_account = Account("trade_url", {"header": "header"})
#         mocked_get.return_value.status_code = 200
#         mocked_get.return_value.text = json.dumps(mocked_activities)

#         try:
#             mocked_account.activity("", "2021-10-16")
#             assert False, "Expected an Exception"
#         except ValueError as err:
#             assert str(err) == "Activity type is required."


# def test_account_activity_valid_activities_with_dates():
#     with patch("requests.get") as mocked_get:
#         mocked_account = Account("trade_url", {"header": "header"})
#         mocked_get.return_value.status_code = 200
#         mocked_get.return_value.text = json.dumps(mocked_activities)

#         transactions = mocked_account.activity("FILL", "2021-10-17")
#         assert isinstance(transactions, pd.DataFrame)
#         assert not transactions.empty


# def test_account_activity_valid_activities_without_dates():
#     with patch("requests.get") as mocked_get:
#         mocked_account = Account("trade_url", {"header": "header"})
#         mocked_get.return_value.status_code = 200
#         mocked_get.return_value.text = json.dumps(mocked_activities)
#         transactions = mocked_account.activity("FILL", until_date="2021-10-18")
#         assert isinstance(transactions, pd.DataFrame)
#         assert not transactions.empty


# def test_account_activity_error_response():
#     with patch("requests.get") as mocked_get:
#         mocked_account = Account("trade_url", {"header": "header"})
#         mocked_get.return_value.status_code = 404
#         mocked_get.return_value.text = json.dumps(mocked_activities)

#         try:
#             mocked_account.activity("FILL", "2021-10-16")
#             assert False, "Expected an Exception"
#         except Exception as err:
#             assert str(err) == "Failed to get account activities. Response: " + mocked_get.return_value.text
