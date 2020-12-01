import sys


class Semantic:
    """
    Semantic analysis for language 'PJ'.

    Semantic errors:
        - undeclared variables
        - using variable out of scope

    Input:
        AST as string from Parser

    Output:
        List of semantic tokens
    """

    def __init__(self, ast_str=None, debug_flag=False):
        self.semantic_tokens = list()
        self.ast_str = ast_str
        self.debug_flag = debug_flag

    def debug(self, msg):
        if self.debug_flag:
            print("DEBUG: {}".format(str(msg)))
        else:
            pass

    def get_tokens(self):
        return self.semantic_tokens

    def analyse(self):
        pass


def main():
    parser_output = sys.stdin.read()

    s = Semantic(parser_output, True)
    s.analyse()

    tokens = s.get_tokens()
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
