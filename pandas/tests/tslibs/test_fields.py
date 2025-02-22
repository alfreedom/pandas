import numpy as np
import pytest

from pandas._libs.tslibs import fields

import pandas._testing as tm


@pytest.fixture
def dtindex():
    dtindex = np.arange(5, dtype=np.int64) * 10**9 * 3600 * 24 * 32
    dtindex.flags.writeable = False
    return dtindex


def test_get_date_name_field_readonly(dtindex):
    # https://github.com/vaexio/vaex/issues/357
    #  fields functions shouldn't raise when we pass read-only data
    result = fields.get_date_name_field(dtindex, "month_name")
    expected = np.array(["January", "February", "March", "April", "May"], dtype=object)
    tm.assert_numpy_array_equal(result, expected)


def test_get_date_field_readonly(dtindex):
    result = fields.get_date_field(dtindex, "Y")
    expected = np.array([1970, 1970, 1970, 1970, 1970], dtype=np.int32)
    tm.assert_numpy_array_equal(result, expected)


def test_get_start_end_field_readonly(dtindex):
    dt64values = dtindex.view("M8[ns]")
    dt64values.flags.writeable = False

    result = fields.get_start_end_field(dt64values, "is_month_start", None)
    expected = np.array([True, False, False, False, False], dtype=np.bool_)
    tm.assert_numpy_array_equal(result, expected)


def test_get_timedelta_field_readonly(dtindex):
    # treat dtindex as timedeltas for this next one
    result = fields.get_timedelta_field(dtindex, "days")
    expected = np.arange(5, dtype=np.int32) * 32
    tm.assert_numpy_array_equal(result, expected)
