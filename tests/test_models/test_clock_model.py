from datetime import datetime
from py_alpaca_api.models.clock_model import ClockModel, clock_class_from_dict
import pendulum


def test_clock_class_from_dict():
    data_dict = {
        "market_time": "2022-01-01T10:00:00Z",
        "is_open": True,
        "next_open": "2022-01-01T12:00:00Z",
        "next_close": "2022-01-01T16:00:00Z",
    }
    expected_clock = ClockModel(
        market_time=pendulum.DateTime(
            2022, 1, 1, 10, 0, 0, tzinfo=pendulum.Timezone("UTC")
        ),
        is_open=True,
        next_open=datetime(2022, 1, 1, 12, 0, 0, tzinfo=pendulum.Timezone("UTC")),
        next_close=datetime(2022, 1, 1, 16, 0, 0, tzinfo=pendulum.Timezone("UTC")),
    )
    assert clock_class_from_dict(data_dict) == expected_clock
