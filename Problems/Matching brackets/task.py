import collections

BRACKETS = ['(', ')', '[', ']', '{', '}']

stack = collections.deque()


def find_opposite(b):
    if b == ')':
        return '('
    if b == ']':
        return '['
    return '{'


i = input()
error = False

for s in i:
    if s in BRACKETS:
        if s in '([{':
            stack.append(s)
        else:
            op = find_opposite(s)
            if stack:
                bracket = stack.pop()
                if op != bracket:
                    error = True
            else:
                error = True


if error or len(stack) > 0:
    print('ERROR')
else:
    print('OK')
