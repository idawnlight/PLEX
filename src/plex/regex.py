from dataclasses import dataclass


@dataclass
class RegexChar:
    char: str = ""
    is_operator: bool = False

    def __init__(self, c: str = "", can_be_operator: bool = True):
        self.char = c
        self.is_operator = can_be_operator and (c == '*' or c == '|' or c == '(' or c == ')' or c == '@')

    def is_operator_char(self, c: str):
        return self.char == c and self.is_operator

    def priority(self):
        if self.char == '(':
            raise Exception("Invalid operator")
        if self.is_operator_char('*'):
            return 3
        if self.is_operator_char('|'):
            return 2
        if self.is_operator_char('@'):
            return 1
        return 0

    def compare(self, other: 'RegexChar'):
        return self.priority() - other.priority()


class RegexExpr:
    def __init__(self, regex: str):
        self._regex = regex
        self._chars: list[RegexChar] = []

        # parse regex range operator
        self._parse_range()
        # convert to list of RegexChar
        self._generate_regex_string()
        # insert connect operator
        self._insert_connect_operator()
        # convert to postfix
        self._to_postfix()

    def get_regex_chars(self):
        return self._chars

    def _parse_range(self):
        _beg = 0
        while True:
            x = self._regex.find('-', _beg)
            if x == -1:
                break
            if x == 0 or x == len(self._regex) - 1:
                _beg = x + 1
                continue
            pre = x - 1
            nxt = x + 1
            if self._regex[pre] == '\\':
                continue
            if self._regex[nxt] == '\\':
                nxt = x + 2
            if self._regex[pre] > self._regex[nxt]:
                raise Exception("Invalid range")
            self._regex = self._regex[:pre] + '|'.join(
                [chr(i) for i in range(ord(self._regex[pre]), ord(self._regex[nxt]) + 1)]) + self._regex[nxt + 1:]

    def _generate_regex_string(self):
        i = 0
        while i < len(self._regex):
            if self._regex[i] == '\\':
                i += 1
                self._chars.append(RegexChar(self._regex[i], False))
            else:
                self._chars.append(RegexChar(self._regex[i], True))
            i += 1

    def _insert_connect_operator(self):
        new_chars: list[RegexChar] = [self._chars[0]]
        for i in range(1, len(self._chars)):
            current_char = self._chars[i]
            previous_char = self._chars[i - 1]
            flag = (
                # case 1: 2 non-operator chars, ab
                    (not previous_char.is_operator and not current_char.is_operator) or
                    # case 2: between non-operator and '(', a(
                    (not previous_char.is_operator and current_char.is_operator_char('(')) or
                    # case 3: between ')' and non-operator, )a
                    (previous_char.is_operator_char(')') and not current_char.is_operator) or
                    # case 4: between '*' and non-operator, *a
                    (previous_char.is_operator_char('*') and not current_char.is_operator) or
                    # case 5: between '*' and '(', *(
                    (previous_char.is_operator_char('*') and current_char.is_operator_char('(')) or
                    # case 6: between ')' and '(', )(
                    (previous_char.is_operator_char(')') and current_char.is_operator_char('('))
            )

            if flag:
                new_chars.append(RegexChar('@'))
            new_chars.append(current_char)

        self._chars = new_chars

    def _to_postfix(self):
        operator_stack: list[RegexChar] = []
        postfix: list[RegexChar] = []
        for c in self._chars:
            if c.is_operator:
                if c.char == '(':
                    operator_stack.append(c)
                elif c.char == ')':
                    while len(operator_stack) > 0 and operator_stack[-1].char != '(':
                        postfix.append(operator_stack.pop())
                    if len(operator_stack) == 0:
                        raise Exception("Invalid regex")
                    operator_stack.pop()
                else:
                    while len(operator_stack) > 0 and not operator_stack[-1].is_operator_char('(') and operator_stack[
                        -1].compare(c) >= 0:
                        postfix.append(operator_stack.pop())
                    operator_stack.append(c)
            else:
                postfix.append(c)
        while len(operator_stack) > 0:
            postfix.append(operator_stack.pop())

        self._chars = postfix
