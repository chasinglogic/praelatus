from random import randint
import praeltaus.seeds.defaults as defaults
import praelatus.lib.users as usr
import praelatus.lib.projects as prj
import praelatus.lib.labels as lbls
import praelatus.lib.roles as rls
import praelatus.lib.fields as flds
import praelatus.lib.tickets as tks
import praelatus.lib.permissions as perm_schemes


def seed(db):
    users = [
        {
            'username': 'testadmin',
            'password': 'test',
            'email': 'test@example.com',
            'full_name': 'Test Testerson',
            'is_admin': True,
        },
        {
            'username': 'anonymous',
            'password': 'none',
            'email': 'anonymous',
            'full_name': 'Anonymous User',
            'is_active': False,
        },
        {
            'username': 'testuser',
            'password': 'test',
            'email': 'test@example.com',
            'full_name': 'Test Testerson II',
        }
    ]

    for u in users:
        try:
            usr.new(db, **u)
        except:
            continue

    for r in defaults.roles:
        rls.new(db, **r)

    perm_schemes.new(db, **defaults.permission_scheme)

    projects = [
        {
            'name': 'TEST Project',
            'key':  'TEST',
            'lead': {'id': 1},
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
        flds.new(db, **f)

    for i in range(1, 100):
        t = {
            'summary': 'This is ticket #%d' % i,
            'description': 'This is a test',
            'workflow_id': 1,
            'reporter': {'id': 1},
            'assignee': {'id': 1},
            'status': {'id': 1},
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
            'type': {
                'id': 1,
            }
        }

        tks.new(db, **t)
