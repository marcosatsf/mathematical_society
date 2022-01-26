# Mathematical Society
Imagine a world where people born, live and die just to execute one single task...\
-*yea, it could be ours too...but with a simpler goal* \
Here's what we could call, a mathematical society. A genetic algorithm applied in order to
find the local(maybe global...who knows...) minimum of a set of polynomial function(s).

## How this works
Inside a python environment, execute the next command followed by the filename that contains
polynomial functions to be studied. Don't mind the size of the file, while your computer is capable
to process...
```shell
python3 mathematical_society.py -f <filename>
```
If you're interested to dig more on some hyperparameters, please modify `hyper.ini` file (DON'T TRY THIS WITH HUGE VALUES AT HOME), here's an example of it:
```ini
# How many bits this population will have, values from a power of 2 are very well accepted!
NUMBER_OF_GENES = 32
# Population size of each generation
POPULATION_SIZE = 1000
# Crossover rate of this population. How often it will occur. Here is possible to use 
# NUMBER_OF_GENES variable to execute some simple computation (e.g. 1/NUMBER_OF_GENES)
CROSSOVER_RATE = 0.95
# Mutation rate of this population. How often it will occur. Here is possible to use 
# NUMBER_OF_GENES variable to execute some simple computation (e.g. 1/NUMBER_OF_GENES)
MUTATION_RATE = 1/NUMBER_OF_GENES
# Generation defined by next variable
GENERATIONS = 50
# Range of values to work on
RANGE = [-100, 100]
```

## Results
Using the following test file: \
P.S.: These people just work with one single variable and it must be called as `x`! Yea, sorry, I told you they only execute one single task!
```text
6x^4 + 15x^3 - 12x - 10
6x^6 + 15x^5 - 12x - 10x^2
````
Here's brief log form a random run of our dear 🧠 maker:
```
Finished last generation of polynomial -> 6*x**4+15*x**3-12*x-10
Got best -> f(0.4625) = -13.7915 ...
it's genes -> [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1], at generation 28

.
.
.

Finished last generation of polynomial -> 6*x**6+15*x**5-12*x-10*x**2
Got best -> f(-2.1249) = -117.1501 ...
it's genes -> [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1], at generation 21
```
If we analyze it from a chart perspective, it's possible to conclude that on both equations, we found one of root of it 😀 

![Alt text](./media/poly_chart.png?raw=true "Chart of both equations")

## Expected to be added...
- [ ] Output charts
- [ ] More vivid experience ⁉...