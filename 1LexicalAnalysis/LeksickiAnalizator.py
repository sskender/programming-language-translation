import sys


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
    COMMENT = "//"
    TOKEN_BREAKERS = [" ", "\t", "\n"]
    LINE_BREAKER = "\n"
    DIGITS = [str(i) for i in range(10)]
    NUMBER = "BROJ"
    VARIABLE = "IDN"


class Lexer:
    def __init__(self, source):
        self.source_code = source
        self.line_number = 0
        self.pointer_position = 0
        self.pointer = None
        self.tokens = []
        self.debug_flag = True
        self.init_pointer()

    def debug(self, msg):
        # display debug message
        print("DEBUG: {}".format(msg))

    def verify_comment(self, possible_token):
        # given the pointer and current possible token,
        # check if this could be a comment
        # return new value of possible token
        if self.pointer + possible_token[::-1][:1] == DataTypes.COMMENT:
            self.process_token(possible_token[:-1])
            self.process_comment()
            possible_token = ""
        # this is half of a comment, check that later
        else:
            possible_token += self.pointer
        return possible_token

    def analyze(self):
        # move pointer forward and process
        possible_token = ""

        while self.pointer != None:
            # this may be a comment
            if self.pointer == DataTypes.COMMENT[:1]:
                possible_token = self.verify_comment(possible_token)
            # maybe the last false comment was division
            elif possible_token[::-1][:1] == DataTypes.COMMENT[:1]:
                self.process_token(possible_token[:-1])
                self.process_token(possible_token[::-1][:1])
                possible_token = self.pointer
            # this is some kind of an operator
            elif self.pointer in DataTypes.OPERATORS or self.pointer in DataTypes.PARENTHESIS:
                self.process_token(possible_token)
                self.process_token(self.pointer)
                possible_token = ""
            # this is a new token
            elif self.pointer in DataTypes.TOKEN_BREAKERS:
                self.process_token(possible_token)
                possible_token = ""
            # this must be some kind of char coming after a digit
            elif self.pointer not in DataTypes.DIGITS and possible_token[:1] in DataTypes.DIGITS:
                self.process_token(possible_token)
                possible_token = self.pointer
            # this is something else
            else:
                possible_token += self.pointer
            # move pointer forward
            self.move_pointer_next()

        # process what's left of token
        self.process_token(possible_token)

    def init_pointer(self):
        # set pointer to point at the first char
        if len(self.source_code) >= 1:
            self.pointer_position = 0
            self.pointer = self.source_code[self.pointer_position]
            self.line_number = 1
        else:
            self.line_number = 0
            self.pointer = None

    def move_pointer_next(self):
        # move pointer to the next char
        if self.pointer_position + 1 < len(self.source_code):
            self.pointer_position += 1
            self.pointer = self.source_code[self.pointer_position]
        else:
            self.pointer = None

    def process_comment(self):
        # everything is comment till the end of line
        while self.pointer != DataTypes.LINE_BREAKER:
            self.move_pointer_next()

    def process_token(self, possible_token):
        if self.debug_flag:
            self.debug("Got token to process: '{}'".format(possible_token))
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
