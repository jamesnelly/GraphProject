def shunt(infix):
    # Special characters for regular expressions and their precedence
    # this setups there precedence value
    specials = {'*': 50, '.': 40, '|': 30}

    # Will eventually be the output stack
    pofix = ""
    # Operator stack
    stack = ""
    for c in infix:
        # push the open bracket too the stack
        if c == '(':
            stack = stack + c
            # look at the charchers on the stack and start taking them off
        elif c == ')':
            while stack[-1] != '(':
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack[:-1]
            # want to take was ever is on the stack and put it into
            # the pofix regular expression
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack + c
            # Deals with normal characters in our regular expression
        else:
            pofix = pofix + c
    while stack:
        pofix, stack = pofix + stack[-1], stack[:-1]
    return pofix
# infix regular expression that will be converted to postfix regular expression
print(shunt("(a.b)|(c*.d)"))
print(shunt("(a|b).(a*|b*)"))
print(shunt("(a|b).(a*|b)"))

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

    # nfastack should only have a single nfa on it at this point.    
    return nfastack.pop()

def followes(state):
    ''' Return the set of states that can be reached from state following e arrows.'''
    # Craete a new set, with state as its only member.
    states = set()
    states.add(state)

    # check if state has arrows labelled e from it.
    if state.label is None:
        # Check if edge1 is a state.
        if state.edge1 is not None:
            # If there's an edge1, follow it
            states |= followes(state.edge1)
        # Check if edge2 is a state.
        if state.edge2 is not None:
            # If there's an edge2, follow it.
            states |= followes(state.edge2)
    # Return the set of states
    return states

def match(infix, string):
    # Shunt and compile the regular expression.
    postfix = shunt(infix)
    nfa = compile(postfix)

    # The current set of states and the next set of states.
    current = set()
    next = set()

    # Add the initial state to the current set.
    current |= followes(nfa.initial)

    # Loop through each character in the string.
    for s in string:
        # Loop through the current set of states.
        for c in current:
            # Check if that state is labelled s.
            if c.label == s:
                # Add the edge1 state to the next set.
                next |= followes(c.edge1)
        # Set current to next, and clear out next.
        current = next
        next = set()

    # Check if the accept state is in the set of current states.
    return (nfa.accept in current)

# some tests.
infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
strings = ["", "abc", "abbc", "abcc", "abad", "abbbc"]

for i in infixes:
    for s in strings:
        print(match(i, s), i, s)
# nfastack should only have a single nfa on it at this point.
#print(compile("ab.cd.|"))