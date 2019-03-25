
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
# Represents a state with two arrows, labelled by a label
# Use None for a label representing "e" arrows.
class  state: 
    label = None
    edge1 = None
    edge2 = None
# An NFA is represented by its initial and accept states.
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
            # POP two NFA's off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # Connect first NFA's accept state to the secods's initial.
            nfa1.accept.edge1 = nfa2.initial
            # Push NFA to the stack
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)
        elif c == '|':
            # POP two NFA's off the stack.
             nfa2 = nfastack.pop()
             nfa1 = nfastack.pop()
             # Create a new initial state, connect it to initial states
             # of the two NFA's popped from the stck
             initial = state()
             accept = state()
             initial.edge1 = nfa1.initial
             initial.edge2 = nfa2.initial
             # Create a new accept state, connecting the accept states
             # of the two NFA's popped from the stack, to the new state.
             accept = state()
             nfa1.accept.edge1 = accept
             nfa2.accept.edge2 = accept
             # Push a new NFA to the stack
             newnfa = nfa(initial, accept)
             nfastack.append(newnfa)
        elif c == '*':
             #  Pop a single NFA from the stack
             nfa1 = nfastack.pop()
             # Create new initial and accept states.
             initial = state()
             accept = state()
             # Join the new initial state to the nfa1's initial state and the new accept state
             initial.edge1 = nfa1.initial
             initial.edge2 = accept
             # Join the old accept state to the new accept state and nfa1's initial state
             nfa1.accept.edge1 = nfa1.initial
             nfa1.accept.edge2 = accept
             # Push new NFA to the stack
             newnfa = nfa(initial, accept)
             nfastack.append(newnfa)
        else:
            # Create a new initial and accept states.
            accept = state()
            initial = state()
            # Join the initial state the accept state using an arrow labelled c.
            initial.label = c
            initial.edge1 = accept
            # Push new NFA to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        return nfastack.pop()
# nfastack should only have a single nfa on it at this point.
print(compile("ab.cd.|"))