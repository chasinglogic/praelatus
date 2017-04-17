import praelatus.lib.users as users
import praelatus.lib.tickets as tickets


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
    print(tks)
    assert tks is not None
    assert len(tks) > 0
    assert 'TEST' in tks[0].key
    assert len(tks[0].fields) > 0


def test_update(db):
    new_description = 'Super Duper Test Ticket'
    lead = users.get(db, username='testuser')
    ticket = tickets.get(db, key='TEST-2')
    ticket.description = new_description

    tickets.update(db, ticket=ticket, project=lead.lead_of[0], actioning_user=lead)

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
