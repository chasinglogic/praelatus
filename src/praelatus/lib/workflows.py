"""
Contains functions for interacting with workflows.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from sqlalchemy.orm import joinedload

from praelatus.models import Workflow
from praelatus.models import Ticket
from praelatus.models import Transition
from praelatus.models import Hook
from praelatus.lib.permissions import sys_admin_required
import praelatus.lib.statuses as statuses


def get(db, actioning_user=None, id=None, name=None, filter=None,
        preload_tickets=False):
    """
    Get workflows from the database.

    If the keyword arguments id or name are specified returns a
    single sqlalchemy result, otherwise returns all matching results.

    Keyword Arguments:
    id -- database id (default None)
    name -- the workflowe name (default None)
    filter -- a pattern to search through workflows with (default None)
    preload_tickets -- whether to load the tickets associated with
                       this workflowe (default False)
    """
    query = db.query(Workflow)

    if id is not None:
        query = query.filter(Workflow.id == id)

    if name is not None:
        query = query.filter(Workflow.name == name)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(Workflow.name.like(pattern))

    if preload_tickets:
        query = query.options(joinedload(Ticket))

    if any([id, name]):
        return query.first()
    return query.order_by(Workflow.name).all()


@sys_admin_required
def new(db, actioning_user=None, **kwargs):
    """
    Create a new workflowe in the database then returns that workflowe.

    The kwargs are parsed such that if a json representation of a
    workflowe is provided as expanded kwargs it will be handled
    properly.

    If a required argument is not provided then it raises a KeyError
    indicating which key was missing. Useful for returning HTTP 400
    errors.

    Required Keyword Arguments:
    name -- the workflow name
    """
    new_workflow = Workflow(
        name=kwargs['name'],
        description=kwargs.get('description')
    )

    db.add(new_workflow)

    transitions = kwargs.get('transitions', {})
    for from_status_name, available_transitions in transitions.items():
        from_status = statuses.get(db, name=from_status_name)
        if from_status is None and from_status_name != "Create":
            from_status = statuses.new(
                db,
                actioning_user=actioning_user,
                name=from_status
            )

        for tran in available_transitions:
            to_status = statuses.get(
                db,
                name=tran['to_status']['name']
            )

            if to_status is None:
                to_status = statuses.new(db, **to_status)

            hks = []
            for h in tran.get('hooks', []):
                hks.append(Hook(
                    name=h['name'],
                    description=h.get('description'),
                    body=h.get('body'),
                    method=h.get('method'),
                    url=h.get('url')
                ))

            new_tr = Transition(
                name=tran['name'],
                from_status=from_status,
                to_status=to_status,
                hooks=hks,
            )

            db.add(new_tr)
            new_workflow.transitions.append(new_tr)

    db.commit()
    return new_workflow


@sys_admin_required
def update(db, actioning_user=None, workflow=None):
    """
    Update the given workflowe in the database.

    workflowe must be a Workflow class instance.
    """
    db.add(workflow)
    db.commit()


@sys_admin_required
def delete(db, actioning_user=None, workflow=None):
    """
    Remove the given workflowe from the database.

    workflowe must be a Workflow class instance.
    """
    db.delete(workflow)
    db.commit()


def update_from_json(db, workflow, jsn, actioning_user=None):
    """Update workflow using jsn as the new form."""
    workflow.name = jsn['name']
    workflow.description = jsn['description']

    transitions = jsn.get('transitions', {})
    new_transitions = []
    for from_status_name, available_transisitions in transitions.items():
        from_status = statuses.get(db, name=from_status_name)
        if from_status is None and from_status_name != "Create":
            from_status = statuses.new(
                db,
                actioning_user=actioning_user,
                name=from_status
            )

            for tran in available_transisitions:
                to_status = statuses.get(
                    db,
                    actioning_user=actioning_user,
                    name=tran['to_status']['name']
                )

                if to_status is None:
                    to_status = statuses.new(
                        db,
                        actioning_user=actioning_user,
                        **to_status
                    )

                hks = []
                for h in tran.get('hooks', []):
                    hook = db.query(Hook).\
                        filter(Hook.id == h.get('id', 0))
                    if hook is None:
                        hook = Hook()
                    hook.name = h['name']
                    hook.description = h.get('description')
                    hook.body = h.get('body')
                    hook.method = h.get('method')
                    hook.url = h.get('url')
                    hks.append(hook)

                t = db.query(Transition).\
                    filter(Transition.id == tran.get('id', 0))
                if t is None:
                    t = Transition()
                t.name = tran['name']
                t.from_status = from_status
                t.to_status = to_status
                t.hooks = hks
                db.update(t)
                new_transitions.append(t)

    workflow.transitions = new_transitions
    return workflow
