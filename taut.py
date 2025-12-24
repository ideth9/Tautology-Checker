

def tokenize(expr):
    # list of appropriate logical symbols
    # not, and, or, implies, biconditional
    symbols = ['~', '^', '|', '>', '=', '(', ')']

    tokens = []
    i = 0
    
    while i < len(expr):
        # Skip spaces
        if expr[i] == ' ':
            i += 1
            continue
        
        # If it's a symbol, add it as a single token
        if expr[i] in symbols:
            tokens.append(expr[i])
            i += 1
        
        # If it's a letter, collect consecutive letters into one token (for variable names)
        elif expr[i].isalpha():
            var_token = ''
            while i < len(expr) and expr[i].isalpha():
                var_token += expr[i]
                i += 1
            tokens.append(var_token)
        
        # Invalid character
        else:
            raise ValueError(f"Invalid Character in Expression: '{expr[i]}'")
    
    print(tokens)
    return tokens 




if __name__ == '__main__':
    # Test cases
    expr1 = 'P ^ Q'
    expr2 = 'VAR ^ PROPOSITION'
    expr3 = '(P | Q) > R'
    
    print("Test 1:", expr1)
    tokenize(expr1)
    
    print("\nTest 2:", expr2)
    tokenize(expr2)
    
    print("\nTest 3:", expr3)
    tokenize(expr3)

