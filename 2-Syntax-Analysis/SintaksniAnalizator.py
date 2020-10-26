import sys


class Grammar:
    """
    'PJ' GRAMMAR

    Grammar table of language 'PJ'


    <program> ::= <lista_naredbi> = { IDN KR_ZA ⏊ }

    <lista_naredbi> ::= <naredba> <lista_naredbi> = { IDN KR_ZA }
    <lista_naredbi> ::= $ = { KR_AZ ⏊ }

    <naredba> ::= <naredba_pridruzivanja> = { IDN }
    <naredba> ::= <za_petlja> = { KR_ZA }

    <naredba_pridruzivanja> ::= IDN OP_PRIDRUZI <E> = { IDN }
    <za_petlja> ::= KR_ZA IDN KR_OD <E> KR_DO <E> <lista_naredbi> KR_AZ = { KR_ZA }

    <E> ::= <T> <E_lista> = { IDN BROJ OP_PLUS OP_MINUS L_ZAGRADA }

    <E_lista> ::= OP_PLUS <E> = { OP_PLUS }
    <E_lista> ::= OP_MINUS <E> = { OP_MINUS }
    <E_lista> ::= $ = { IDN KR_ZA KR_DO KR_AZ D_ZAGRADA ⏊ }

    <T> ::= <P> <T_lista> = { IDN BROJ OP_PLUS OP_MINUS L_ZAGRADA }

    <T_lista> ::= OP_PUTA <T> = { OP_PUTA }
    <T_lista> ::= OP_DIJELI <T> = { OP_DIJELI }
    <T_lista> ::= $ = { IDN KR_ZA KR_DO KR_AZ OP_PLUS OP_MINUS D_ZAGRADA ⏊ }

    <P> ::= OP_PLUS <P> = { OP_PLUS }
    <P> ::= OP_MINUS <P> = { OP_MINUS }
    <P> ::= L_ZAGRADA <E> D_ZAGRADA = { L_ZAGRADA }
    <P> ::= IDN = { IDN }
    <P> ::= BROJ = { BROJ }
    """

    """ Language token identifiers and grammar stored in variables and lists """

    """ Default token identifiers <class Token> """
    IDN = "IDN"
    KR_ZA = "KR_ZA"
    KR_OD = "KR_OD"
    KR_DO = "KR_DO"
    KR_AZ = "KR_AZ"
    OP_PRIDRUZI = "OP_PRIDRUZI"
    OP_PLUS = "OP_PLUS"
    OP_MINUS = "OP_MINUS"
    OP_PUTA = "OP_PUTA"
    OP_DIJELI = "OP_DIJELI"
    L_ZAGRADA = "L_ZAGRADA"
    D_ZAGRADA = "D_ZAGRADA"

    """ List of valid operations <lista_naredbi> """
    OPERATIONS_LIST_VALID_OPTIONS = ["IDN", "KR_ZA", "KR_AZ", None]
    OPERATIONS_LIST_VALID_END_OPTIONS = ["KR_AZ", None]

    """ Expressions table <E> and expressions list table <E_lista> """
    EXPRESSION_VALID_OPTIONS = ["IDN", "BROJ",
                                "OP_PLUS", "OP_MINUS", "L_ZAGRADA"]
    EXPRESSION_LIST_VALID_END_OPTIONS = [
        "IDN", "KR_ZA", "KR_DO", "KR_AZ", "D_ZAGRADA", None]
    EXPRESSION_LIST_VALID_OPTIONS = [
        "OP_PLUS", "OP_MINUS"] + EXPRESSION_LIST_VALID_END_OPTIONS

    """ Terms table <T> and terms list table <T_lista> """
    TERM_VALID_OPTIONS = ["IDN", "BROJ", "OP_PLUS", "OP_MINUS", "L_ZAGRADA"]
    TERM_LIST_VALID_END_OPTIONS = ["IDN", "KR_ZA", "KR_DO",
                                   "KR_AZ", "OP_PLUS", "OP_MINUS", "D_ZAGRADA", None]
    TERM_LIST_VALID_OPTIONS = ["OP_PUTA",
                               "OP_DIJELI"] + TERM_LIST_VALID_END_OPTIONS

    """ Primaries table <P> """
    PRIMARY_VALID_OPTIONS = ["OP_PLUS", "OP_MINUS", "L_ZAGRADA", "IDN", "BROJ"]
    PRIMARY_VALID_END_OPTIONS = ["IDN", "BROJ"]


