"""Contains definition for the CommentStore."""

from praelatus.store import Store
from praelatus.models import Comment
from praelatus.models import Ticket
from praelatus.lib.permissions import permission_required
from praelatus.lib.permissions import is_system_admin
from praelatus.lib.permissions import has_permission


class CommentStore(Store):
    """Stores and retrieves comments."""

    @permission_required('VIEW_PROJECT')
    def get(self, db, uid=None, **kwargs):
        """Retrieve a single comment by ID."""
        return db.query(Comment).filter_by(id=uid).first()

    @permission_required('VIEW_PROJECT')
    def get_for_ticket(self, db, ticket_id=0, ticket_key=None, **kwargs):
        """Get all tickets for given ticket_id or ticket_key."""
        query = db.query(Comment)
        if ticket_key:
            query = query.join(Ticket).filter(Ticket.key == ticket_key)
        else:
            query = query.filter(Comment.ticket_id == ticket_id)
        return query.all()

    @permission_required('COMMENT_TICKET')
    def new(self, db, **kwargs):
        """Add comment to if acitoning_user has permission.

        Required Keyword Arguments:
        actioning_user -- user who is making the comment
        author -- json representation of a User who is the author
        project -- the project the ticket belongs to
        ticket_id -- the id of the ticket the comment is being added to
        """
        new_comment = Comment(author_id=kwargs['author']['id'],
                              body=kwargs['body'],
                              ticket_id=kwargs['ticket_id'])
        db.add(new_comment)
        db.commit()
        return new_comment

    def has_permission(self, db, model, actioning_user, project):
        """Check if user has permissions for the given comment.

        This is used for updates and deletes.
        """
        return (
            # If they have edit comment they can edit any comment.
            has_permission(db, 'EDIT_COMMENT', project, actioning_user) or
            # If the actioning_user is the author and they have
            # the EDIT_OWN_COMMENT permission then they can
            # perform the edit.
            (model.author_id == actioning_user['id'] and
             has_permission(db, 'EDIT_OWN_COMMENT',
                            project, actioning_user)) or
            # If sys admin then they can do whatever
            is_system_admin(db, actioning_user)
        )

    def update(self, db, model=None, actioning_user=None, project=None):
        """Update the given comment.

        Not using permission_required to make as little DB calls as possible.
        """
        if self.has_permission(db, model, actioning_user, project):
            db.add(model)
            db.commit()
        else:
            raise PermissionError('permission denied')

    def delete(self, db, model=None, actioning_user=None, project=None):
        """Delete the given comment.

        Not using permission_required to make as little DB calls as needed.
        """
        if self.has_permission(db, model, actioning_user, project):
            db.delete(model)
            db.commit()
        else:
            raise PermissionError('permission denied')


store = CommentStore(Comment)
