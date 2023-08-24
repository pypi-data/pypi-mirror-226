def test_api():
    """test if the provided functionality is importable"""
    from sensospot_tools import (
        normalize,  # noqa: F401
        select,  # noqa: F401
        select_hdr_data,  # noqa: F401
        split,  # noqa: F401
    )
