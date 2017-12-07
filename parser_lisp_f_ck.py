import ox
import click
import pprint

#Define lexer rules
lisp_lexer = ox.make_lexer([
    ('COMMENT', r';.*'),
    ('NEWLINE', r'\n'),
    ('SPACE', r'\s+'),
    ('NAME', r'[-a-zA-Z]+'),
    ('NUMBER', r'\d+'),
    ('PARENT_OPEN', r'\('),
    ('PARENT_CLOSE', r'\)')
])

#Define tokens
tokens = ['PARENT_CLOSE','PARENT_OPEN','NUMBER','NAME']

#Methods for parser
def name(name):
    return name

def number(number):
    return int(number)

def single_operator(operator):
    return operator

def parent_expr(parent_open, expr, parent_close):
    return expr

def parent(parent_open, parent_close):
    return '()'

def operator_expr(operator, expr):
    return (operator,) + expr

def composed_operator(operator):
    return (operator,)

#Define parser rules
lisp_parser = ox.make_parser([
	('program : PARENT_OPEN expr PARENT_CLOSE', parent_expr),
    ('program : PARENT_OPEN PARENT_CLOSE', parent ),
	('expr : operator expr', operator_expr),
	('expr : operator', composed_operator),
	('operator : program', single_operator),
    ('operator : NAME', name),
    ('operator : NUMBER', number),
], tokens)


#Create tree
@click.command()
@click.argument('source', type=click.File('r'))
def create_tree(source):
    program = source.read()
    tokens = lisp_lexer(program)

    # remove spaces and comments before do parser
    parser_tokens = [token for token in tokens if token.type != 'COMMENT' and token.type != 'SPACE']

    tree = lisp_parser(parser_tokens)

    #print the tree
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(tree)
    return tree

if __name__ == '__main__':
    tree = create_tree()