class Token:
    """ Token data class """

    def __init__(self, identifier, line_number, value):
        self.identifier = identifier
        self.line_number = line_number
        self.value = value

    def __repr__(self):
        return "{} {} {}".format(self.identifier,
                                 self.line_number, self.value)

    def __str__(self):
        return "{} {} {}".format(self.identifier,
                                 self.line_number, self.value)


class AST:
    """ Abstract syntax tree """

    def __init__(self, node_name, node_children=[]):
        self.node_name = node_name
        self.node_children = node_children

    def __repr__(self, margin_size=0):
        s = f"{' '*margin_size}{self.node_name}\n"
        if len(self.node_children) == 0 or self.node_children[0] is None:
            s += f"{' '*margin_size} $\n"
        else:
            for child in self.node_children:
                if isinstance(child, Token):
                    s += f"{' '*margin_size} {child.__repr__()}\n"
                else:
                    s += f"{child.__repr__(margin_size+1)}"
        return s

    def __str__(self):
        return self.__repr__()


class ParserException(Exception):
    """
    Custom parser exception class

    Parsing exception as invalid token or invalid end of file:
        err <identifier> <line_number> <value>
        err kraj
    """

    def __init__(self, token, message="Invalid token"):
        self.token_string = str(token) if token is not None else "kraj"
        super().__init__(message)

    def __repr__(self):
        return f"err {self.token_string}"

    def __str__(self):
        return f"err {self.token_string}"


