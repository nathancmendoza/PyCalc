from interpreter import *
import unittest


def _gen_n_digit_number():
    from random import randint, uniform
    if randint(0,1):
        digits = randint(1, 9)
        the_number = ''
        for _ in range(digits):
            the_number += f'{randint(0,9)}'
        if randint(0, 1):
            the_number = f'-{the_number}'
        return the_number
    else:
        return f'{uniform(0, 999999999)}'

def _choose_random_operation():
    from random import choice
    return choice(['+', '-', '*', '/', '**'])

def _gen_parenthetical_expression():
    return f'({_gen_n_digit_number()} {_choose_random_operation()} {_gen_n_digit_number()})'

class TestInterpretorInitialization(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_interpretor_exists(self):
        self.assertTrue('demo' in self.__dict__)

    def test_interpretor_was_created(self):
        self.assertTrue(type(self.demo) is Interpretor)

    def test_interpretor_initialized_with_empty_string(self):
        self.assertTrue(self.demo.expression == '')
    
    def test_interpretor_initialized_with_no_previous_answer(self):
        self.assertTrue(self.demo.ans is None)

class TestInterpretorExpressionEditing(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_setting_expression_to_a_number(self):
        from random import randint
        num_to_add = str(randint(0, 9))
        self.demo.set_expression(num_to_add)
        self.assertEqual(self.demo.expression, num_to_add)

    def test_setting_epression_to_n_digit_number(self):
        from random import randint
        digits = randint(1, 50)
        num = ''
        for _ in range(digits):
            num += f'{randint(0,9)}'
        self.demo.set_expression(num)
        self.assertEqual(self.demo.expression, num)

    def test_setting_expression_to_sample_expression(self):
        from random import randint, choice
        num1 = str(randint(0,9))
        num2 = str(randint(0,9))
        op = choice(['+','-','/','-'])
        self.demo.set_expression(num1+op+num2)
        self.assertEqual(self.demo.expression, ''.join([num1, op, num2]))
        
    def test_adding_to_expression_with_an_operation(self):
        from random import choice
        self.demo.set_expression('1')
        op = choice(['+', '-', '*', '/'])
        self.demo.append_expression(op)
        self.assertEqual(self.demo.expression, f'1{op}')

    def test_adding_to_expression_with_a_number(self):
        from random import randint
        self.demo.set_expression('1+')
        num = str(randint(1,9))
        self.demo.append_expression(num)
        self.assertEqual(self.demo.expression, f'1+{num}')
    

    def test_removing_last_character(self):
        self.demo.set_expression('1+12')
        self.demo.remove_last()
        self.assertEqual(self.demo.expression, '1+1')

    def test_clear_expression(self):
        from random import randint
        self.demo.set_expression(f'{randint(0,100)}')
        self.demo.clear_expression()
        self.assertEqual(self.demo.expression, '')

class TestInterpreterParsingSimpleExpressions(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_binary_expression_interpertation(self):
        first_num = _gen_n_digit_number()
        op = _choose_random_operation()
        second_num = _gen_n_digit_number()
        self.demo.set_expression(f'{first_num} {op} {second_num}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, ' '.join([first_num, op, second_num]))

    def test_long_expression_interprertation(self):
        from random import randint
        expr = ''
        for _ in range(randint(2, 101)):
            expr += f'{_gen_n_digit_number()}'
            expr += f' {_choose_random_operation()} '
        expr += f'{_gen_n_digit_number()}'
        self.demo.set_expression(expr)
        self.demo.parse()
        self.assertAlmostEqual(self.demo.expression, expr)

class TestInterpreterParsingOfExponetionalExpressions(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_interpretation_of_exponentiation_between_two_numbers(self):
        the_base = f'{_gen_n_digit_number()}'
        the_power = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'{the_base} ^ {the_power}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_base} ** {the_power}')

    def test_interpretation_of_exponentiation_between_irrational_numbers_as_base(self):
        from random import choice
        the_base = f"{choice(['e', 'π'])}"
        the_power = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'{the_base} ^ {the_power}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_base} ** {the_power}'.replace('π', 'pi'))

    def test_interpretation_of_exponentiation_between_irrational_numbers_as_power(self):
        from random import choice
        the_power = f"{choice(['e', 'π'])}"
        the_base = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'{the_base} ^ {the_power}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_base} ** math.{the_power}'.replace('π', 'pi'))

    def test_interpretation_of_exponentiation_between_irrational_numbers_as_base_and_power(self):
        from random import choice
        the_base = f"{choice(['e', 'π'])}"
        the_power = f"{choice(['e', 'π'])}"
        self.demo.set_expression(f'{the_base} ^ {the_power}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_base} ** math.{the_power}'.replace('π', 'pi'))

    def test_inerpretation_of_exponentation_between_parethetical_expressions_as_base(self):
        the_base = f'{_gen_parenthetical_expression()}'
        the_power = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'{the_base} ^ {the_power}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_base} ** {the_power}')

    def test_interpretation_of_exponentiation_between_parethetical_expressions_as_power(self):
        the_base = f'{_gen_n_digit_number()}'
        the_power = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'{the_base} ^ {the_power}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_base} ** {the_power}')

    def test_interpretation_of_exponentiation_between_parethetical_expressions_as_base_and_as_power(self):
        the_base = f'{_gen_parenthetical_expression()}'
        the_power = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'{the_base} ^ {the_power}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_base} ** {the_power}')

    def test_interpretation_of_exponentiation_with_function_as_base(self):
        from random import choice
        the_base = f"{choice(['sin', 'cos', 'tan'])}"
        the_power = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'{the_base}(0) ^ {the_power}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_base}(0) ** {the_power}')

    def test_interpretation_of_exponentiation_with_functions_as_power(self):
        from random import choice
        the_power = f"{choice(['sin', 'cos', 'tan'])}"
        the_base = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'{the_base} ^ {the_power}(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_base} ** math.{the_power}(0)')

    def test_interpreation_of_exponentiation_with_functions_as_base_and_as_power(self):
        from random import choice
        the_base = f"{choice(['sin', 'cos', 'tan'])}"
        the_power = f"{choice(['sin', 'cos', 'tan'])}"
        self.demo.set_expression(f'{the_base}(0) ^ {the_power}(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_base}(0) ** math.{the_power}(0)')

