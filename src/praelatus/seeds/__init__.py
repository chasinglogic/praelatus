"""Contains a function for seeding a database with test data."""

from random import randint
import praelatus.lib.users as usr
import praelatus.lib.projects as prj
import praelatus.lib.labels as lbls
import praelatus.lib.roles as rls
import praelatus.lib.fields as flds
import praelatus.lib.tickets as tks
import praelatus.lib.ticket_types as types
import praelatus.lib.workflows as workflows
import praelatus.lib.statuses as statuses
import praelatus.lib.permissions as perm_schemes
from praelatus.lib.utils import rollback


@rollback
def seed(db):
    """Seed the given db with test data."""
    import praelatus.seeds.defaults as defaults

    users = [
        {
            'username': 'testadmin',
            'password': 'test',
            'email': 'test@example.com',
            'full_name': 'Test Testerson',
            'is_admin': True,
        },
        {
            'username': 'testuser',
            'password': 'test',
            'email': 'test@example.com',
            'full_name': 'Test Testerson II',
        }
    ]

    for u in defaults.users:
        try:
            usr.new(db, **u)
        except Exception as e:
            print(e)
            continue

    for u in users:
        try:
            usr.new(db, **u)
        except Exception as e:
            print(e)
            continue

    admin = usr.get(db, id=2)
    for r in defaults.roles:
        try:
            rls.new(db, actioning_user=admin, **r)
        except:
            continue

    perm_schemes.new(db, actioning_user=admin,
                     **defaults.permission_scheme)

    projects = [
        {
            'name': 'TEST Project',
            'key':  'TEST',
            'lead': {'id': 3},
        },
        {
            'name': 'TEST Project 2',
            'key':  'TEST2',
            'lead': {'id': 2},
        },
        {
            'name': 'TEST Project 3',
            'key':  'TEST3',
            'lead': {'id': 2},
        }
    ]

    for p in projects:
        try:
            prj.new(db, **p)
        except Exception as e:
            print(e)
            continue

    labels = [
        {
            'name': 'test',
        },
        {
            'name': 'duplicate',
        },
        {
            'name': 'wontfix',
        }
    ]

    for l in labels:
        try:
            lbls.new(db, **l)
        except:
            continue

    priorities = ['HIGH', 'MEDIUM', 'LOW']

    fields = [
        {
            'name':     'Story Points',
            'data_type': 'INT',
        },
        {
            'name':     'TestField2',
            'data_type': 'FLOAT',
        },
        {
            'name':     'TestField3',
            'data_type': 'INT',
        },
        {
            'name':     'TestField4',
            'data_type': 'DATE',
        },
        {
            'name':     'Priority',
            'data_type': 'OPT',
            'options':  priorities,
        },
    ]

    for f in fields:
        try:
            flds.new(db, **f)
        except:
            continue

    for s in defaults.statuses:
        try:
            statuses.new(db, actioning_user=admin, **s)
        except Exception as e:
            print(e)
            continue

    for t in defaults.ticket_types:
        try:
            types.new(db, actioning_user=admin, **t)
        except Exception as e:
            print(e)
            continue

    workflows.new(db, actioning_user=admin, **defaults.workflow)

    for i in range(1, 100):
        t = {
            'summary': 'This is ticket #%d' % i,
            'description': 'This is a test',
            'workflow_id': 1,
            'reporter': {'id': 1},
            'assignee': {'id': 1},
            'status': {'id': 1},
            'project': {'id': 1, 'key': 'TEST'},
            'labels': [],
            'fields': [
                {
                    'name': 'Story Points',
                    'value': randint(1, 50),
                },
                {
                    'name': 'Priority',
                    'selected': priorities[randint(0, 2)]
                }
            ],
            'ticket_type': {
                'id': 1,
            }
        }

        try:
            tks.new(db, **t)
        except Exception as e:
            print(e)
            continue
