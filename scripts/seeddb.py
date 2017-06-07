from random import randint

try:
    import praelatus.lib.defaults as defaults
    from praelatus.store import *
    from praelatus.lib import connection
except ImportError as e:
    import sys
    print(e)
    print('You need to install praelatus before running this script.')
    sys.exit(1)

try:
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
    with connection() as db:
        for u in users:
            UserStore.new(db, **u)

    with connection() as db:
        admin = UserStore.get(db, username='testadmin')

        print('Seeding permissions schemes...')
        PermissionSchemeStore.new(db, actioning_user=admin,
                                  **defaults.permission_scheme)

        print('Seeding statuses...')
        for s in defaults.statuses:
            StatusStore.new(db, actioning_user=admin, **s)

        print('Seeding workflows...')
        WorkflowStore.new(db, actioning_user=admin, **defaults.workflow)

    with connection() as db:
        admin = UserStore.get(db, username='testadmin')
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

        print('Seeding projects...')
        for p in projects:
            ProjectStore.new(db, actioning_user=admin, **p)

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

        print('Seeding labels...')
        for l in labels:
            LabelStore.new(db, **l)

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

        print('Seeding fields...')
        for f in fields:
            FieldStore.new(db, actioning_user=admin, **f)

        print('Seeding ticket types...')
        for t in defaults.ticket_types:
            TicketTypeStore.new(db, actioning_user=admin, **t)

        assignees = [None, {'id': 2}, {'id': 3}]
        print('Seeding tickets...')
        for i in range(1, 100):
            t = {
                'summary': 'This is ticket #%d' % i,
                'description': """# Utque erant et edentem suoque nox fertur

## Tegi aurum inridet flumine auras natas vulnus

Lorem markdownum misit sudor, sine eodem libratum munus aristis tutos, hac.
Longe mens vultus iurgia Iovem difficilis suus; ut erat mollis robore terga ei
perque! Quae quos sacrorum custodit quaecumque harena fallis et modo hinc
[recessu](http://venerat.com/), superorum Peleus, temptamenta. **Pudore** Sparte
lentisciferumque nataque inpulsos et ille novat haec sollicitare Plura, levis
vellet valuit, summo dum lutea viso. Solebat lintea ingentibus capillis dicta
Paridis seque quoquam [poposcit in](http://per.net/) Tempe vivacem.

1. Nate nulli
2. Coniunx hausi nunc Quirini Othrys
3. Caede nascuntur ubera congreditur vincula ubi regis
4. Spatium pectore amplexus ferunt ille instat cultores

Illo dolores voluit Achaemenias unde theatris paventem secum ineamus minacia
retro. Duplicataque siste suo recessit; opes albus moribunda referentem animam
nulloque domini et laborent hac?

## Senecta finita

Iovi nec aperire mihi mira respondit, qui exit vulnere aeterno dixerunt dat
corpus? Erit terrae, avidas; sola plenum, cauda edax et referre. Quater posuere:
facit mihi primaque remanet parte, eundo.""",
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

            TicketStore.new(db, **t)

        tickets = TicketStore.search(db, actioning_user=admin, search='TEST*')
        print('Seeding comments...')
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

                CommentStore.new(db, actioning_user=comment['author'],
                                 project=t.project, **comment)
except Exception:
    print('Exception during seeding. Carrying on!')