class TestInterpretetationOfIrrationalConstants(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_interpreting_eulers_number(self):
        self.demo.set_expression('e')
        self.demo.parse()
        self.assertEqual(self.demo.expression, 'math.e')

    def test_interpreting_pi(self):
        self.demo.set_expression('π')
        self.demo.parse()
        self.assertEqual(self.demo.expression, 'math.pi')

class TestInterpretationOfSquareRoots(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_parsing_of_radical_expression(self):
        x = _gen_n_digit_number()
        expr = f'√({x})'
        self.demo.set_expression(expr)
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.sqrt({x})')

class TestInterpretationOfTrigFunctions(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_parsing_of_sine_function(self):
        self.demo.set_expression('sin(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, 'math.sin(0)')

    def test_parsing_of_cosing_function(self):
        self.demo.set_expression('cos(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, 'math.cos(0)')

    def test_parsing_of_tangent_function(self):
        self.demo.set_expression('tan(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, 'math.tan(0)')

class TestInterpretationOfInverseTrigFunctions(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_parsing_of_arcsine_function(self):
        self.demo.set_expression('arcsin(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, 'math.asin(0)')

    def test_parsing_of_arccosine_function(self):
        self.demo.set_expression('arccos(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, 'math.acos(0)')

    def test_parsing_of_arctangent_function(self):
        self.demo.set_expression('arctan(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, 'math.atan(0)')

class TestInterpretationOfLogarithms(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()
        

    def test_parsing_of_log_base_ten(self):
        x = _gen_n_digit_number()
        self.demo.set_expression(f'log({x})')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.log10({x})')

    def test_parsing_of_natural_logarithm(self):
        x = _gen_n_digit_number()
        self.demo.set_expression(f'ln({x})')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.log({x})')

class TestInterpretiationOfImplicitMultiplicationWithNumericalExpressionsOnly(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()        

    def test_implicit_multiplication_between_two_parathetical_expressions(self):
        first_expr = _gen_parenthetical_expression()
        second_expr = _gen_parenthetical_expression()
        self.demo.set_expression(f'{first_expr}{second_expr}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{first_expr}*{second_expr}')

    def test_implicit_multiplication_between_many_paranthetical_expressions(self):
        from random import randint
        expressions = [f'{_gen_parenthetical_expression()}' for _ in range(randint(3, 10))]
        self.demo.set_expression(''.join(expressions))
        self.demo.parse()
        self.assertEqual(self.demo.expression, '*'.join(expressions))

    def test_implicit_multiplication_between_a_number_and_a_parathetical_expression_on_the_right(self):
        the_number = f'{_gen_n_digit_number()}'
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'{the_number}{the_expression}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_number}*{the_expression}')

    def test_implicit_mulitplication_between_a_number_and_a_parathetical_expresssion_on_the_left(self):
        the_number = f'{_gen_n_digit_number()}'
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'{the_expression}{the_number}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_expression}*{the_number}')

    def test_implicit_multiplication_between_a_parathetical_expression_and_numbers_on_both_sides(self):
        first_num = f'{_gen_n_digit_number()}'
        second_num = f'{_gen_n_digit_number()}'
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'{first_num}{the_expression}{second_num}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{first_num}*{the_expression}*{second_num}')

    def test_implicit_multiplication_with_numbers_and_trailing_irrational_constants(self):
        the_number = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'{the_number}π')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_number}*math.pi')
        self.demo.set_expression(f'{the_number}e')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_number}*math.e')

    def test_implicit_mulitplication_with_numbers_and_leading_irrattional_constants(self):
        the_number = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'π{the_number}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.pi*{the_number}')
        self.demo.set_expression(f'e{the_number}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.e*{the_number}')

    def test_implicit_multiplication_with_parathetical_expression_and_leading_irrational_constants(self):
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'π{the_expression}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.pi*{the_expression}')
        self.demo.set_expression(f'e{the_expression}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.e*{the_expression}')

    def test_implicit_multiplication_with_parathetical_expression_and_trailing_irrational_constants(self):
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'{the_expression}π')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_expression}*math.pi')
        self.demo.set_expression(f'{the_expression}e')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_expression}*math.e')

    def test_implicit_mulitplication_with_irrational_constants_expression(self):
        self.demo.set_expression('eπ')
        self.demo.parse()
        self.assertEqual(self.demo.expression, 'math.e*math.pi')
        self.demo.set_expression('πe')
        self.demo.parse()
        self.assertEqual(self.demo.expression, 'math.pi*math.e')
       
class TestInterpretationOfImplicitMultiplicationWithTrigFunctionsAndNumericalExpressions(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_implicit_multiplication_with_trig_functions_and_leading_numbers(self):
        from random import choice
        the_number = f'{_gen_n_digit_number()}'
        trig_func = f'{choice(["sin", "cos", "tan"])}'
        self.demo.set_expression(f'{the_number}{trig_func}(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_number}*math.{trig_func}(0)')

    def test_implicit_multiplication_with_inverse_trig_functions_and_leading_numbers(self):
        from random import choice
        the_number = f'{_gen_n_digit_number()}'
        inverse_trig_func = f'{choice(["arcsin", "arccos", "arctan"])}'
        self.demo.set_expression(f'{the_number}{inverse_trig_func}(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_number}*math.{inverse_trig_func[0] + inverse_trig_func[3:]}(0)')

    def test_implicit_multiplication_with_trig_functions_and_trailing_numbers(self):
        from random import choice
        the_number = f'{_gen_n_digit_number()}'
        trig_func = f'{choice(["sin", "cos", "tan"])}'
        self.demo.set_expression(f'{trig_func}(0){the_number}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{trig_func}(0)*{the_number}')

    def test_implicit_multiplication_with_inverse_trig_functions_and_trailing_numbers(self):
        from random import choice
        the_number = f'{_gen_n_digit_number()}'
        inverse_trig_func = f'{choice(["arcsin", "arccos", "arctan"])}'
        self.demo.set_expression(f'{inverse_trig_func}(0){the_number}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{inverse_trig_func[0] + inverse_trig_func[3:]}(0)*{the_number}')

    def test_implicit_multiplication_with_trig_functions_and_leading_irrational_numbers(self):
        from random import choice
        the_constant = f'{choice(["π", "e"])}'
        the_function = f'{choice(["sin", "cos", "tan"])}'
        self.demo.set_expression(f'{the_constant}{the_function}(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_constant}*math.{the_function}(0)'.replace('π', 'pi'))

    def test_implicit_multiplication_with_inverse_trig_functions_and_leading_irrational_numbers(self):
        from random import choice
        the_constant = f'{choice(["π", "e"])}'
        the_inverse_function = f'{choice(["arcsin", "arccos", "arctan"])}'
        self.demo.set_expression(f'{the_constant}{the_inverse_function}(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_constant}*math.{the_inverse_function[0] + the_inverse_function[3:]}(0)'.replace('π', 'pi'))

    def test_implicit_multiplication_with_trig_functions_and_trailing_irrational_numbers(self):
        from random import choice
        the_constant = f'{choice(["π", "e"])}'
        the_function = f'{choice(["sin", "cos", "tan"])}'
        self.demo.set_expression(f'{the_function}(0){the_constant}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_function}(0)*math.{the_constant}'.replace('π', 'pi'))

    def test_implicit_multiplication_with_inverse_trig_functions_and_trailing_irrational_numbers(self):
        from random import choice
        the_constant = f'{choice(["π", "e"])}'
        the_inverse_function = f'{choice(["arcsin", "arccos", "arctan"])}'
        self.demo.set_expression(f'{the_inverse_function}(0){the_constant}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_inverse_function[0] + the_inverse_function[3:]}(0)*math.{the_constant}'.replace('π', 'pi'))

    def test_implicit_multiplication_with_trig_functions_and_leading_parenthetical_expressions(self):
        from random import choice
        the_expression = f'{_gen_parenthetical_expression()}'
        the_function = f'{choice(["sin", "cos", "tan"])}'
        self.demo.set_expression(f'{the_expression}{the_function}(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_expression}*math.{the_function}(0)')

    def test_implicit_multiplication_with_inverse_trig_functions_and_leading_parenthetical_expressions(self):
        from random import choice
        the_expression = f'{_gen_parenthetical_expression()}'
        the_inverse_function = f'{choice(["arcsin", "arccos", "arctan"])}'
        self.demo.set_expression(f'{the_expression}{the_inverse_function}(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_expression}*math.{the_inverse_function[0] + the_inverse_function[3:]}(0)')

    def test_implicit_multiplication_with_trig_functions_and_trailing_parenthetical_expressions(self):
        from random import choice
        the_expression = f'{_gen_parenthetical_expression()}'
        the_function = f'{choice(["sin", "cos", "tan"])}'
        self.demo.set_expression(f'{the_function}(0){the_expression}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_function}(0)*{the_expression}')

    def test_implicit_multiplication_with_inverse_trig_functions_and_trailing_parenthetical_expressions(self):
        from random import choice
        the_expression = f'{_gen_parenthetical_expression()}'
        the_inverse_function = f'{choice(["arcsin", "arccos", "arctan"])}'
        self.demo.set_expression(f'{the_inverse_function}(0){the_expression}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_inverse_function[0] + the_inverse_function[3:]}(0)*{the_expression}')

class TestInterpretationOfImplicitMultiplicationWithLogsAndNumericalExpressions(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_implicit_multipication_of_ln_and_leading_numbers(self):
        the_number = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'{the_number}ln(1)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_number}*math.log(1)')

    def test_implicit_multiplication_of_log_and_leading_numbers(self):
        the_number = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'{the_number}log(1)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_number}*math.log10(1)')

    def test_implicit_multiplication_of_ln_and_trailing_numbers(self):
        the_number = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'ln(1){the_number}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.log(1)*{the_number}')

    def test_implicit_multiplication_of_log_and_trailing_numbers(self):
        the_number = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'log(1){the_number}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.log10(1)*{the_number}')

    def test_implicit_multiplication_of_ln_and_leading_parenthetical_expressions(self):
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'{the_expression}ln(1)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_expression}*math.log(1)')

    def test_implicit_multiplication_of_ln_and_trailing_parenthetical_expressions(self):
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'ln(1){the_expression}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.log(1)*{the_expression}')

    def test_implicit_multiplication_of_log_and_leading_parenthetical_expressions(self):
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'{the_expression}log(1)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_expression}*math.log10(1)')

    def test_implicit_multiplication_of_log_and_trailing_parenthetical_expressions(self):
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'log(1){the_expression}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.log10(1)*{the_expression}')

