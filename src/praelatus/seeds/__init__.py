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
from praelatus.lib import session


@rollback
def seed():
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

    print('Seeding users...')
    with session() as db:
        for u in defaults.users:
            usr.new(db, **u)

        for u in users:
            usr.new(db, **u)

        admin = usr.get(db, id=2)

    with session() as db:
        for r in defaults.roles:
            rls.new(db, actioning_user=admin, **r)

        perm_schemes.new(db, actioning_user=admin,
                         **defaults.permission_scheme)

        for s in defaults.statuses:
            statuses.new(db, actioning_user=admin, **s)

    with session() as db:
        workflows.new(db, actioning_user=admin, **defaults.workflow)

    with session() as db:
        projects = [
            {
                'name': 'TEST Project',
                'key': 'TEST',
                'lead': {'id': 3},
            },
            {
                'name': 'TEST Project 2',
                'key': 'TEST2',
                'lead': {'id': 2},
            },
            {
                'name': 'TEST Project 3',
                'key': 'TEST3',
                'lead': {'id': 2},
            }
        ]
        
        for p in projects:
            prj.new(db, **p)
            
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
                lbls.new(db, **l)
                
                priorities = ['HIGH', 'MEDIUM', 'LOW']
                
                fields = [
                    {
                        'name': 'Story Points',
                        'data_type': 'INT',
                    },
                    {
                        'name': 'Priority',
                        'data_type': 'OPT',
                        'options': priorities,
                    },
                    {
                        'name': 'Business Value',
                        'data_type': 'FLOAT'
                    },
                    {
                        'name': 'Due Date',
                        'data_type': 'DATE'
                    },
                    {
                        'name': 'Organization',
                        'data_type': 'STRING'
                    },
                ]
                
                for f in fields:
                    flds.new(db, **f)
                    
                    for t in defaults.ticket_types:
                        types.new(db, actioning_user=admin, **t)
                        
                        assignees = [None, {'id': 2}, {'id': 3}]
                        for i in range(1, 100):
                            t = {
                                'summary': 'This is ticket #%d' % i,
                                'description': 'This is a test',
                                'workflow_id': 1,
                                'reporter': assignees[randint(1, 2)],
                                'assignee': assignees[randint(0, 2)],
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
                                        'value': priorities[randint(0, 2)]
                                    }
                                ],
                                'ticket_type': {
                                    'id': 1,
                                }
                            }
                            
                            tks.new(db, **t)
                            
                            tickets = tks.get(db, actioning_user=admin, filter='TEST*')
                            for t in tickets:
                                for i in range(1, 10):
                                    comment = {
                                        'body': """This is the %d th comment
                                        # Yo Dawg
                                        **I** *heard* you
                                        > like markdown
                                        so I put markdown in your comment""" % i,
                                        'author': assignees[randint(1, 2)],
                                        'ticket_key': t.key,
                                        'ticket_id': t.id
                                    }
                                    
                                    tks.add_comment(db, actioning_user=comment['author'],
                                                    project=t.project, **comment)

