

def tokenize(expr):
    # list of appropriate logical symbols
    # not, and, or, implies, biconditional
    symbols = ['~', '&', '|', '>', '=', '(', ')']

    token = []
    for i in expr:
        if i == ' ':
            continue 

        elif i.isalpha() or i in symbols:
          token.append(i)

        else: 
            raise ValueError("Invalid Character in Expression")
    
    print(token)
    return token 




if __name__ == '__main__':
    expr = ('P ^ Q = @')

    tokenize(expr)

