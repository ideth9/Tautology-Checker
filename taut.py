from taut_test import *

def tokenize(expr):
    """
    Takes a logical expression string and breaks it into tokens.
    
    Goes through the string and separates it into operators, variables, and parentheses. 
    Groups letters together for variable names and ignores spaces.
    
    Returns list of tokens. 
    """
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


class Node:
    """
    A node in the expression tree.
    """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class Parser:
    """
    Parses tokens into an expression tree.
    Uses recursive descent parsing. 
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0
    
    def parse(self):
        """
        Main parsing function which takes the tokens and builds the expression tree
        and returns the root node of the tree.
        """
        self.current_index = 0
        tree = self.parse_expression()
        if self.current_index != len(self.tokens):
            raise ValueError(f"Unexpected tokens at end: {self.tokens[self.current_index:]}")
        return tree
    
    def parse_expression(self):
        """
        Parses biconditional expressions (=).
        This is the lowest precedence, so it's called first. 
        """
        left = self.parse_implies()

        while self.current_token() == '=':
            operator = self.consume('=')
            right = self.parse_implies()
            left = Node(operator, left, right)

        return left
    
    def parse_implies(self):
        """
        Parses implication expressions (>).
        """
        left = self.parse_or()
        
        while self.current_token() == '>':
            operator = self.consume('>')
            right = self.parse_or()
            left = Node(operator, left, right)

        return left
    
    def parse_or(self):
        """
        Parses OR expressions (|).
        """
        left = self.parse_and()

        while self.current_token() == '|':
            operator = self.consume('|')
            right = self.parse_and()
            left = Node(operator, left, right)

        return left 

    def parse_and(self):
        """
        Parses AND expressions (^).
        """
        left = self.parse_not()

        while self.current_token() == '^':
            operator = self.consume('^')
            right = self.parse_not()
            left = Node(operator, left, right)

        return left 
    
    def parse_not(self):
        """
        Parses NOT expressions (~) and has the highest precedence. 
        Handle double negation like ~~P.
        """
        if self.current_token() == '~':
            operator = self.consume('~')
            operand = self.parse_not()

            return Node(operator, operand, None)

        else:
            return self.parse_atom()
    
    def parse_atom(self):
        """
        Parses the variables or things in parentheses.
        If it sees a variable name, it makes a node for it. If it sees
        a parenthesis, it parses what's inside and then expects a closing parentheses.
        """
        if self.current_token() == '(':
            self.consume('(')
            expr = self.parse_expression()
            self.consume(')')

            return expr

        elif self.current_token().isalpha():
            var_name = self.consume()

            return Node(var_name, None, None)

        else:
            raise ValueError(f"Unexpected token: {self.current_token()}") 
    
    def consume(self, expected_token=None):
        """
        Eats the current token and moves forward.
        If you give it an expected_token, it checks that the current token
        matches before consuming it. If you don't give one (None), it just
        takes whatever token is there (useful for variables).
        """
        if expected_token is None:
            if self.current_token() is None:
                raise ValueError("Unexpected end of tokens")
            value = self.current_token()
            self.current_index += 1

            return value
        
        elif self.current_token() == expected_token:
            value = self.current_token()
            self.current_index += 1

            return value 
        
        else:
            raise ValueError(f"Expected {expected_token} but got {self.current_token()}")
    
    def current_token(self):
        """
        Looks at the current token without eating it.
        Returns the token, or None if we're at the end of the token list.
        """
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        
        return None


def extract_variables(node):
    """
    Finds all unique variables in an expression tree.
    Goes through the tree recursively and collects all variable names
    and returns a set of variable names.
    """
    variables = set()

    if node is None:
        return variables

    # If this is a leaf node (both children are None), it's a variable
    if node.left is None and node.right is None:
        if node.value not in ['~', '^', '|', '>', '=']:
            variables.add(node.value)

    # Otherwise, it's an operator, so recursively check children
    else:
        # check left child
        if node.left is not None:
            left_v = extract_variables(node.left)
            variables.update(left_v)

        # check right child
        if node.right is not None:
            right_v = extract_variables(node.right)
            variables.update(right_v)

    # return
    return variables


def print_tree(node, indent=""):
    """
    Prints out the tree structure.
    """
    if node is None:
        return
    
    if node.right is not None:
        print_tree(node.right, indent + "   ")
    
    print(indent + str(node.value))
    
    if node.left is not None:
        print_tree(node.left, indent + "   ")


if __name__ == '__main__':
    # Test tokenizer
    print("=" * 60)
    print("TOKENIZER TESTING")
    print("=" * 60)
    print()
    
    expr1 = 'P ^ Q'
    expr2 = 'VAR ^ PROPOSITION'
    expr3 = '(P | Q) > R'
    
    print("Test 1:", expr1)
    tokenize(expr1)
    
    print("\nTest 2:", expr2)
    tokenize(expr2)
    
    print("\nTest 3:", expr3)
    tokenize(expr3)
    
    print("\n" + "=" * 60)
    print()
    
    # Test parser (once implemented)
    # Uncomment the line below when you're ready to test the parser
    test_parser()
    
    # Test variable extraction
    test_extract_variables()