class TestInterpretationOfImplicitMultiplicationWithSqrtsAndNumericalExpressions(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_implicit_multiplication_with_sqrt_and_leading_numbers(self):
        the_number = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'{the_number}√(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_number}*math.sqrt(0)')

    def test_implicit_multiplication_with_sqrt_and_trailing_numbers(self):
        the_number = f'{_gen_n_digit_number()}'
        self.demo.set_expression(f'√(0){the_number}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.sqrt(0)*{the_number}')

    def test_implicit_multiplication_with_sqrt_and_leading_irrational_constants(self):
        from random import choice
        the_constant = f"{choice(['e', 'π'])}"
        self.demo.set_expression(f'{the_constant}√(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_constant}*math.sqrt(0)'.replace('π', 'pi'))

    def test_implicit_multiplication_with_sqrt_and_trailing_irrational_numbers(self):
        from random import choice
        the_constant = f"{choice(['e', 'π'])}"
        self.demo.set_expression(f'√(0){the_constant}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.sqrt(0)*math.{the_constant}'.replace('π', 'pi'))

    def test_implicit_multiplication_with_sqrt_and_leading_parethetical_expressions(self):
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'{the_expression}√(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_expression}*math.sqrt(0)')
        
    def test_implicit_multiplication_with_sqrt_and_trailing_parethetical_expresssions(self):
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'√(0){the_expression}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.sqrt(0)*{the_expression}')

