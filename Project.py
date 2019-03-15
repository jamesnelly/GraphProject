
"""
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
"""
class  state: 
    label = None
    edge1 = None
    edge2 = None

class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(pofix):
    nfastack = []

    for c in pofix:
        if c == '.':
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            nfa1.accept.edge1 = nfa2.initial
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)
        elif c == '|':
             nfa2 = nfastack.pop()
             nfa1 = nfastack.pop()
             initial = state()
             accept = state()
             initial.edge1 = nfa1.initial
             initial.edge2 = nfa2.initial
             accept = state()
             nfa1.accept.edge1 = accept
             nfa2.accept.edge2 = accept
             newnfa = nfa(initial, accept)
             nfastack.append(newnfa)
        elif c == '*':
             nfa1 = nfastack.pop()
             initial = state()
             accept = state()
             initial.edge1 = nfa1.initial
             initial.edge2 = accept
             nfa1.accept.edge1 = nfa1.initial
             nfa1.accept.edge2 = accept
             newnfa = nfa(initial, accept)
             nfastack.append(newnfa)
        else:
            accept = state()
            initial = state()
            initial.label = c
            initial.edge1 = accept
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        return nfastack.pop()

print(compile("ab.cd.|"))