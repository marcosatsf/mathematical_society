import argparse
import configparser
from random import random
from numpy.random import randint
from polynomial import Polynomial


class MaxbitPop:
    def __init__(self, n_bits, n_pop, obj_fun, poly, range_values) -> None:
        """
        Instatiate class of maxbit population.

        Args:
            n_bits (int): How many bits this population 
            will have.
            n_pop (int): Population size.
            obj_fun (function): Goal function.
        """
        self.lenb = n_bits
        self.popsi = n_pop
        self.objective_fun = obj_fun
        self.poly = poly
        self.range = range_values
        # t0 population of random bitstrings
        self.population = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]
        # Keep track of best solution
        self.best, self.best_eval = 0, obj_fun(poly, self.decode(self.population[0]))

    def decode(self, bitstring):
        chars = ''.join([str(s) for s in bitstring])
        integer = int(chars, 2)
        return self.range[0] + (integer/2**self.lenb) * (self.range[1] - self.range[0])

    def generation(self, crossover_rate, mutation_rate, generation_id):
        """
        Run generation process.

        Args:
            crossover_rate (int): Rate of population crossover 
            for this generation.
            mutation_rate (int): Rate of population mutation 
            for this generation.
            generation_id (int): Current generation year.
        """
        # Decoded population
        decoded = [self.decode(p) for p in self.population]
        scores = [self.objective_fun(self.poly, c) for c in decoded]
        print(f'--- Gen. {generation_id}, scores from pop: {min(scores)} ---')

        # Verify new best member of that population
        for i in range(self.popsi):
            if scores[i] < self.best_eval:
                self.best, self.best_eval = self.population[i], scores[i]
                print(f'>Generation {generation_id} [NEW BEST]: f({self.decode(self.population[i])}) -> {scores[i]:2.2f}')
                self.gen = generation_id

        # Selected parents
        parents = [selection(self.population, scores, k=3) for _ in range(self.popsi)]

        # Create next generation
        children_population = list()
        for i in range(0, self.popsi, 2):
            # Get selected parents in pairs
            p1, p2 = parents[i], parents[i+1]
            # Crossover and mutation
            for c in crossover(p1, p2, crossover_rate):
                # Mutation
                mutation(c, mutation_rate)
                # Store for next generation
                children_population.append(c)
        # Replace population
        self.population = children_population

    def get_stats(self):
        return {
            'best_person':self.best,
            'best':self.objective_fun(self.poly, self.decode(self.best)),
            'best_x':self.decode(self.best),
            'generation':self.gen
            }

def selection(pop, scores, k=3):
    """
    Selects random members (k times 
    looking for a better score) from current
    generation in order to be parents to
    next generation.

    Args:
        pop (list): Current list of population.
        scores (list): Current list of scores.
        k (int, optional): How many members
        will be searching. Defaults to 3.

    Returns:
        list: One member gene.
    """
    # first random selection
    selection_ix = randint(len(pop))
    for ix in randint(0, len(pop), k-1):
        # check if better (e.g. perform a tournament)
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]

# Crossover two parents to create two children
def crossover(p1, p2, crossover_rate):
    """
    Function to Crossover genes! 👨‍🔬👩‍🔬

    Args:
        p1 (list): Parent one.
        p2 (list): Parent two.
        crossover_rate (float): Crossover rate.
        How oftem a crossover will occur.

    Returns:
        list: Contains 2 newborn children.
    """
    # Children are copies of parents by default
    c1, c2 = p1.copy(), p2.copy()
    # Check recombination
    if random() < crossover_rate:
        # Select crossover point that is not on the end of the string
        pt = randint(1, len(p1)-2)
        # Perform crossover
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1,c2]

# Mutation operator
def mutation(bitstring, mutation_rate):
    """
    Function to execute mutation. ☢

    Args:
        bitstring (list): Member's gene.
        mutation_rate (float): Mutation rate.
        How oftem a mutation will occur.
    """
    for i in range(len(bitstring)):
        # Check for mutation
        if random() < mutation_rate:
            # Flip the bit
            bitstring[i] = 1 - bitstring[i]

def execute_function(polynomial, value):
    """
    Responsible to translate a polynomial
    string into a computated result of that
    polynomial and x value.

    Args:
        polynomial (str): Polynomial expression.
        value (float): Value that will be applied
        on X.

    Returns:
        float: result from this substitution.
    """
    return eval(polynomial.replace('x', f'({value})'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', dest='file_name', required=True, help='Filename which has polynomials')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('hyper.ini')
    # Polynomial object to organize all requests
    polys = Polynomial(args.file_name)
    # How many bits this population will have
    n_bits = int(config['DEFAULT']['NUMBER_OF_GENES'])
    # Population size
    n_pop = int(config['DEFAULT']['POPULATION_SIZE'])
    # Crossover rate of this population
    co_r = eval(config['DEFAULT']['CROSSOVER_RATE'].replace('NUMBER_OF_GENES', config['DEFAULT']['NUMBER_OF_GENES']))
    # Mutation rate of this population
    m_r = eval(config['DEFAULT']['MUTATION_RATE'].replace('NUMBER_OF_GENES', config['DEFAULT']['NUMBER_OF_GENES']))
    # Generation defined by next variable
    n_iter = int(config['DEFAULT']['GENERATIONS'])
    # Range of values to work on
    range_fun = eval(config['DEFAULT']['RANGE'])
    for current_poly in polys.polynomials:
        # t0 population of random bitstrings
        society = MaxbitPop(n_bits, n_pop, obj_fun=execute_function, poly=current_poly, range_values=range_fun)
        # Enumerate generations
        for gen in range(n_iter):
            society.generation(crossover_rate=co_r, mutation_rate=m_r, generation_id=gen)

        status = society.get_stats()
        print('\n------- RESULT LOG -------')
        print(f'Finished last generation of polynomial -> {current_poly}')
        print(f"Got best -> f({status['best_x']:.4f}) = {status['best']:.4f} ...")
        print(f"It's genes -> {status['best_person']}, at generation {status['generation']}")
        print('--------------------------\n')
