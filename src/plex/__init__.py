from lex import Lex


class MyLanguage(Lex):
    def __init__(self, source_code):
        super().__init__()

        # define the token specification
        self.token_specification = [
            # ('(a)(b)*', 'TEST'),

            ('\n| ( )*', self.count_whitespace),

            # keyword symbols
            (r';', "EOL"),
            (r'\(', "LPAREN"),
            (r'\)', "RPAREN"),
            (r'{', "LBRACE"),
            (r'}', "RBRACE"),
            (r'[', "LBRACKET"),
            (r']', "RBRACKET"),

            # keywords
            (r'if', "IF"),
            (r'else', "ELSE"),
            (r'while', "WHILE"),
            (r'for', "FOR"),
            (r'return', "RETURN"),
            (r'break', "BREAK"),
            (r'continue', "CONTINUE"),

            # operators
            (r'\+', "PLUS"),
            (r'-', "MINUS"),
            (r'\*', "MULTIPLY"),
            (r'/', "DIVIDE"),
            (r'%', "MODULO"),
            (r'\+\+', "INCREMENT"),
            (r'--', "DECREMENT"),
            (r'=', "ASSIGN"),
            (r'\+=', "PLUS_ASSIGN"),
            (r'-=', "MINUS_ASSIGN"),
            (r'\*=', "MULTIPLY_ASSIGN"),
            (r'/=', "DIVIDE_ASSIGN"),
            (r'%=', "MODULO_ASSIGN"),
            (r'==', "EQUAL"),
            (r'!=', "NOT_EQUAL"),
            (r'>', "GREATER_THAN"),
            (r'<', "LESS_THAN"),
            (r'>=', "GREATER_THAN_EQUAL"),
            (r'<=', "LESS_THAN_EQUAL"),
            (r'!', "NOT"),
            (r'&&', "AND"),
            (r'\|\|', "OR"),

            # literals
            (r'(A-Z|a-z|_)(A-Z|a-z|0-9|_)*', "identifier"),
            (r'(0-9)(0-9)*', self.parse_numeric),
            (r'(0-9)(0-9)*\.(0-9)(0-9)*', self.parse_numeric),
        ]

        # user defined variables that may be used
        self.whitespaces = 0

        # run the lexer
        self._tokenize(source_code)

    def count_whitespace(self, token):
        self.whitespaces += 1
        return None

    def parse_numeric(self, token):
        try:
            return "INTEGER: " + str(int(token))
        except ValueError:
            return "FLOAT: " + str(float(token))


if __name__ == '__main__':
    language = MyLanguage('')
    # language.tokenize('')
    # print(language.whitespaces)
