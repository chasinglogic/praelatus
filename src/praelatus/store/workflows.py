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
        for from_status_name, available_transitions in transitions.items():
            from_status = self.status_store.get(db, name=from_status_name)
            if from_status is None and from_status_name != "Create":
                from_status = self.status_store.new(
                    db,
                    actioning_user=actioning_user,
                    name=from_status
                )

            for tran in available_transitions:
                to_status = self.status_store.get(
                    db,
                    name=tran['to_status']['name']
                )

                if to_status is None:
                    to_status = self.status_store.new(db, **to_status)

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


status_store = Store(Status)
store = WorkflowStore(Workflow, status_store)
