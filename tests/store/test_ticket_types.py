import praelatus.lib.ticket_types as ticket_types


def test_get(db, admin):
    lbl = ticket_types.get(db, actioning_user=admin, name='Bug')
    assert lbl is not None
    assert lbl.name == 'Bug'
    assert lbl.id is not None


def test_get_with_filter(db, admin):
    lbls = ticket_types.get(db, actioning_user=admin, filter='*or*')
    assert lbls is not None
    assert len(lbls) > 0
    assert lbls[0].id is not None


def test_update(db, admin):
    new_name = 'Duplex'
    lbl = ticket_types.get(db, actioning_user=admin, name='Question')
    lbl.name = new_name

    ticket_types.update(db, actioning_user=admin, ticket_type=lbl)

    l = ticket_types.get(db, actioning_user=admin, id=lbl.id)
    assert l.name == new_name


def test_delete(db, admin):
    ticket_type = {
            'name': 'DELETE THIS',
    }

    ticket_types.new(db, actioning_user=admin, **ticket_type)

    l = ticket_types.get(db, actioning_user=admin, name='DELETE THIS')
    assert l is not None

    ticket_types.delete(db, actioning_user=admin, ticket_type=l)

    l = ticket_types.get(db, actioning_user=admin, name='DELETE THIS')
    assert l is None


def test_json(db, admin):
    ticket_type = {
        'name': 'json'
    }

    l = ticket_types.new(db, actioning_user=admin, **ticket_type)
    ticket_type['id'] = l.id

    lbl = ticket_types.get(db, actioning_user=admin, id=l.id)
    assert ticket_type == lbl.clean_dict()
