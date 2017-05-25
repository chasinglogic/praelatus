import datetime

from praelatus.store import *
from praelatus.app.api.schemas import *


def test_stores(db, admin):
    ticket_type = TicketTypeStore.get(db, name='Bug')
    project = ProjectStore.get(db, uid='TEST')

    tests = [
        {
            'name': 'Ticket Store Test',
            'store': TicketStore,
            'schema': TicketSchema,
            'uid_param': 'TEST-2',
            'new': {
                'summary': 'json test',
                'description': 'testing json serialization',
                'ticket_type': ticket_type.jsonify(),
                'workflow_id': 1,
                'project': project.jsonify(),
                'reporter': admin,
                'labels': ['internal', 'test'],
                'fields': [
                    {
                        'name': 'Story Points',
                        'data_type': 'INT',
                        'value': 5,
                    },
                    {
                        'name': 'Priority',
                        'data_type': 'OPT',
                        'value': 'HIGH',
                    },
                    {
                        'name': 'Business Value',
                        'data_type': 'FLOAT',
                        'value': 1.24
                    },
                    {
                        'name': 'Due Date',
                        'data_type': 'DATE',
                        'value': str(datetime.datetime.now())
                    },
                    {
                        'name': 'Organization',
                        'data_type': 'STRING',
                        'value': 'Praelatus'
                    }
                ]
            },
        }
    ]

    for t in tests:
        store = t['store']
        res = store.get(db, uid=t['uid_param'],
                        actioning_user=admin)
        assert res is not None
        t['schema'].validate(res.jsonify())

        res = store.new(db, **t['new'])
        assert res is not None
