"""
Solutions to module 4 - A calculator
Student: Olof Rörby
Mail: Ollerorby@hotmail.se

"""

"""
Note:
The program is only working for a very tiny set of operations.
You have to add and/or modify code in ALL functions as well as add some new functions.
Use the syntax charts when you write the functions!
However, the class CalculatorSyntaxError is complete as well as handling in main
of CalculatorSyntaxError and TokenError.
"""

import math
from tokenize import TokenError  
from MA4tokenizer import TokenizeWrapper

def log(n):
    if n <=0:
        raise EvaluationError(f"Argument to log is {n}. Must be > 0")
    return math.log(n)

def fac(n):
    if n < 0 or int(n) != n:
        raise EvaluationError(f"Argument to fac is {n}. Must be integer >= 0")
    return math.factorial(int(n))

def fib(n):
    if n < 0 or int(n) != n:
        raise EvaluationError(f"Argument to fib is {n}. Must be integer >= 0")
    n = int(n)
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def mean(args):
    if not args:
        raise EvaluationError("mean requires at least one argument")
    return sum(args) / len(args)

function_1 = {'sin': math.sin,'cos': math.cos,'exp': math.exp,'log': log, 'fac': fac, 'fib': fib, }
function_n = {'max':max, 'min': min, 'sum': sum, 'mean': mean}

class EvaluationError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)
    pass

class CalculatorSyntaxError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)
    pass

def statement(wtok, variables):
    """ See syntax chart for statement"""
    result = assignment(wtok, variables)
    
    if not wtok.is_at_end():
        raise CalculatorSyntaxError("Unexpected token")
        
    return result


def assignment(wtok, variables):
    """ See syntax chart for assignment"""
    result = expression(wtok, variables)
    
    while wtok.get_current() == '=':
        wtok.next() 
        
        if wtok.is_name():
            variables[wtok.get_current()] = result
            wtok.next() 
        else:
            raise CalculatorSyntaxError("Expected variable after '='")
            
    return result


def expression(wtok, variables):
    """ See syntax chart for expression"""
    result = term(wtok, variables)
    while wtok.get_current() == '+' or wtok.get_current() == '-':
            if wtok.get_current() == '+':
                wtok.next()
                result = result + term(wtok, variables)
            elif wtok.get_current() == '-':
                wtok.next()
                result = result - term(wtok, variables)
    return result


def term(wtok, variables):
    """ See syntax chart for term"""
    result = factor(wtok, variables)
    while wtok.get_current() == '*' or wtok.get_current() == '/': 
        if wtok.get_current() == '*':
            wtok.next()
            result = result * factor(wtok, variables)
        elif wtok.get_current() == '/':
            wtok.next()
            denominator = factor(wtok, variables)
            if denominator == 0:
                raise EvaluationError('Division by zero')
            result = result / denominator

             
    return result


def arglist(wtok, variables):
    if wtok.get_current() != '(':
        raise CalculatorSyntaxError("Expected '('")
    wtok.next()

    args = []
    while True:
        args.append(assignment(wtok, variables))
        if wtok.get_current() == ',':
            wtok.next()
        elif wtok.get_current() == ')':
            wtok.next()
            break
        else:
            raise CalculatorSyntaxError("Expected ',' or ')'")

    return args

def factor(wtok, variables):
    """ See syntax chart for factor"""
    if wtok.get_current() == '(':
        wtok.next()
        result = assignment(wtok, variables)
        if wtok.get_current() != ')':
            raise CalculatorSyntaxError("Expected ')'")
        else:
            wtok.next()

    elif wtok.is_name():
        name = wtok.get_current()
        if name in function_1:
            wtok.next()

            if wtok.get_current() == '(':
                wtok.next()
                arg_value = assignment(wtok, variables)

                if wtok.get_current() != ')':
                    raise CalculatorSyntaxError("Expected')'")
                
                wtok.next()
                result = function_1[name](arg_value)

            else:
                raise CalculatorSyntaxError("Expected '(' after function name ")

        elif name in function_n:
            wtok.next()
            args_list = arglist(wtok, variables)
            result = function_n[name](args_list)
        
        elif name in variables:
            result = variables[name]
            wtok.next()
        else:
            raise EvaluationError(f"Undefined variable: '{name}'")   
            
    elif wtok.is_number():
        result = float(wtok.get_current())
        wtok.next()

    elif wtok.get_current() == '-':
        wtok.next()
        result = -factor(wtok, variables)

    else:
        raise CalculatorSyntaxError(
            "Expected number, word or '('")  
    return result


def main():
    """
    Handles:
       the iteration over input lines,
       commands like 'quit' and 'vars' and
       raised exceptions.
    Starts with reading the init file
    """
    
    print("Numerical calculator")
    variables = {"ans": 0.0, "PI": math.pi, "E": math.e}
    # Note: The unit test file initiate variables in this way. If your implementation 
    # requires another initiation you have to update the test file accordingly.
    init_file = 'MA4init.txt'
    lines_from_file = ''
    try:
        with open(init_file, 'r') as file:
            lines_from_file = file.readlines()
    except FileNotFoundError:
        pass

    while True:
        if lines_from_file:
            line = lines_from_file.pop(0).strip()
            print('init  :', line)
        else:
            line = input('\nInput : ')
        if line == '' or line[0]=='#':
            continue
        wtok = TokenizeWrapper(line)

        if wtok.get_current() == 'quit':
            print('Bye')
            exit()

        elif wtok.get_current() == 'vars':
            for var_name, var_value in variables.items():
                print(f"{var_name:<5} : {var_value}")
                continue
        else:
            try:
                result = statement(wtok, variables)
                print('Result:', result)
                variables['ans'] = result

            except CalculatorSyntaxError as se:
                print("*** Syntax error: ", se)
                curr_tok = wtok.get_current()
                if wtok.is_at_end() or curr_tok.strip() == "":
                    curr_tok = '*EOL*'

                print(
                f"Error occurred at token '{curr_tok}' just after token '{wtok.get_previous()}'")

            except EvaluationError as ee:
                print("*** Evaluation error:", ee)

            except TokenError as te:
                print('*** Syntax error: Unbalanced parentheses')
 


if __name__ == "__main__":
    main()