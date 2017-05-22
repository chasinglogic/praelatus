"""Contains definition for the WorkflowStore."""

from praelatus.store import Store
from praelatus.models import Hook
from praelatus.models import Status
from praelatus.models import Workflow
from praelatus.models import Transition
from praelatus.lib.permissions import sys_admin_required

status_store = Store(Status)


class WorkflowStore(Store):
    """Stores and retrieves workflows."""

    def __init__(self, model, status_store):
        self.status_store = status_store
        self.model = model

    @sys_admin_required
    def new(self, db, actioning_user=None, **kwargs):
        """Add workflow to if acitoning_user has permission.

        Required Keyword Arguments:
        """
        new_workflow = Workflow(
            name=kwargs['name'],
            description=kwargs.get('description')
        )

        db.add(new_workflow)

        transitions = kwargs.get('transitions', {})
        new_workflow.transitions = self.make_transitions(db, transitions,
                                                         actioning_user)
        db.commit()
        return new_workflow

    def update_from_json(self, db, workflow, jsn, actioning_user=None):
        """Update workflow using jsn as the new form."""
        workflow.name = jsn['name']
        workflow.description = jsn['description']

        transitions = jsn.get('transitions', {})
        workflow.transitions = self.make_transitions(db, transitions,
                                                     actioning_user)
        return workflow

    def make_transitions(self, db, transitions, actioning_user):
        """Turn JSON transitions into SQLAlchemy models."""
        new_transitions = []
        for from_status_name, available_transisitions in transitions.items():
            from_status = self.status_store.get(db, name=from_status_name)
            if from_status is None and from_status_name != "Create":
                from_status = self.status_store.new(
                    db,
                    actioning_user=actioning_user,
                    name=from_status
                )

            for tran in available_transisitions:
                to_status = self.status_store.get(
                    db,
                    actioning_user=actioning_user,
                    name=tran['to_status']['name']
                )

                if to_status is None:
                    to_status = self.status_store.new(
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
                    filter(Transition.id == tran.get('id', 0)).\
                    first()
                if t is None:
                    t = Transition()
                t.name = tran['name']
                t.from_status = from_status
                t.to_status = to_status
                t.hooks = hks
                db.add(t)
                db.commit()
                new_transitions.append(t)
        return new_transitions





status_store = Store(Status)
store = WorkflowStore(Workflow, status_store)
