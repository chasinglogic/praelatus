import datetime

import praelatus.lib.users as users
import praelatus.lib.tickets as tickets
from praelatus.models import Project
from praelatus.models import Status
from praelatus.models import TicketType


def test_get_one(db):
    ticket = tickets.get(db, key='TEST-1')
    assert ticket is not None
    assert ticket.key == 'TEST-1'
    assert len(ticket.fields) > 0

def test_get_filter(db):
    tks = tickets.get(db, filter='test*')
    print(tks)
    assert tks is not None
    assert len(tks) > 0
    assert 'TEST' in tks[0].key
    assert len(tks[0].fields) > 0


def test_get_filter_action(db, admin):
    tks = tickets.get(db, filter='test*', actioning_user=admin)
    assert tks is not None
    assert len(tks) > 0
    assert 'TEST' in tks[0].key
    assert len(tks[0].fields) > 0


def test_get_by_assignee(db, admin):
    tks = tickets.get(db, assignee=admin)
    assert tks is not None
    assert len(tks) > 0
    assert 'TEST' in tks[0].key
    assert len(tks[0].fields) > 0


def test_get_by_reporter(db, admin):
    tks = tickets.get(db, reporter=admin)
    assert tks is not None
    assert len(tks) > 0
    assert 'TEST' in tks[0].key
    assert len(tks[0].fields) > 0


def test_preload_comments(db, admin):
    tks = tickets.get(db, actioning_user=admin,
                      key='TEST-2', preload_comments=True)
    assert tks is not None
    assert 'TEST' in tks.key
    assert len(tks.fields) > 0
    assert len(tks.comments) > 0


def test_update(db):
    new_description = 'Super Duper Test Ticket'
    lead = users.get(db, username='testuser')
    ticket = tickets.get(db, key='TEST-2')
    ticket.description = new_description

    tickets.update(db, ticket=ticket, project=lead.lead_of[0],
                   actioning_user=lead)

    tk = tickets.get(db, id=ticket.id)
    assert tk is not None
    assert tk.description == new_description


def test_delete(db):
    lead = users.get(db, username='testuser')
    ticket = {
        'summary': 'DELETE',
        'description': 'DELETE THIS TICKET',
        'ticket_type': {'id': 1},
        'workflow_id': 1,
        'project': {'id': 1, 'key': 'TEST'},
        'status': {'id': 1},
        'reporter': {'id': lead.id},
    }

    t = tickets.new(db, acitoning_user=lead, **ticket)

    p = tickets.get(db, key=t.key)
    assert p is not None

    tickets.delete(db, ticket=p, project=lead.lead_of[0], actioning_user=lead)

    p = tickets.get(db, key='DELETE')
    assert p is None


def test_json(db, admin):
    status = db.query(Status).get(1)
    project = db.query(Project).get(1)
    ticket_type = db.query(TicketType).get(1)

    ticket = {
        'summary': 'json test',
        'description': 'testing json serialization',
        'ticket_type': ticket_type.clean_dict(),
        'workflow_id': 1,
        'project': project.clean_dict(),
        'status': status.clean_dict(),
        'reporter': admin.clean_dict(),
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
    }

    t = tickets.new(db, acitoning_user=admin, **ticket)

    ticket['key'] = t.key
    ticket['id'] = t.id
    ticket['updated_date'] = str(t.updated_date)
    ticket['created_date'] = str(t.created_date)
    ticket['labels'] = sorted(ticket['labels'])

    ref_dict = t.clean_dict()
    ref_dict['labels'] = sorted(ref_dict['labels'])

    for field in ticket['fields']:
        for f in ref_dict['fields']:
            if field['name'] == f['name']:
                field['id'] = f['id']
                if f['data_type'] == 'OPT':
                    field['options'] = f['options']
                if f['data_type'] == 'DATE':
                    field['value'] = f['value']

    assert ticket == ref_dict


def test_add_comment(db, admin):
    t = tickets.get(db, key='TEST-40')
    comment = {
        'body': 'test',
        'author': admin.clean_dict(),
        'ticket_key': t.key,
        'ticket_id': t.id
    }

    ref_com = tickets.add_comment(db, project=t.project,
                                  actioning_user=admin, **comment)
    assert ref_com is not None

    comment['id'] = ref_com.id
    comment['created_date'] = str(ref_com.created_date)
    comment['updated_date'] = str(ref_com.updated_date)
    del comment['ticket_id']

    assert comment == ref_com.clean_dict()