class Parser:
    """ Language 'PJ' parser """

    def __init__(self, tokens, debug_flag=False):
        self.tokens = tokens
        self.debug_flag = debug_flag
        self.total_tokens = 0
        self.current_token_index = -1
        self.current_token = None
        self.ast_root = None

    def debug(self, msg):
        if self.debug_flag:
            print("DEBUG: {}".format(str(msg)))
        else:
            pass

    def print_ast_tree(self):
        """ Print the whole AST program tree """
        print(self.ast_root, end="")

    def init_parser(self):
        """ Initialize parser to eat the first token """
        if len(self.tokens) >= 1:
            self.total_tokens = len(self.tokens)
            self.current_token_index = 0
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def advance(self):
        """ Eat the next token """
        self.debug(f"advancing from: {self.current_token}")

        if self.current_token_index + 1 < len(self.tokens):
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

        self.debug(f"advanced to: {self.current_token}")

    def parse(self):
        """ Generate AST tree """
        self.init_parser()

        program_tree = self.program()
        self.ast_root = program_tree

    def program(self):
        """
        Program: <program>

        Options:
            <lista_naredbi> = {IDN KR_ZA ⏊}
        """
        self.debug("program starting: {}".format(self.current_token))

        # empty program, so return empty tree
        if self.current_token is None:
            tree_children = [None]
            return AST("<program>", tree_children)

        # program start is valid
        elif self.current_token.identifier == Grammar.IDN or \
                self.current_token.identifier == Grammar.KR_ZA:
            operations_list_tree = self.operations_list()

            tree_children = [operations_list_tree]
            return AST("<program>", tree_children)

        # invalid program start
        else:
            raise ParserException(self.current_token)

    def operations_list(self):
        """
        List of operations: <lista_naredbi>

        Options:
            <naredba> <lista_naredbi> = {IDN KR_ZA}
            $ = {KR_AZ ⏊}
        """
        self.debug("operations list: {}".format(self.current_token))

        # end reached
        if self.current_token is None or self.current_token.identifier == Grammar.KR_AZ:
            tree_children = [None]
            return AST("<lista_naredbi>", tree_children)

        # identifier or loop
        elif self.current_token.identifier == Grammar.IDN or \
                self.current_token.identifier == Grammar.KR_ZA:
            operation_tree = self.operation()
            operations_list_tree = self.operations_list()

            tree_children = [operation_tree, operations_list_tree]
            return AST("<lista_naredbi>", tree_children)

        # invalid token
        else:
            raise ParserException(self.current_token)

    def operation(self):
        """
        Operation: <naredba>

        Options:
            <naredba_pridruzivanja> = {IDN}
            <za_petlja> = {KR_ZA}
        """
        self.debug("operation {}".format(self.current_token))

        if self.current_token is None:
            raise ParserException(self.current_token)

        # identifier token
        if self.current_token.identifier == Grammar.IDN:
            compound_tree = self.operation_compound()

            tree_children = [compound_tree]
            return AST("<naredba>", tree_children)

        # loop start token
        elif self.current_token.identifier == Grammar.KR_ZA:
            loop_tree = self.operation_loop()

            tree_children = [loop_tree]
            return AST("<naredba>", tree_children)

        # invalid token
        else:
            raise ParserException(self.current_token)

    def operation_compound(self):
        """
        Operation compound: <naredba_pridruzivanja>

        Options:
            IDN OP_PRIDRUZI <E> = {IDN}
        """
        self.debug("operation compound: {}".format(self.current_token))

        left_token = self.current_token
        self.advance()

        if self.current_token is None or self.current_token.identifier != Grammar.OP_PRIDRUZI:
            raise ParserException(self.current_token)
        operation = self.current_token
        self.advance()

        right_tree = self.expression()

        tree_children = [left_token, operation, right_tree]
        return AST("<naredba_pridruzivanja>", tree_children)

    def operation_loop(self):
        """
        Operation loop: <za_petlja>

        Options:
            KR_ZA IDN KR_OD <E> KR_DO <E> <lista_naredbi> KR_AZ = { KR_ZA }
        """
        self.debug("operation loop: {}".format(self.current_token))

        loop_definition_start = self.current_token
        self.advance()

        if self.current_token is None or self.current_token.identifier != Grammar.IDN:
            raise ParserException(self.current_token)
        identifier = self.current_token
        self.advance()

        if self.current_token is None or self.current_token.identifier != Grammar.KR_OD:
            raise ParserException(self.current_token)
        loop_start = self.current_token
        self.advance()

        expression_start = self.expression()

        if self.current_token is None or self.current_token.identifier != Grammar.KR_DO:
            raise ParserException(self.current_token)
        loop_finish = self.current_token
        self.advance()

        expression_finish = self.expression()
        operations_list = self.operations_list()

        if self.current_token is None or self.current_token.identifier != Grammar.KR_AZ:
            raise ParserException(self.current_token)
        loop_definition_end = self.current_token
        self.advance()

        tree_children = [loop_definition_start, identifier, loop_start, expression_start,
                         loop_finish, expression_finish, operations_list, loop_definition_end]
        return AST("<za_petlja>", tree_children)

    def expression(self):
        """
        Expression: <E>

        Options:
            <T> <E_lista> = { IDN BROJ OP_PLUS OP_MINUS L_ZAGRADA }
        """
        self.debug("expression: {}".format(self.current_token))

        # invalid token
        if self.current_token is None or \
                self.current_token.identifier not in Grammar.EXPRESSION_VALID_OPTIONS:
            raise ParserException(self.current_token)

        t_tree = self.term()
        e_list_tree = self.expression_list()

        tree_children = [t_tree, e_list_tree]
        return AST("<E>", tree_children)

    def expression_list(self):
        """
        Expression list: <E_lista>

        Options:
            OP_PLUS <E> = { OP_PLUS }
            OP_MINUS <E> = { OP_MINUS }
            $ = { IDN KR_ZA KR_DO KR_AZ D_ZAGRADA ⏊ }
        """
        self.debug("expression list: {}".format(self.current_token))

        # end reached
        if self.current_token is None or \
                self.current_token.identifier in Grammar.EXPRESSION_LIST_VALID_END_OPTIONS:
            tree_children = [None]
            return AST("<E_lista>", tree_children)

        # invalid token
        if self.current_token.identifier not in Grammar.EXPRESSION_LIST_VALID_OPTIONS:
            raise ParserException(self.current_token)

        # OP_PLUS or OP_MINUS reached
        elif self.current_token.identifier == Grammar.OP_PLUS or \
                self.current_token.identifier == Grammar.OP_MINUS:
            plus_minus_token = self.current_token
            self.advance()

            e_tree = self.expression()

            tree_children = [plus_minus_token, e_tree]
            return AST("<E_lista>", tree_children)

        # should never come here
        else:
            raise ParserException(self.current_token)

    def term(self):
        """
        Term: <T>

        Options:
            <P> <T_lista> = { IDN BROJ OP_PLUS OP_MINUS L_ZAGRADA }
        """
        self.debug("term: {}".format(self.current_token))

        # invalid token
        if self.current_token is None or \
                self.current_token.identifier not in Grammar.TERM_VALID_OPTIONS:
            raise ParserException(self.current_token)

        p_tree = self.primary()
        t_list_tree = self.term_list()

        tree_children = [p_tree, t_list_tree]
        return AST("<T>", tree_children)

    def term_list(self):
        """
        Term list: <T_lista>

        Options:
            OP_PUTA <T> = { OP_PUTA }
            OP_DIJELI <T> = { OP_DIJELI }
            $ = { IDN KR_ZA KR_DO KR_AZ OP_PLUS OP_MINUS D_ZAGRADA ⏊ }
        """
        self.debug("term list: {}".format(self.current_token))

        # end reached
        if self.current_token is None or \
                self.current_token.identifier in Grammar.TERM_LIST_VALID_END_OPTIONS:
            tree_children = [None]
            return AST("<T_lista>", tree_children)

        # invalid token
        if self.current_token.identifier not in Grammar.TERM_LIST_VALID_OPTIONS:
            raise ParserException(self.current_token)

        # OP_PUTA or OP_DIJELI reached
        elif self.current_token.identifier == Grammar.OP_PUTA or \
                self.current_token.identifier == Grammar.OP_DIJELI:
            mul_div_token = self.current_token
            self.advance()

            p_tree = self.term()

            tree_children = [mul_div_token, p_tree]
            return AST("<T_lista>", tree_children)

        # should never come here
        else:
            raise ParserException(self.current_token)

    def primary(self):
        """
        Primary: <P>

        Options:
            OP_PLUS <P> = { OP_PLUS }
            OP_MINUS <P> = { OP_MINUS }
            L_ZAGRADA <E> D_ZAGRADA = { L_ZAGRADA }
            IDN = { IDN }
            BROJ = { BROJ }
        """
        self.debug("primary: {}".format(self.current_token))

        # invalid token
        if self.current_token is None or \
                self.current_token.identifier not in Grammar.PRIMARY_VALID_OPTIONS:
            raise ParserException(self.current_token)

        # end reached
        if self.current_token.identifier in Grammar.PRIMARY_VALID_END_OPTIONS:
            end_token = self.current_token
            self.advance()

            tree_children = [end_token]
            return AST("<P>", tree_children)

        # OP_PLUS or OP_MINUS reached
        elif self.current_token.identifier == Grammar.OP_PLUS or \
                self.current_token.identifier == Grammar.OP_MINUS:
            plus_minus_token = self.current_token
            self.advance()

            p_tree = self.primary()

            tree_children = [plus_minus_token, p_tree]
            return AST("<P>", tree_children)

        # L_ZAGRADA reached, advance to expression
        elif self.current_token.identifier == Grammar.L_ZAGRADA:
            # left parenthesis
            l_paren_token = self.current_token
            self.advance()

            expression_tree = self.expression()

            # right parenthesis
            if self.current_token is None or \
                    self.current_token.identifier != Grammar.D_ZAGRADA:
                raise ParserException(self.current_token)
            r_paren_token = self.current_token
            self.advance()

            tree_children = [l_paren_token, expression_tree, r_paren_token]
            return AST("<P>", tree_children)

        # should never come here
        else:
            raise ParserException(self.current_token)


def main():
    tokens = []

    lexer_output = sys.stdin.read()
    for line in lexer_output.split("\n"):
        try:
            (identifier, line_number, value) = line.split(" ")
            tokens.append(Token(identifier, line_number, value))
        except Exception:
            break

    parser = Parser(tokens, debug_flag=False)

    try:
        parser.parse()
        parser.print_ast_tree()
    except ParserException as e:
        print(e)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
