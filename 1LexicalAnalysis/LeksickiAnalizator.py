import sys


class Token:
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
    def __init__(self, source, debug_flag=True):
        self.source_code = source
        self.line_number = 0
        self.pointer_position = 0
        self.pointer = None
        self.tokens = []
        self.debug_flag = debug_flag
        self.init_pointer()

    def debug(self, msg):
        # display debug message
        print("DEBUG: {}".format(msg))

    def get_tokens(self):
        # yield all tokens
        for t in self.tokens:
            yield t

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
                self.process_token(self.pointer)
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

    def is_token_number(self, possible_token):
        # check if token consist only of digits
        is_number = True
        for i in possible_token:
            if i not in DataTypes.DIGITS:
                is_number = False
                break
        return is_number

    def process_token(self, possible_token):
        # debug verbose
        if self.debug_flag:
            self.debug("Got token to process: '{}'".format(possible_token))
        # token is empty or breker
        if len(possible_token) == 0 or possible_token in DataTypes.TOKEN_BREAKERS:
            pass
        # token is new line
        elif possible_token == DataTypes.LINE_BREAKER:
            self.line_number += 1
        # token is operator, find out which one
        elif possible_token in DataTypes.OPERATORS.keys():
            identifier = DataTypes.OPERATORS[possible_token]
            token = Token(identifier, self.line_number, possible_token)
            self.tokens.append(token)
        # token is parenthesis, find out which one
        elif possible_token in DataTypes.PARENTHESIS.keys():
            identifier = DataTypes.PARENTHESIS[possible_token]
            token = Token(identifier, self.line_number, possible_token)
            self.tokens.append(token)
        # token is language keyword
        elif possible_token in DataTypes.KEY_WORDS.keys():
            identifier = DataTypes.KEY_WORDS[possible_token]
            token = Token(identifier, self.line_number, possible_token)
            self.tokens.append(token)
        # token contains only digits
        elif self.is_token_number(possible_token):
            token = Token(DataTypes.NUMBER, self.line_number, possible_token)
            self.tokens.append(token)
        # token must be a variable
        else:
            token = Token(DataTypes.VARIABLE, self.line_number, possible_token)
            self.tokens.append(token)


def main():
    source = sys.stdin.read()

    l = Lexer(source, debug_flag=False)
    l.analyze()

    for token in l.get_tokens():
        print(token)


if __name__ == "__main__":
    main()
