import praelatus.lib.workflows as workflows
import pytest


@pytest.fixture
def workflow_json():
    return {
        'name':  'DELETE',
        'description': 'DELETE ME',
        'transitions': {
            'Create': [
                {
                    'name': 'Create',
                    'to_status': {
                        'id': 1,
                        'name': 'Backlog'
                    },
                    'hooks': [],
                }
            ],
            'Backlog': [
                {
                    'name': 'In Progress',
                    'to_status': {
                        'id': 2,
                        'name': 'In Progress'
                    },
                    'hooks': [],
                },
            ],
            'In Progress': [
                {
                    'name':     'Done',
                    'to_status': {
                        'id': 3,
                        'name': 'Done'
                    },
                    'hooks':    [],
                },
                {
                    'name':     'Backlog',
                    'to_status': {
                        'id': 1,
                        'name': 'Backlog'
                    },
                    'hooks':    [],
                },
            ],
            'Done': [
                {
                    'name':     'ReOpen',
                    'to_status': {
                        'id': 1,
                        'name': 'Backlog'
                    },
                    'hooks':    [],
                },
            ],
        }
    }



def test_get_one(db, admin):
    workflow = workflows.get(db, actioning_user=admin, name='Default Workflow')
    assert workflow is not None
    assert workflow.name == 'Default Workflow'
    assert workflow.transitions is not None
    assert len(workflow.transitions) > 0


def test_get_filter_action(db, admin):
    pjs = workflows.get(db, filter='Default*', actioning_user=admin)
    assert pjs is not None
    assert len(pjs) > 0
    assert 'Workflow' in pjs[0].name


def test_update(db, admin, workflow_json):
    new_name = 'Super Duper Test Workflow'
    workflow_json['name'] = 'TEST UPDATE'
    workflows.new(db, actioning_user=admin, **workflow_json)
    workflow = workflows.get(db, actioning_user=admin, name='TEST UPDATE')
    workflow.name = new_name

    workflows.update(db, workflow=workflow, actioning_user=admin)

    proj = workflows.get(db, id=workflow.id)
    assert proj is not None
    assert proj.name == new_name


def test_delete(db, admin, workflow_json):
    workflows.new(db, actioning_user=admin, **workflow_json)

    p = workflows.get(db, name='DELETE')
    assert p is not None

    workflows.delete(db, workflow=p, actioning_user=admin)

    p = workflows.get(db, name='DELETE')
    assert p is None


def test_json(db, admin, workflow_json):
    workflow_json['name'] = 'JSON Test Workflow'
    w = workflows.new(db, actioning_user=admin, **workflow_json)
    workflow_json['id'] = w.id
    ref_dict = w.clean_dict()

    # Fill in the ID's for our transitions. I can't think of a better way.
    for k, v in workflow_json['transitions'].items():
        refs = ref_dict['transitions'][k]
        for tran in v:
            for r in refs:
                if tran['name'] == r['name']:
                    tran['id'] = r['id']

    assert workflow_json == ref_dict
