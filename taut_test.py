from taut import tokenize, Parser, print_tree, extract_variables

# tests for parser and extract provided by Cursor AI
def test_parser():
    """
    Runs test cases to make sure the parser works.
    
    Tests different expressions to check precedence, parentheses,
    and all the operators.
    """
    test_cases = [
        ("P ^ Q", "Simple AND"),
        ("P | Q", "Simple OR"),
        ("P | Q ^ R", "Precedence test"),
        ("(P | Q) ^ R", "Parentheses"),
        ("~P", "NOT"),
        ("P ^ Q | ~R", "Complex"),
        ("P > Q", "Implies"),
        ("((P))", "Nested parentheses"),
        ("P | Q > R", "Multiple operators"),
        ("P = Q", "Biconditional"),
        ("~P ^ Q", "NOT with AND"),
    ]
    
    print("=" * 60)
    print("PARSER TESTING")
    print("=" * 60)
    print()
    
    for expression, description in test_cases:
        print(f"Test: {description}")
        print(f"Expression: {expression}")
        
        try:
            tokens = tokenize(expression)
            # tokenize prints tokens, so we don't need to print again
            parser = Parser(tokens)
            tree = parser.parse()
            print("Tree structure:")
            print_tree(tree)
            print("✓ Parsed successfully")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        print("-" * 60)
        print()


def test_extract_variables():
    """
    Runs test cases to verify variable extraction works.
    
    Tests that we can correctly identify all unique variables
    from different expression trees.
    """
    test_cases = [
        ("P ^ Q", ["P", "Q"], "Simple AND"),
        ("P | Q | R", ["P", "Q", "R"], "Multiple OR"),
        ("P", ["P"], "Single variable"),
        ("~P", ["P"], "NOT with one variable"),
        ("P ^ Q | ~R", ["P", "Q", "R"], "Complex expression"),
        ("(P | Q) ^ R", ["P", "Q", "R"], "With parentheses"),
        ("P = Q", ["P", "Q"], "Biconditional"),
        ("P ^ P", ["P"], "Repeated variable"),
    ]
    
    print("=" * 60)
    print("VARIABLE EXTRACTION TESTING")
    print("=" * 60)
    print()
    
    for expression, expected_vars, description in test_cases:
        print(f"Test: {description}")
        print(f"Expression: {expression}")
        
        try:
            tokens = tokenize(expression)
            parser = Parser(tokens)
            tree = parser.parse()
            variables = extract_variables(tree)
            variables_list = sorted(list(variables))  # Convert set to sorted list for comparison
            
            expected_sorted = sorted(expected_vars)
            if variables_list == expected_sorted:
                print(f"✓ Found variables: {variables_list}")
            else:
                print(f"✗ Expected: {expected_sorted}, Got: {variables_list}")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        print("-" * 60)
        print()