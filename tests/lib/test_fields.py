import praelatus.lib.fields as fields

def test_get(db):
    fld = fields.get(db, name='Priority')
    assert fld is not None
    assert fld.name == 'Priority'
    assert fld.id is not None


def test_get_with_filter(db):
    flds = fields.get(db, filter='*ority*')
    assert flds is not None
    assert len(flds) > 0
    assert flds[0].id is not None

def test_update(db):
    new_name = 'duplex'
    fld = fields.get(db, name='Story Points')
    fld.name = new_name

    fields.update(db, field=fld)

    l = fields.get(db, id=fld.id)
    assert l.name == new_name


def test_delete(db):
    field = {
        'name': 'DELETE THIS',
        'data_type': 'INT'
    }

    fields.new(db, **field)

    l = fields.get(db, name='DELETE THIS')
    assert l is not None

    fields.delete(db, field=l)

    l = fields.get(db, name='DELETE THIS')
    assert l is None


def test_json(db):
    field = {
        'name': 'json',
        'data_type': 'STRING'
    }

    l = fields.new(db, **field)
    field['id'] = l.id

    lbl = fields.get(db, id=l.id)
    assert field == lbl.clean_dict()
