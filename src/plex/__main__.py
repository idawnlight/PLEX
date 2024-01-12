import dill

from lex import Lex

test_input = """
int main() {
    float p    = 1.1;
    int   i    = 2;
    int   loop = 0;
    int   a[10][10];
    int   x;
    while (loop == 0 && i <= 10) {
        int j = 1;
        while (loop == 0 && j < i)
            if (a[i][j] == x)
                loop = 1;
            else
                j = j + 1;
        if (loop == 0)
            i = i + 1;
    }
}
"""

class MyLanguage(Lex):
    def __init__(self):
        super().__init__()

        # define the token specification
        self.token_specification = [
            # ('(a)(b)*', 'TEST'),
            # ('/', 'TEST2'),

            ('\n| ( )*', self.count_whitespace),

            # keyword symbols
            (r';', "EOL"),
            (r'\(', "LPAREN"),
            (r'\)', "RPAREN"),
            (r'{', "LBRACE"),
            (r'}', "RBRACE"),
            (r'[', "LBRACKET"),
            (r']', "RBRACKET"),

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
            (r'(A-Z|a-z|_)(A-Z|a-z|0-9|_)*', self.identifier),
            (r'(0-9)(0-9)*', self.parse_numeric),
            (r'(0-9)(0-9)*\.(0-9)(0-9)*', self.parse_numeric),
        ]

        # user defined variables that may be used
        self.whitespaces = 0

        # init the lexer, generate MinimalDFA
        self._init()

    def count_whitespace(self, token):
        self.whitespaces += 1
        return None

    def parse_numeric(self, token):
        try:
            return "INTEGER: " + str(int(token))
        except ValueError:
            return "FLOAT: " + str(float(token))

    def identifier(self, token):
        if token in ["if", "else", "while", "for", "return", "break", "continue"]:
            return "KEYWORD: " + token
        if token in ['int', 'float', 'char', 'void']:
            return "TYPE: " + token
        return "IDENTIFIER: " + token


if __name__ == '__main__':
    language = MyLanguage()
    dill.dump(language, open("language.p", "wb"))

    # language = dill.load(open("language.p", "rb"))

    language.tokenize(test_input)
    # language.tokenize("main while else if")
    print("\nAfter tokenize, whitespaces counted: " + str(language.whitespaces))
