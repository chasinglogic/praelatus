"""Lexer, Parser, Interpreter for PQL (Praelatus Query Language)"""
# flake8: noqa

import datetime

import ply.lex as lex
import ply.yacc as yacc
from django.db.models import Q

tokens = (
    'LIST',
    'STRING',
    'NUMBER',
    'DATE',
    'B_OP',
    'U_OP',
    'FIELD',
    'COMPA'
)

t_COMPA = r'startswith|endswith|in|IN|=|[<>]=?|~~?'

literals = '()'
t_ignore = ' \t\n'


def t_LIST(t):
    r'\[(?P<values>.*)\]'
    values = t.lexer.lexmatch.group('values').split(", ")
    if "'" in values[0] or '"' in values[0]:
        t.value = [v.replace('"', '').replace("'", "")
                   for v in values]
    else:
        t.value = [int(v) for v in values]
    return t


def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_DATE(t):
    r'(?P<day>\d{1,2})/(?P<month>\d{1,2})/(?P<year>\d{4})'
    day = int(t.lexer.lexmatch.group('day'))
    month = int(t.lexer.lexmatch.group('month'))
    year = int(t.lexer.lexmatch.group('year'))
    t.value = date(year, month, day)
    return t


def t_B_OP(t):
    r'AND|OR|and|or'
    return t


def t_U_OP(t):
    r'not|NOT'
    return t


def t_FIELD(t):
    r"'?(?P<field>[A-Za-z ]+)'?(?=\s(startswith|endswith|in|=|[<>]=?|~~?))"
    t.value = t.lexer.lexmatch.group('field')
    return t


def t_error(t):
    raise CompileException(u"Cannot make sense of char: %s" % t.value[0])


def make_q(f, compa, v):
    if (f == 'summary' or
        f == 'description' or
        f == 'created_at' or
        f == 'updated_at' or
            f == 'key'):
        field = '%s__%s' % (f, compa)
        return Q(**{field: v})
    elif f == 'project':
        if isinstance(v, int):
            return Q(project__id=v)
        return (Q(project__key=v) |
                Q(project__name=v))
    elif f == 'assignee' or f == 'reporter':
        username = '%s__username__%s' % (f, compa)
        return Q(**{username: v})
    elif f == 'ticket_type' or f == 'status':
        ticket_type = '%s__name__%s' % (f, compa)
        return Q(**{ticket_type: v})
    elif f == 'state':
        state = 'status__state__%s' % compa
        return Q(**{state: v})
    elif f == 'labels':
        return Q(labels__name__in=v)
    # Else we have an actual field field
    value = ''
    if isinstance(v, int):
        value = 'fields__int_value__%s' % compa
    elif isinstance(v, float):
        value = 'fields__flt_value__%s' % compa
    elif isinstance(v, str):
        value = 'fields__str_value__%s' % compa
    elif isinstance(v, datetime.datetime):
        value = 'fields__date_value__%s' % compa
    return (Q(fields__field__name=f) & Q(**{value: v}))



# missing: i* (case insensitive), day&co, isnull
# TODO: range
compa2lookup = {
    '=': 'exact',
    '~': 'contains',
    '~~': 'regex',
    '>': 'gt',
    '>=': 'gte',
    '<': 'lt',
    '<=': 'lte',
    'in': 'in',
    'IN': 'in',
    'startswith': 'startswith',
    'endswith': 'endswith',
}


def p_expression_b_op(p):
    '''expression : expression B_OP expression'''
    if p[2] == 'AND' or p[2] == 'and':
        p[0] = p[1] & p[3]
    elif p[2] == 'OR' or p[2] == 'or':
        p[0] = p[1] | p[3]


def p_expression_u_op(p):
    '''expression : U_OP expression'''
    if p[1] == 'NOT':
        p[0] = ~ p[2]


def p_expression_paren(p):
    "expression : '(' expression ')' "
    p[0] = p[2]


def p_expression_ID(p):
    'expression : FIELD COMPA value'
    lookup = compa2lookup[p[2]]
    p[0] = make_q(str(p[1]), lookup, p[3])


def p_value(p):
    '''value : STRING
            | LIST
            | NUMBER
            | DATE'''
    p[0] = p[1]


def p_error(p):
    if p:
        raise CompileException(u"Parsing error around token: %s" % p.value)
    raise CompileException(u"Parsing error: unexpected end of expression")


precedence = (
    ('left', 'B_OP'),
    ('right', 'U_OP'),
)


class CompileException(Exception):

    def __init__(self, message):
        self.message = message


def compile_q(expr):
    lexer = lex.lex()
    parser = yacc.yacc()
    return parser.parse(expr, lexer=lexer)
