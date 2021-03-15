import re
import math


class Interpretor():
    def __init__(self):
        self.expression = ''
        self.ans = None
    
    def set_expression(self, expr):
        self.expression = expr

    def append_expression(self, expr):
        self.expression += expr

    def remove_last(self):
        self.expression = self.expression[:-1]

    def clear_expression(self):
        self.expression = ''

    def solve(self):
        self.parse()
        self.ans = f'{eval(self.expression)}'
        self.clear_expression()

    def parse(self):
        self._parse_ans()
        self._parse_pi()
        self._parse_eulers_number()
        self._parse_exponentiation()
        self._parse_radicals()
        self._parse_trig_functions()
        self._parse_implicit_multiplication()
        self._parse_logarithms()

    def _parse_ans(self):
        if self.ans is not None:
            self._im_with_ans()
            self.expression = self.expression.replace('ans', self.ans)

    def _parse_pi(self):
        if 'π' in self.expression:
            self.expression = self.expression.replace(chr(960), 'math.pi')

    def _parse_eulers_number(self):
        if 'e' in self.expression:
            self.expression = self.expression.replace('e', 'math.e')

    def _parse_exponentiation(self):
        if '^' in self.expression:
            self.expression = self.expression.replace('^', '**')

    def _parse_radicals(self):
        if '√' in self.expression:
            self.expression = self.expression.replace('√', 'math.sqrt')

    def _parse_trig_functions(self):
        if 'arcsin' in self.expression:
            self.expression = self.expression.replace('arcsin', 'inverse_s')
        if 'arccos' in self.expression:
            self.expression = self.expression.replace('arccos', 'inverse_c')
        if 'arctan' in self.expression:
            self.expression =  self.expression.replace('arctan', 'inverse_t')
        if 'sin' in self.expression:
            self.expression = self.expression.replace('sin', 'math.sin')
        if 'cos' in self.expression:
            self.expression = self.expression.replace('cos', 'math.cos')
        if 'tan' in self.expression:
            self.expression = self.expression.replace('tan', 'math.tan')
        if 'inverse' in self.expression:
            self.expression = self.expression.replace('inverse_s', 'math.asin')
            self.expression = self.expression.replace('inverse_c', 'math.acos')
            self.expression = self.expression.replace('inverse_t', 'math.atan')


    def _parse_logarithms(self):
        if 'log' in self.expression:
            self.expression =  self.expression.replace('log', 'math.log10')
        if 'ln' in self.expression:
            self.expression = self.expression.replace('ln', 'math.log')

    def _parse_implicit_multiplication(self):
        self._im_with_parenthetical_expr()
        self._im_with_irrational_constants()
        self._im_with_functions()

    def _im_with_parenthetical_expr(self):
        if ')(' in self.expression:
            self.expression =  self.expression.replace(')(', ')*(')
        
        for im in re.findall(r'[0-9ei]\(', self.expression):
            self.expression = self.expression.replace(im, f'{im[0]}*{im[-1]}')

        for im in re.findall(r'\)[lm0-9\-\.]', self.expression):
            self.expression = self.expression.replace(im, f'{im[0]}*{im[-1]}')
            
    def _im_with_irrational_constants(self):
        for im in re.findall(r'[0-9ei][m]', self.expression):
            self.expression = self.expression.replace(im, f'{im[0]}*{im[-1]}')

        for im in re.findall(r'[ei][m0-9\.\-]', self.expression):
            self.expression = self.expression.replace(im, f'{im[0]}*{im[-1]}')

    def _im_with_functions(self):
        for im in re.findall(r'[0-9ei][ml]', self.expression):
            self.expression = self.expression.replace(im, f'{im[0]}*{im[-1]}')

    def _im_with_ans(self):
        for im in re.findall(r'[0-9\.eπs]a', self.expression):
            self.expression = self.expression.replace(im, f'{im[0]}*{im[-1]}')

        for im in re.findall(r's[0-9\.\-eπa]', self.expression):
            self.expression = self.expression.replace(im, f'{im[0]}*{im[-1]}')