class TestinterpretationOfImplicitMultiplicationBetweenFunctions(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_implicit_multiplication_between_trig_functions(self):
        from random import shuffle, randint
        the_functions = ['sin', 'cos', 'tan']
        shuffle(the_functions)
        expression_length = randint(1, 3)
        expr = ''
        for f in the_functions[:expression_length]:
            expr += f'{f}(0)'
        self.demo.set_expression(expr)
        self.demo.parse()
        self.assertEqual(self.demo.expression, '*'.join([f'math.{i}(0)' for i in the_functions[:expression_length]]))

    def test_implicit_multiplication_between_inverse_trig_functions(self):
        from random import shuffle, randint
        the_functions = ['arcsin', 'arccos', 'arctan']
        shuffle(the_functions)
        expression_length = randint(1, 3)
        expr = ''
        for f in the_functions[:expression_length]:
            expr += f'{f}(0)'
        self.demo.set_expression(expr)
        self.demo.parse()
        self.assertEqual(self.demo.expression, '*'.join([f'math.{i[0]+i[3:]}(0)' for i in the_functions[:expression_length]]))

    def test_implicit_multiplication_between_a_trig_functions_and_an_inverse_trig_function(self):
        from random import choice
        the_func = choice(['sin', 'cos', 'tan'])
        the_inverse = choice(['arcsin', 'arccos', 'arctan'])
        expr = f'{the_func}(0){the_inverse}(0)'
        self.demo.set_expression(expr)
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_func}(0)*math.{the_inverse[0] + the_inverse[3:]}(0)')

    def test_implicit_multiplication_between_a_trig_function_and_and_sqrt(self):
        from random import choice
        the_func = choice(['sin', 'cos', 'tan'])
        self.demo.set_expression(f'{the_func}(0)√(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_func}(0)*math.sqrt(0)')

    def test_implicit_multiplication_between_an_inverse_trig_function_and_sqrt(self):
        from random import choice
        the_func = choice(['arcsin', 'arccos', 'arctan'])
        self.demo.set_expression(f'{the_func}(0)√(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.{the_func[0] + the_func[3:]}(0)*math.sqrt(0)')

    def test_implicit_multiplication_between_a_trig_function_and_a_logarithm(self):
        from random import choice
        the_func = choice(['sin', 'cos', 'tan'])
        the_log = choice(['ln', 'log'])
        self.demo.set_expression(f'{the_func}(0){the_log}(1)')
        self.demo.parse()
        if the_log == 'ln':
            self.assertEqual(self.demo.expression, f'math.{the_func}(0)*math.log(1)')
        else:
            self.assertEqual(self.demo.expression, f'math.{the_func}(0)*math.log10(1)')

    def test_implicit_multiplication_between_an_inverse_trig_function_and_a_logarithm(self):
        from random import choice
        the_func = choice(['arcsin', 'arccos', 'arctan'])
        the_log = choice(['ln', 'log'])
        self.demo.set_expression(f'{the_func}(0){the_log}(1)')
        self.demo.parse()
        if the_log == 'ln':
            self.assertEqual(self.demo.expression, f'math.{the_func[0] + the_func[3:]}(0)*math.log(1)')
        else:
            self.assertEqual(self.demo.expression, f'math.{the_func[0] + the_func[3:]}(0)*math.log10(1)')

    def test_implicit_multiplication_between_a_sqrt_and_a_logarithm(self):
        from random import choice
        the_log = choice(['ln', 'log'])
        self.demo.set_expression(f'√(0){the_log}(1)')
        self.demo.parse()
        if the_log == 'ln':
            self.assertEqual(self.demo.expression, f'math.sqrt(0)*math.log(1)')
        else:
            self.assertEqual(self.demo.expression, f'math.sqrt(0)*math.log10(1)')

    def test_implicit_multiplication_between_logarithms(self):
        self.demo.set_expression('log(1)ln(1)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, 'math.log10(1)*math.log(1)')

    def test_implicit_multiplication_between_square_roots(self):
        self.demo.set_expression('√(0)√(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, 'math.sqrt(0)*math.sqrt(0)')
          
class TestAnswerPreservationAndExceptionReporting(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()

    def test_answer_to_current_expression_is_remembered_after_evaluation(self):
        self.demo.set_expression('1 + 1')
        self.demo.solve()
        self.assertEqual(self.demo.ans, '2')

    def test_after_evaluation_of_current_expression__the_expression_attribute_is_cleared_to_an_empty_string(self):
        self.demo.set_expression('1 + 1')
        self.demo.solve()
        self.assertEqual(self.demo.expression, '')

    def test_if_ans_is_not_none_and_is_used_in_a_subsequent_expression__ans_is_parsed_appropriately(self):
        self.demo.set_expression('1 + 1')
        self.demo.solve()
        self.demo.set_expression('2 + ans')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'2 + {self.demo.ans}')

class TestImplicitMultiplicationOfExpresssionsUsingPreviousAnswer(unittest.TestCase):
    def setUp(self):
        self.demo = Interpretor()
        self.demo.set_expression('1 + 1')
        self.demo.solve()

    def test_implicit_multiplication_with_leading_ans_and_numbers(self):
        self.demo.set_expression('2ans')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'2*{self.demo.ans}')

    def test_implicit_multiplication_with_trailing_ans_and_numbers(self):
        self.demo.set_expression('ans2')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{self.demo.ans}*2')

    def test_implicit_multiplication_with_leading_ans_and_trailing_function(self):
        self.demo.set_expression('anssin(0)')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{self.demo.ans}*math.sin(0)')

    def test_implicit_multiplication_with_trailing_ans_and_leading_function(self):
        self.demo.set_expression('sin(0)ans')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'math.sin(0)*{self.demo.ans}')

    def test_implicit_multiplication_with_leading_ans_and_trailing_parenthetical_expression(self):
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'ans{the_expression}')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{self.demo.ans}*{the_expression}')

    def test_implicit_multiplication_with_trailing_ans_and_leading_parenthetical_expression(self):
        the_expression = f'{_gen_parenthetical_expression()}'
        self.demo.set_expression(f'{the_expression}ans')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{the_expression}*{self.demo.ans}')

    def test_implicit_multiplication_with_leading_and_trailing_ans(self):
        self.demo.set_expression('ansans')
        self.demo.parse()
        self.assertEqual(self.demo.expression, f'{self.demo.ans}*{self.demo.ans}')



if __name__ == "__main__":
    unittest.main()
