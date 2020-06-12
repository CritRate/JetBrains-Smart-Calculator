def what_to_do(instructions):
    i = instructions.find('Simon says')
    if instructions.startswith('Simon says'):
        return f'I {instructions[i + 11:]}'
    if instructions.endswith('Simon says'):
        return f'I {instructions[:i - 1]}'
    return 'I won\'t do it!'
