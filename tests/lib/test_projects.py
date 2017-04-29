import praelatus.lib.users as users
import praelatus.lib.projects as projects


def test_get_one(db):
    project = projects.get(db, key='TEST')
    assert project is not None
    assert project.key == 'TEST'


def test_get_filter(db):
    pjs = projects.get(db, filter='test*')
    print(pjs)
    assert pjs is not None
    assert len(pjs) > 0
    assert 'TEST' in pjs[0].key


def test_get_filter_action(db, admin):
    pjs = projects.get(db, filter='test*', actioning_user=admin)
    print(pjs)
    assert pjs is not None
    assert len(pjs) > 0
    assert 'TEST' in pjs[0].key


def test_update(db):
    new_name = 'Super Duper Test Project'
    lead = users.get(db, username='testuser')
    project = projects.get(db, key='TEST')
    project.name = new_name

    projects.update(db, project=project, actioning_user=lead)

    proj = projects.get(db, id=project.id)
    assert proj is not None
    assert proj.name == new_name


def test_delete(db, admin):
    lead = users.get(db, username='testuser')
    project = {
        'name': 'DELETE THIS PROJECT',
        'key':  'DELETE',
        'lead': {'id': lead.id}
    }

    projects.new(db, actioning_user=admin, **project)

    p = projects.get(db, key='DELETE')
    assert p is not None

    projects.delete(db, project=p, actioning_user=lead)

    p = projects.get(db, key='DELETE')
    assert p is None


def test_json(db, admin):
    project_json = {
        'name': 'JSON TEST Project',
        'key':  'JSON',
        'lead': admin,
        'homepage': None,
        'icon_url': None,
        'repo': None
    }

    p = projects.new(db, actioning_user=admin, **project_json)
    project_json['id'] = p.id
    project_json['created_date'] = str(p.created_date)
    assert p.clean_dict() == project_json
