"""Contains the defaults that should be set up on a new instance."""

users = [
    {
        'username': 'anonymous',
        'password': 'none',
        'email': 'anonymous',
        'full_name': 'Anonymous User',
        'is_active': False,
    }
]

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

permissions = [
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
    'REMOVE_TICKET'
]


permission_scheme = {
    'name': 'Default Permission Scheme',
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


workflow = {
    'name': 'Default Workflow',
    'description': 'A simple workflow that fits most use cases.',
    'transitions': {
        'Create': [
            {
                'name': 'Create',
                'to_status': {
                    'id': 1,
                    'name': 'Backlog'
                }
            }
        ],
        'Backlog': [
            {
                'name': 'In Progress',
                'to_status': {
                    'id': 2,
                    'name': 'In Progress'
                },
                'hooks': [],
            },
        ],
        'In Progress': [
            {
                'name': 'Done',
                'to_status': {
                    'id': 3,
                    'name': 'Done'
                },
                'hooks': [],
            },
            {
                'name': 'Backlog',
                'to_status': {
                    'id': 1,
                    'name': 'Backlog'
                },
                'hooks': [],
            },
        ],
        'Done': [
            {
                'name': 'ReOpen',
                'to_status': {
                    'id': 1,
                    'name': 'Backlog'
                },
                'hooks': [],
            },
        ],
    }
}
