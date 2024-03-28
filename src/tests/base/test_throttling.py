import sys
from unittest.mock import patch

import pytest

from src.base.throttling import (
    ScopedOnePerThreeSecsThrottle,
)


@pytest.mark.parametrize(
    "sys_argv, expected_rate",
    [
        (["pytest"], (100, 1)),
        (
            ["python", "some_script.py"],
            (1, 3),
        ),
    ],
)
def test_parse_rate(sys_argv, expected_rate):
    with patch.object(sys, "argv", sys_argv):
        throttle = ScopedOnePerThreeSecsThrottle()
        rate = throttle.parse_rate(throttle.rate)
        assert (
            rate == expected_rate
        ), f"Rate should be {expected_rate} when sys.argv is {sys_argv}"
