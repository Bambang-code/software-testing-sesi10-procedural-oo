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
