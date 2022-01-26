from random import random
from numpy.random import randint, rand


class MaxbitPop:
    def __init__(self, n_bits, n_pop, obj_fun, is_quadratic=False) -> None:
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

        # t0 population of random bitstrings
        self.population = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]
        # Keep track of best solution
        self.is_quadratic = is_quadratic
        if is_quadratic:
            self.best, self.best_eval = 0, obj_fun(self.decode(self.population[0]))
        else:
            self.best, self.best_eval = 0, obj_fun(self.population[0])

    def decode(self, bitstring):
        chars = ''.join([str(s) for s in bitstring])
        integer = int(chars, 2)
        return -100 + (integer/2**8) * 100

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
        if self.is_quadratic:
            decoded = [self.decode(p) for p in self.population]
            scores = [self.objective_fun(c) for c in decoded]
        else:
        # Generate scores from current population
            scores = [self.objective_fun(c) for c in self.population]
        print(f'--- Gen. {generation_id}, scores from pop: {min(scores)} ---')

        # Verify new best member of that population
        for i in range(self.popsi):
            if self.is_quadratic:
                if abs(scores[i]) < abs(self.best_eval):
                    self.best, self.best_eval = self.population[i], scores[i]
                    print(f'>Generation {generation_id} [NEW BEST]: f({self.decode(self.population[i])}) -> {scores[i]:2.2f}')
                    self.gen = generation_id
            else:
                if scores[i] < self.best_eval:
                    self.best, self.best_eval = self.population[i], scores[i]
                    print(f'>Generation {generation_id} [NEW BEST]: f({self.population[i]}) -> {scores[i]:2.2f}')
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
            'best':self.objective_fun(self.best),
            'exp_best':self.best_eval,
            'generation':self.gen
            }

def selection(pop, scores, k=3):
    # first random selection
    selection_ix = randint(len(pop))
    for ix in randint(0, len(pop), k-1):
        # check if better (e.g. perform a tournament)
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]

# Crossover two parents to create two children
def crossover(p1, p2, crossover_rate):
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
    for i in range(len(bitstring)):
        # Check for mutation
        if random() < mutation_rate:
            # Flip the bit
            bitstring[i] = 1 - bitstring[i]

# Simple goal function
def onemax(x):
    """
    Retrieve negative sum of elements.

    Args:
        x (list): List of boolean elements.

    Returns:
        int: Negative sum of elements. 
    """
    return -sum(x)

def quadratic_function(x):
    """
    An example quadratic function:
    4x²+3x-10

    Args:
        x (int): x value

    Returns:
        int: function value
    """
    return 4*x**2 + 3*x - 10

if __name__ == '__main__':
    # How many bits this population will have
    n_bits = 8
    # Population size
    n_pop = 100
    # Crossover rate of this population
    co_r = 0.85
    # Mutation rate of this population
    m_r = 1/n_bits
    # Generation defined by next variable
    n_iter = 100
    # t0 population of random bitstrings
    society = MaxbitPop(n_bits, n_pop, obj_fun=quadratic_function, is_quadratic=True)
    # Enumerate generations
    for gen in range(n_iter):
        society.generation(crossover_rate=co_r, mutation_rate=m_r, generation_id=gen)

    status = society.get_stats()
    print('Finished last generation!!')
    print(f"Expected best -> {status['exp_best']}")
    print(f"Got best -> {status['best']}, at generation {status['generation']}")
