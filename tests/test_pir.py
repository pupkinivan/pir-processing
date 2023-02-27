from pathlib import Path

from mock_data import PIR_FILE


def test_sample_rate():
    sample_rate_real = PIR_FILE.get_sample_rate()
    sample_rate_expected = 48000
    print(f"{sample_rate_real = }\t{sample_rate_expected = }")
    assert sample_rate_real == sample_rate_expected, f"Sample rate ({sample_rate_real}) is not as expected ({sample_rate_expected})"

def test_ir_with_time():
    array = PIR_FILE.get_ir()
    assert array.shape[1] == 2, "There are not two columns in the IR+Time array"
    assert array.shape[0] > 1, "There should be more than one sample in the IR"
