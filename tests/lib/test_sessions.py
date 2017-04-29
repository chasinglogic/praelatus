import praelatus.lib.sessions as sessions


def test_set_delete_and_get(admin):
    sess_id = sessions.gen_session_id()
    sessions.set(sess_id, admin)
    u = sessions.get(sess_id)
    assert u == admin

    sessions.delete(sess_id)
    u = sessions.get(sess_id)
    assert u is None
