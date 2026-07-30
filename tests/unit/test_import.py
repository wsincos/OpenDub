import sys


def test_core_package_exposes_release_metadata_without_torch() -> None:
    import opendub

    assert opendub.__version__ == "0.4.0"
    assert "torch" not in sys.modules
