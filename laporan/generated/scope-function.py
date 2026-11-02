def validate_scopes(
    client_active: bool,
    requested_scope: str,
    allowed_scopes: frozenset[str],
) -> frozenset[str]:
    """Terima hanya client aktif dengan scope tidak kosong dan seluruhnya diizinkan.

    Precondition: client_active adalah bool, requested_scope adalah str, dan
    allowed_scopes adalah frozenset[str]. Identitas client sudah diverifikasi
    oleh pemanggil. Scope bersifat case-sensitive; whitespace dan duplikat
    dinormalisasi. Fungsi tidak mengubah konfigurasi izin milik pemanggil.
    """
    if not client_active:  # D1
        raise ScopeValidationError("CLIENT_INACTIVE")

    scopes = frozenset(requested_scope.split())
    if not scopes:  # D2
        raise ScopeValidationError("EMPTY_SCOPE")

    if not scopes.issubset(allowed_scopes):  # D3
        raise ScopeValidationError("SCOPE_NOT_ALLOWED")

    return scopes
