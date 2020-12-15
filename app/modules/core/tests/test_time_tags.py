from modules.core.templatetags import time_tags
import datetime


def test_format_time():
    assert time_tags.format_time(datetime.time(12, 0)) == "midday"
    assert time_tags.format_time(datetime.time(0, 0)) == "midnight"
    assert time_tags.format_time(datetime.time(15, 30)) == "3.30pm"
    assert time_tags.format_time(datetime.time(15, 0)) == "3pm"
