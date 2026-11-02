def test_entire_transition_contract(application_class, initial, event, expected):
    application = make_application(application_class, initial)
    before = snapshot(application)
    action = getattr(application, event)
    args = ("  Dokumen tidak sesuai  ",) if event == "reject" else ()

    if expected is None:
        with pytest.raises(InvalidTransitionError):
            action(*args)
        assert snapshot(application) == before  # kegagalan tidak merusak state
    else:
        assert action(*args) is None
        assert application.status == expected
        assert application.shop_name == "Kedai Demo"
        if expected == S.REJECTED:
            assert application.rejection_reason == "Dokumen tidak sesuai"
        else:
            assert application.rejection_reason is None
