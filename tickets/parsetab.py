
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "leftB_OPrightU_OPLIST STRING NUMBER DATE B_OP U_OP FIELD COMPAexpression : expression B_OP expressionexpression : U_OP expressionexpression : '(' expression ')' expression : FIELD COMPA valuevalue : STRING\n            | LIST\n            | NUMBER\n            | DATE"

_lr_action_items = {')': ([5, 7, 9, 10, 11, 12, 13, 14, 15, ], [-2, 14, -6, -4, -5, -8, -7, -3, -1, ]), 'U_OP': ([0, 1, 3, 8, ], [1, 1, 1, 1, ]), '$end': ([4, 5, 9, 10, 11, 12, 13, 14, 15, ], [0, -2, -6, -4, -5, -8, -7, -3, -1, ]), 'FIELD': ([0, 1, 3, 8, ], [2, 2, 2, 2, ]
                                                                                                                                                                                                                                                  ), 'STRING': ([6, ], [11, ]), 'COMPA': ([2, ], [6, ]), '(': ([0, 1, 3, 8, ], [3, 3, 3, 3, ]), 'DATE': ([6, ], [12, ]), 'B_OP': ([4, 5, 7, 9, 10, 11, 12, 13, 14, 15, ], [8, -2, 8, -6, -4, -5, -8, -7, -3, -1, ]), 'LIST': ([6, ], [9, ]), 'NUMBER': ([6, ], [13, ]), }

_lr_action = {}
for _k, _v in _lr_action_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_action:
            _lr_action[_x] = {}
        _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'value': ([6, ], [10, ]), 'expression': (
    [0, 1, 3, 8, ], [4, 5, 7, 15, ]), }

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_goto:
            _lr_goto[_x] = {}
        _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
    ("S' -> expression", "S'", 1, None, None, None),
    ('expression -> expression B_OP expression',
        'expression', 3, 'p_expression_b_op', 'queries.py', 113),
    ('expression -> U_OP expression', 'expression',
        2, 'p_expression_u_op', 'queries.py', 121),
    ('expression -> ( expression )', 'expression',
        3, 'p_expression_paren', 'queries.py', 127),
    ('expression -> FIELD COMPA value', 'expression',
        3, 'p_expression_ID', 'queries.py', 132),
    ('value -> STRING', 'value', 1, 'p_value', 'queries.py', 138),
    ('value -> LIST', 'value', 1, 'p_value', 'queries.py', 139),
    ('value -> NUMBER', 'value', 1, 'p_value', 'queries.py', 140),
    ('value -> DATE', 'value', 1, 'p_value', 'queries.py', 141),
]
