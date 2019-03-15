def shunt(infix):
    specials = {'*': 50, '.': 40, '|': 30}

    pofix: str = ""
    stack: str = ""

    for c in infix:
        print("c: ", c, " stack: ", stack, "  postfix: ", pofix)
        if c == '(':
            stack = stack + c
        elif c == ')':

            while stack[-1] != '(':
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack[:-1]
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix, stack = pofix + stack[-1], stack[:-1]
        stack = stack + c
    else:
        pofix = pofix + c

        while stack:
            pofix, stack = pofix + stack[-1], stack[:-1]

    return pofix


print(shunt("a.b+c"))