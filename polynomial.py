class Polynomial:
    def __init__(self, file_name) -> None:
        """
        Polynomial group class. This organizes
        polynomials from a file into a list to
        be executed.

        Args:
            file_name (str): File name which contain(s)
            polynomial(s) formula(s)
        """
        try:
            with open(file_name, 'r') as f:
                self.polynomials = list()
                for p in f.readlines():
                    p = p.replace('^','**').replace('x','*x').replace(' ', '').replace('\n', '')
                    self.polynomials.append(p)
            
        except FileNotFoundError as e:
            print(f'File {file_name} does not exists :/')


    # def power_parser(self, term):
    #     term = term.split('x')
    #     if len(term) == 1:
    #         power = 0
    #     else:
    #         if term[1] == '':
    #             power = 1
    #         else:
    #             power = eval(term[1][1:])
    #     if term[0] == '':
    #         mult = 1
    #     else:
    #         mult = eval(term[0])
    #     return (mult, power)

    # def polynomial_parser(self, polynomial:str):
    #     polynomial_splitted = polynomial.split(' ')
        
    #     operators = list()
    #     poly_terms = list()
    #     for term in polynomial_splitted:
    #         if term in ('+','-','*','/'):
    #             operators.append(term)
    #         else:
    #             poly_terms.append(term)
    #     # N operators to N+1 poly_terms
    #     if len(operators)+1 == len(poly_terms):
    #         raise Exception('Impossible to parse...incompatible number of terms and operators -> {polynomial}')
        
    #     polynomial_str = str()
    #     for idx, op in enumerate(operators):
    #         if op in ('*','/'):
    #             # poly_terms[idx] and poly_terms[idx+1]
    #             term_power1 = self.power_parser(poly_terms[idx])
    #             term_power2 = self.power_parser(poly_terms[idx+1])
    #             if op == '*':
    #                 term_result = term_power1[0] * term_power2[0]
    #                 power_result = term_power1[1] + term_power2[1]
    #             else:
    #                 term_result = term_power1[0] / term_power2[0]
    #                 power_result = term_power1[1] - term_power2[1]
    #             polynomial_str += f'{term_result}*x**{power_result} '

    #             if power_result != 0:
    #                 polynomial_str += f'{term_result}*x**{power_result} '
    #                 poly_terms[idx+1] = f'{term_result}x^{power_result}'
    #             else:
    #                 polynomial_str += f'{term_result} '
    #                 poly_terms[idx+1] = f'{term_result}'
    #         else:
    #             term_power = self.power_parser(poly_terms[idx])
    #             if term_power[1] != 0:
    #                 if idx == 0:
    #                     polynomial_str += f'{term_power[0]}*x**{term_power[1]} '
    #                 else:
    #                     polynomial_str += f'{op} {term_power[0]}*x**{term_power[1]} '
    #             else:
    #                 if idx == 0:
    #                     polynomial_str += f'{term_power[0]} '
    #                 else:
    #                     polynomial_str += f'{op} {term_power[0]} '
            
    #     return polynomial_str