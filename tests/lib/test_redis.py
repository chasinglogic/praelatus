import praelatus.lib.redis as redis


def test_set_delete_and_get(admin):
    redis.set('test', admin)
    u = redis.get('test')
    assert u == admin

    redis.delete('test')
    u = redis.get('test')
    assert u is None
