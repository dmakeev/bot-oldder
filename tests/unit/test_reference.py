"""Unit tests for reference service."""
from bot.services import reference as ref_service


def test_get_version():
    """Test getting reference version."""
    version = ref_service.get_version()
    assert version is not None
    assert version == '4'


def test_search_by_action():
    """Test searching reference by action."""
    results = ref_service.search("собрание")
    assert len(results) > 0
    for r in results:
        assert "собрание" in r['action'].lower() or "собрание" in r['law'].lower()


def test_search_by_law():
    """Test searching reference by law."""
    results = ref_service.search("ЗоБ")
    assert len(results) > 0


def test_search_not_found():
    """Test searching for non-existent item."""
    results = ref_service.search("xyz123")
    assert len(results) == 0


def test_get_item():
    """Test getting specific item."""
    item = ref_service.get_item("1.1")
    assert item is not None
    assert item['id'] == "1.1"


def test_get_item_not_found():
    """Test getting non-existent item."""
    item = ref_service.get_item("999")
    assert item is None