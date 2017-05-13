import praelatus.lib.labels as labels

def test_get(db):
    lbl = labels.get(db, name='duplicate')
    assert lbl is not None
    assert lbl.name == 'duplicate'
    assert lbl.id is not None


def test_get_with_filter(db):
    lbls = labels.get(db, filter='*t*')
    assert lbls is not None
    assert len(lbls) > 0
    assert lbls[0].id is not None

def test_update(db):
    new_name = 'duplex'
    lbl = labels.get(db, name='duplicate')
    lbl.name = new_name

    labels.update(db, label=lbl)

    l = labels.get(db, id=lbl.id)
    assert l.name == new_name


def test_delete(db):
    label = {
            'name': 'DELETE THIS',
    }

    labels.new(db, **label)

    l = labels.get(db, name='DELETE THIS')
    assert l is not None

    labels.delete(db, label=l)

    l = labels.get(db, name='DELETE THIS')
    assert l is None


def test_json(db):
    label = {
        'name': 'json'
    }

    l = labels.new(db, **label)
    label['id'] = l.id

    lbl = labels.get(db, id=l.id)
    assert label == lbl.clean_dict()
