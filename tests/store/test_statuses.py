import praelatus.lib.statuses as statuses

from praelatus.api.schemas import StatusSchema


def test_get(db, admin):
    lbl = statuses.get(db, actioning_user=admin, name='Backlog')
    assert lbl is not None
    assert lbl.name == 'Backlog'
    assert lbl.id is not None


def test_get_with_filter(db, admin):
    lbls = statuses.get(db, actioning_user=admin, filter='*o*')
    assert lbls is not None
    assert len(lbls) > 0
    assert lbls[0].id is not None


def test_update(db, admin):
    new_name = 'duplex'
    lbl = statuses.get(db, actioning_user=admin, name='For Saving')
    lbl.name = new_name

    statuses.update(db, actioning_user=admin, status=lbl)

    l = statuses.get(db, actioning_user=admin, id=lbl.id)
    assert l.name == new_name


def test_delete(db, admin):
    status = {
            'name': 'DELETE THIS',
    }

    statuses.new(db, actioning_user=admin, **status)

    l = statuses.get(db, actioning_user=admin, name='DELETE THIS')
    assert l is not None

    statuses.delete(db, actioning_user=admin, status=l)

    l = statuses.get(db, actioning_user=admin, name='DELETE THIS')
    assert l is None


def test_json(db, admin):
    status = {
        'name': 'json'
    }

    l = statuses.new(db, actioning_user=admin, **status)
    status['id'] = l.id

    lbl = statuses.get(db, actioning_user=admin, id=l.id)
    assert status == lbl.clean_dict()
