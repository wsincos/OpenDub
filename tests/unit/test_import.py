import sys


def test_core_package_exposes_release_metadata_without_torch() -> None:
    import opendub

    assert opendub.__version__ == "0.0.1a0"
    assert "torch" not in sys.modules
