import string
from collections import deque


def is_digit(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_variable(s):
    validate = [True if x in string.ascii_letters else False for x in s]
    if False in validate:
        return False
    return True


def is_valid(s):
    return is_digit(s) or is_variable(s)


def higher_precedence(top_of_stack, current_operand):
    precedence = {
        '+': '',
        '-': '',
        '*': ['+', '-'],
        '/': ['+', '-'],
        '(': ['+', '-', '*', '-'],
        ')': ['+', '-', '*', '-']
    }

    if top_of_stack in precedence[current_operand]:
        return True
    return False


class Calculator:

    def __init__(self):
        self.variables = {}
        self.exp = None

    def calculate(self):
        self.infix_to_postfix_notation()

        if not self.exp:
            return

        stack = deque()
        result = None

        for el in self.exp:
            if is_digit(el):
                stack.append(int(el))
            else:
                if stack:
                    var_one = stack.pop()
                else:
                    print('Invalid expression')
                    break
                if stack:
                    var_two = stack.pop()
                else:
                    print('Invalid expression')
                    break
                if el == '*':
                    result = var_one * var_two
                elif el == '/':
                    result = var_two / var_one
                elif el == '+':
                    result = var_one + var_two
                elif el == '-':
                    result = var_two - var_one
                stack.append(result)

        if result:
            print(int(result))

    def infix_to_postfix_notation(self):
        stack = deque()
        result = []

        for el in self.exp:
            if el in '+-*/()':
                # if the stack is empty or you see left parenthesis add operand to the stack
                if not stack or stack[-1] == '(':
                    stack.append(el)
                elif el == ')':
                    # add operand to the result until you see left parenthesis
                    while stack and stack[-1] != '(':
                        result.append(stack.pop())
                    # remove the parenthesis from the stack
                    if stack:
                        stack.pop()
                    else:
                        stack.append(el)
                        break
                # left parenthesis add to the top of stack
                elif el == '(':
                    stack.append(el)
                # if current operand has higher precedence put it on top of stack
                elif higher_precedence(stack[-1], el):
                    stack.append(el)
                else:
                    # current operand has lower or equal precedence
                    result.append(stack.pop())
                    # add operands to the result if top of the stack has lower precedence
                    while stack and stack[-1] != '(' and not higher_precedence(stack[-1], el):
                        result.append(stack.pop())
                    stack.append(el)
            else:
                if el in self.variables:
                    result.append(self.variables[el])
                else:
                    result.append(el)

        # at the end add all operands to the result
        while stack:
            op = stack.pop()
            if '(' in op or ')' in op:
                print('Invalid expression')
                self.exp = None
                return None
            result.append(op)

        self.exp = result

    def assign(self):
        if len(self.exp) > 3:
            print('Invalid assignment')
        if is_variable(self.exp[0]):
            if is_valid(self.exp[1]):
                # reassigning variable to another one
                if self.exp[1] in self.variables:
                    self.variables[self.exp[0]] = self.variables[self.exp[1]]
                # creating new variable
                else:
                    self.variables[self.exp[0]] = int(self.exp[1])
            else:
                print('Invalid assignment')
        else:
            print('Invalid identifier')

    def print_variable(self):
        if is_digit(''.join(self.exp)):
            print(int(''.join(self.exp)))
        else:
            print(self.variables.get(self.exp[0], 'Unknown variable'))

    def execute(self, exp):
        valid = self.sanitize(exp)

        if valid:
            operation = self.evaluate()

            if operation == 'ASSIGMENT':
                self.assign()
            if operation == 'CALCULATE':
                self.calculate()
            if operation == 'PRINTING':
                self.print_variable()

    def evaluate(self):
        if '=' in self.exp:
            return 'ASSIGMENT'
        elif len(self.exp) < 3:
            return 'PRINTING'
        else:
            return 'CALCULATE'

    def sanitize(self, exp):
        # 'n=5', 'n= 5', 'n =5' -> ['n', '5', '=]
        if '=' in exp:
            self.exp = [s.strip() for s in exp.split('=')]
            self.exp.append('=')
        else:
            number = ''
            result = ''
            for s in exp:
                if is_valid(s):
                    number += s
                    continue
                if number:
                    result += f' {number} '
                    number = ''
                    if s:
                        result += f'{s} '
                else:
                    if s == '(':
                        result += f'{s} '
                    else:
                        result += s
            if number:
                result += f' {number} '
            result = result.split()
            for index, value in enumerate(result):
                if '+' in value:
                    result[index] = '+'
                if '-' in value:
                    result[index] = '+' if len(value) % 2 == 0 else '-'
            self.exp = result
        return True


if __name__ == '__main__':
    calc = Calculator()

    while True:
        i = input()

        if len(i) == 0:
            continue
        if i == '/help':
            print('Smart calculator - /exit to quit')
            continue
        if i == '/exit':
            print('Bye!')
            break
        if i.startswith('/'):
            print('Unknown command')
            continue

        calc.execute(i)
