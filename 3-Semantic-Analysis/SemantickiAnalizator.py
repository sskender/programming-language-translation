import sys


class SemanticToken:
    """ Semantic token data class """

    def __init__(self, ln_usage, ln_definition, value):
        self.ln_usage = ln_usage
        self.ln_definition = ln_definition
        self.value = value

    def __str__(self):
        return f"{self.ln_usage} {self.ln_definition} {self.value}"

    def __repr__(self):
        return f"{self.ln_usage} {self.ln_definition} {self.value}"

    def __eq__(self, obj):
        return isinstance(obj, SemanticToken) and obj.value == self.value


class Keywords:
    OPERATION_LOOP = "<za_petlja>"
    OPERATION_ASSIGN = "<naredba_pridruzivanja>"

    IDN = "IDN"
    KR_ZA = "KR_ZA"
    KR_AZ = "KR_AZ"
    KR_ZA_VALUE = "za"
    KR_AZ_VALUE = "az"


class SemanticException(Exception):
    """
    Custom semantic exception class.

    err <line_number> <value>
    """

    def __init__(self, token, message="Invalid token"):
        self.token = token
        super().__init__(message)

    def __repr__(self):
        return f"err {self.token.ln_usage} {self.token.value}"

    def __str__(self):
        return f"err {self.token.ln_usage} {self.token.value}"


class Semantic:
    """
    Semantic analysis for language 'PJ'.

    Definition (declaration) of variables is saved on context stack.

    There are two types of scopes:
        - global scope
        - local scope inside loop (KR_ZA <local scope> KR_AZ)

    Semantic errors:
        - undeclared variables
        - using variable out of scope

    Input:
        AST as string from Parser

    Output:
        List of semantic tokens
        One semantic token consists of:
            - line number of variable usage
            - line number of variable definition
            - IDN - variable name
    """

    def __init__(self, ast_str=None, debug_flag=False):
        self.semantic_tokens = list()
        self.ast_str = ast_str
        self.debug_flag = debug_flag
        self.context_stack = list()
        self.ast_lines = None
        self.cursor_index = -1
        self.cursor = None
        self.init_analyser()

    def init_analyser(self):
        self.ast_lines = list()
        for line in self.ast_str.split("\n"):
            line = line.strip()
            self.ast_lines.append(line)
        if len(self.ast_lines) > 0:
            self.cursor_index = 0
            self.cursor = self.ast_lines[self.cursor_index]

    def advance(self):
        self.debug(f"advancing from: {self.cursor_index} - {self.cursor}")
        if self.cursor_index + 1 < len(self.ast_lines):
            self.cursor_index += 1
            self.cursor = self.ast_lines[self.cursor_index]
        else:
            self.cursor_index = -1
            self.cursor = None
        self.debug(f"advanced to: {self.cursor_index} - {self.cursor}")

    def debug(self, msg):
        if self.debug_flag:
            print("DEBUG: {}".format(str(msg)))
        else:
            pass

    def get_tokens(self):
        """ This is ouput of semantic analysis """
        return self.semantic_tokens

    def add_semantic_token(self):
        """
        Record usage of an existing variable (identifier IDN)
        in the list of semantic tokens.

        Create semantic token object from current cursor line string.
        Save as semantic token attributes:
            - line in which variable is used
            - line in which variable was defined (read from context stack)
            - name of the variable

        If undeclared variable is being used, raise exception.
        """
        self.debug(f"adding IDN {self.cursor}")
        self.debug(f"tokens before push: {self.semantic_tokens}")
        line_items = self.cursor.strip().split(" ")
        ln_usage = line_items[1]
        idn_value = line_items[2]
        ln_definition = self.find_definition_line_on_stack(idn_value)
        if ln_definition is not None and ln_definition != ln_usage:
            token = SemanticToken(ln_usage, ln_definition, idn_value)
            self.semantic_tokens.append(token)
        else:
            token = SemanticToken(ln_usage, ln_usage, idn_value)
            raise SemanticException(token)
        self.advance()
        self.debug(f"tokens after push: {self.semantic_tokens}")

    def push_to_stack(self):
        """
        Create token object from current cursor line
        and push it to stack.
        """
        self.debug(f"stack before push: {self.context_stack}")
        line_items = self.cursor.strip().split(" ")
        token = SemanticToken(line_items[1], line_items[1], line_items[2])
        self.context_stack.append(token)
        self.debug(f"stack after push: {self.context_stack}")

    def pop_from_stack(self):
        """
        Remove the latest added token object from stack.
        """
        self.debug(f"stack before pop: {self.context_stack}")
        popped = self.context_stack.pop()
        self.debug(f"stack after pop: {self.context_stack}")
        return popped

    def remove_block_scope_from_stack(self):
        """
        Remove all variables definied in the loop scope.

        Variables in loop scope are all variables saved
        on stack between KR_ZA and KR_AZ loop keywords.
        """
        self.debug(f"loop finished - removing scope {self.cursor}")
        while len(self.context_stack) > 0 and \
                self.context_stack[-1].value != Keywords.KR_ZA_VALUE:
            self.pop_from_stack()
        self.pop_from_stack()
        self.advance()

    def find_definition_line_on_stack(self, idn_value):
        """
        Check if variable being used is defined.
        (saved on context stack)
        Return line of definition required to create SemanticToken object
        """
        self.debug("trying to find on stack: " + str(idn_value))
        for item in self.context_stack[::-1]:
            if item.value == idn_value:
                return item.ln_definition
        return None

    def analyse(self):
        while self.cursor is not None:
            if self.cursor == Keywords.OPERATION_ASSIGN:
                self.operation_compound()
            elif self.cursor == Keywords.OPERATION_LOOP:
                self.operation_loop()
            elif Keywords.IDN in self.cursor:
                self.add_semantic_token()
            elif Keywords.KR_AZ in self.cursor:
                self.remove_block_scope_from_stack()
            else:
                self.advance()

    def operation_compound(self):
        """
        Save variable (IDN) definition to context stack.

        NOTE:
        If a variable is already defined in the same scope,
        (token already pushed to stack) -
        don't rewrite it - keep the original declaration.
        """
        self.debug("assign op: " + self.cursor)
        self.advance()
        line_items = self.cursor.strip().split(" ")
        token = SemanticToken(line_items[1], line_items[1], line_items[2])
        token_on_stack = False
        for item in self.context_stack[::-1]:
            if item == token:
                token_on_stack = True
                break
        if not token_on_stack:
            self.push_to_stack()
        self.advance()

    def operation_loop(self):
        """
        Save new scope to stack (KR_ZA)
        and the following scope variable.
        """
        self.debug("loop op: " + self.cursor)
        self.advance()
        self.push_to_stack()
        self.advance()
        self.push_to_stack()
        self.advance()


def main():
    parser_output = sys.stdin.read()

    s = Semantic(parser_output, False)

    try:
        s.analyse()
        for token in s.get_tokens():
            print(token)
    except SemanticException as e:
        for token in s.get_tokens():
            print(token)
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
