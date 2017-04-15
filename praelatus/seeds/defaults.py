"""Contains the defaults that should be set up on a new instance."""

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


permission_scheme = {
    'name':        'Default Permission Scheme',
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
    'name': 'Simple Workflow',
    'transitions': {
        'Backlog': [
            {
                'name': 'In Progress',
                'to_status': {
                    'id': 2
                },
                'hooks': [],
            },
        ],
        'In Progress': [
            {
                'name':     'Done',
                'to_status': {
                    'id': 3
                },
                'hooks':    [],
            },
            {
                'name':     'Backlog',
                'to_status': {
                    'id': 1
                },
                'hooks':    [],
            },
        ],
        'Done': [
            {
                'name':     'ReOpen',
                'to_status': {
                    'id': 1
                },
                'hooks':    [],
            },
        ],
    }
}
