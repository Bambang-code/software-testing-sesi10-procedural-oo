import pytest

from zenta_auth.scopes import ScopeValidationError, validate_scopes


def test_p1_inactive_client_is_rejected(order_scopes):
    with pytest.raises(ScopeValidationError, match="^CLIENT_INACTIVE$"):
        validate_scopes(False, "read:catalog", order_scopes)


def test_p2_empty_scope_is_rejected(order_scopes):
    with pytest.raises(ScopeValidationError, match="^EMPTY_SCOPE$"):
        validate_scopes(True, "", order_scopes)


def test_p3_disallowed_scope_is_rejected(order_scopes):
    with pytest.raises(ScopeValidationError, match="^SCOPE_NOT_ALLOWED$"):
        validate_scopes(True, "admin:users", order_scopes)


def test_p4_allowed_scopes_are_returned(order_scopes):
    result = validate_scopes(True, "reserve:stock commit:stock release:stock", order_scopes)
    assert result == frozenset({"reserve:stock", "commit:stock", "release:stock"})


@pytest.mark.parametrize("requested", [" ", "\t\n", "   \t   "])
def test_whitespace_only_is_empty(requested, order_scopes):
    with pytest.raises(ScopeValidationError, match="^EMPTY_SCOPE$"):
        validate_scopes(True, requested, order_scopes)


def test_normalization_removes_duplicate_scopes_and_whitespace(order_scopes):
    assert validate_scopes(True, "  read:catalog\tread:catalog\nreserve:stock  ", order_scopes) == frozenset(
        {"read:catalog", "reserve:stock"}
    )


@pytest.mark.parametrize("requested", ["read:catalog admin:users", "READ:CATALOG", "reserve:stockx"])
def test_partial_match_or_mixed_request_does_not_grant_extra_permissions(requested, order_scopes):
    with pytest.raises(ScopeValidationError, match="^SCOPE_NOT_ALLOWED$"):
        validate_scopes(True, requested, order_scopes)


def test_empty_allowlist_rejects_nonempty_request():
    with pytest.raises(ScopeValidationError, match="^SCOPE_NOT_ALLOWED$"):
        validate_scopes(True, "read:catalog", frozenset())


def test_inactive_error_takes_precedence_over_other_invalid_input(order_scopes):
    with pytest.raises(ScopeValidationError, match="^CLIENT_INACTIVE$"):
        validate_scopes(False, "", order_scopes)


def test_allowlist_is_not_changed_by_validation(order_scopes):
    before = frozenset(order_scopes)
    validate_scopes(True, "read:catalog", order_scopes)
    assert order_scopes == before
