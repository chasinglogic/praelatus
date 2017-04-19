import praelatus.lib.sessions as sessions


def test_set_and_get(admin):
    sess_id = sessions.gen_session_id()
    sessions.set(sess_id, admin)
    u = sessions.get(sess_id)
    assert str(u) == str(admin)
