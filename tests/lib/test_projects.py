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


def test_get_filter_action(db):
    admin = users.get(db, username='testadmin')

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


def test_delete(db):
    lead = users.get(db, username='testuser')
    project = {
            'name': 'DELETE THIS PROJECT',
            'key':  'DELETE',
            'lead': {'id': lead.id},
    }

    projects.new(db, **project)

    p = projects.get(db, key='DELETE')
    assert p is not None

    projects.delete(db, project=p, actioning_user=lead)

    p = projects.get(db, key='DELETE')
    assert p is None
