class Token:
    def __init__(self, identifier, line_number, value):
        self.identifier = identifier
        self.line_number = line_number
        self.value = value

    def __repr__(self):
        print("{} {} {}".format(self.identifier, self.line_number, self.value))


class DataTypes:
    OPERATORS = {
        "=": "OP_PRIDRUZI",
        "+": "OP_PLUS",
        "-": "OP_MINUS",
        "*": "OP_PUTA",
        "/": "OP_DIJELI"
    }
    KEY_WORDS = {
        "za": "KR_ZA",
        "od": "KR_OD",
        "do": "KR_DO",
        "az": "KR_AZ"
    }
    PARENTHESIS = {
        "(": "L_ZAGRADA",
        ")": "D_ZAGRADA"
    }
    CONSTANTS = {
        "variable": "IDN",
        "number": "BROJ"
    }
    TOKEN_BREAKERS = [" ", "\t"]
    LINE_BREAKERS = ["\n"]


class Lexer:
    def __init__(self, source):
        self.source_code = source
        self.line_number = 0
        self.pointer_position = 0
        self.pointer = None
        self.tokens = []
        self.debug_flag = True

    def debug(self, msg):
        print("DEBUG: {}".format(msg))

    def analyze(self):
        # set up pointer and build token
        self.init_pointer()
        possible_token = ""

        # build possible token by moving the pointer
        while self.pointer != None:
            # debug
            #  if self.debug_flag:
            #      self.debug("Current pointer: '{}'".format(self.pointer))
            # build current possible token
            possible_token += self.pointer
            # process current pointer position
            # TODO comments - bolje, ali ne gotovo
            if self.pointer == "/" and (possible_token == "/" or possible_token[-1] == "/"):
                while self.pointer != '\n':
                    self.move_pointer_next()
                self.process_token(possible_token[:-1])
                possible_token = ""
            # math operators
            elif self.pointer in DataTypes.OPERATORS:
                self.process_token(possible_token[:-1])
                self.process_token(possible_token[-1])
                possible_token = ""
            # parenthesis
            elif self.pointer in DataTypes.PARENTHESIS:
                self.process_token(possible_token[:-1])
                self.process_token(possible_token[-1])
                possible_token = ""
            # new word
            elif self.pointer in DataTypes.TOKEN_BREAKERS:
                self.process_token(possible_token)
                possible_token = ""
            # new line
            elif self.pointer in DataTypes.LINE_BREAKERS:
                self.process_token(possible_token)
                self.line_number += 1
                possible_token = ""
            # move pointer
            self.move_pointer_next()

        # process what's left of token
        self.process_token(possible_token)

    def init_pointer(self):
        if len(self.source_code) >= 1:
            self.pointer_position = 0
            self.pointer = self.source_code[self.pointer_position]
            self.line_number = 1
        else:
            self.line_number = 0
            self.pointer = None

    def move_pointer_next(self):
        if self.pointer_position + 1 < len(self.source_code):
            self.pointer_position += 1
            self.pointer = self.source_code[self.pointer_position]
        else:
            self.pointer = None

    def process_token(self, possible_token):
        if self.debug_flag:
            self.debug("Got token to process: {}".format(possible_token))
        pass


def main():
    source = """
// stavi
n = 10
rez = 0// ovo ignore baci
za i od 1 do n
rez = rez + i+(i * 69) * (123/14 ) *i*i
az
q=12346546756867898707851234123451089766644
"""
    l = Lexer(source)
    l.analyze()


if __name__ == "__main__":
    main()
