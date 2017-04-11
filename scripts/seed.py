import sys
from random import randint
from os.path import dirname, join
sys.path.append(join(dirname(dirname(__file__))))

from praelatus.lib import session, clean_db
import praelatus.lib.users as usr
import praelatus.lib.projects as prj
import praelatus.lib.labels as lbls
import praelatus.lib.roles as rls
import praelatus.lib.permissions as perm_schemes

# TODO finish the rest of the libs for the other models and add them
# here
print(sys.path)

db = session()
# clean_db()

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

roles = [
    {
        'name': 'Administrator'
    },
    {
        'name': 'Contributor'
    },
    {
        'name': 'User'
    },
    {
        'name': 'Anonymous'
    }
]

for r in roles:
    rls.new(db, **r)

permission_scheme = {
    'name':        'Default Permission Scheme',
    'description': 'The recommended defaults for permissions.',
    'permissions': {
        'Administrator': [
            'VIEW_PROJECT',
            'ADMIN_PROJECT',
            'CREATE_TICKET',
            'COMMENT_TICKET',
            'REMOVE_COMMENT',
            'REMOVE_OWN_COMMENT',
            'EDIT_OWN_COMMENT',
            'EDIT_COMMENT',
            'TRANSITION_TICKET',
            'EDIT_TICKET',
            'REMOVE_TICKET',
        ],
        'Contributor': [
            'VIEW_PROJECT',
            'CREATE_TICKET',
            'COMMENT_TICKET',
            'REMOVE_OWN_COMMENT',
            'EDIT_OWN_COMMENT',
            'TRANSITION_TICKET',
            'EDIT_TICKET',
        ],
        'User': [
            'VIEW_PROJECT',
            'CREATE_TICKET',
            'COMMENT_TICKET',
            'REMOVE_OWN_COMMENT',
            'EDIT_OWN_COMMENT',
        ],
        'Anonymous': [
            'VIEW_PROJECT',
        ],
    }
}

perm_schemes.new(db, **permission_scheme)

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

statuses = [
    {
        'name': 'Backlog',
    },
    {
        'name': 'In Progress',
    },
    {
        'name': 'Done',
    },
    {
        'name': 'For Saving',
    },
    {
        'name': 'For Removing',
    },
]

ticket_types = [
    {
        'name': 'Bug',
    },
    {
        'name': 'Epic',
    },
    {
        'name': 'Story',
    },
    {
        'name': 'Feature',
    },
    {
        'name': 'Question',
    }
]

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


workflow = {
    'name': 'Simple Workflow',
    'transitions': {
        'Backlog': [
            {
                'name': 'In Progress',
                'to_status': {
                    'id': 2
                },
                'hooks': [],
            },
        ],
        'In Progress': [
            {
                'name':     'Done',
                'to_status': {
                    'id': 3
                },
                'hooks':    [],
            },
            {
                'name':     'Backlog',
                'to_status': {
                    'id': 1
                },
                'hooks':    [],
            },
        ],
        'Done': [
            {
                'name':     'ReOpen',
                'to_status': {
                    'id': 1
                },
                'hooks':    [],
            },
        ],
    }
}
