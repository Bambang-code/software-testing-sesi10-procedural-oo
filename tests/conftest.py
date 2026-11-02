import pytest


@pytest.fixture
def order_scopes():
    """Data izin fiktif; tidak memuat kredensial aplikasi kelompok."""
    return frozenset({"read:catalog", "reserve:stock", "commit:stock", "release:stock"})
