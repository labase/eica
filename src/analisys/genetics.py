from enum import Enum
import random
__author__ = "elek"
__date__ = "$Dec 16, 2010 5:36:12 PM$"


def selection(population, fit):
    return [a if (fit(a) < fit(b)) else b for _ in (0, 1) for a, b in [random.sample(population, 2)]]


def crossover(c1, c2):
    if random.randint(0, 10) < 3:
        sep = random.randint(0, len(c1) - 1)
        return c1[:sep] + c2[sep:], c2[:sep] + c1[sep:]
    else:
        return c1, c2


def mutation(c1):
    if random.randint(0, 10) < 2:
        sep = random.randint(0, len(c1) - 1)
        off = random.randint(-5, 5)
        return c1[:sep] + chr(ord(c1[sep]) + off) + c1[sep + 1:]
    else:
        return c1


def fitnesse(ch, target):
    if len(target) != len(ch):
        return None
    else:
        return sum(abs(ord(targ) - ord(sample)) for targ, sample in zip(list(ch), list(target)))


class GA:
    def __init__(self, target, fitnesse_function, selection_function, crossover_function,
                 mutation_function, popul=30):
        self.target = target
        self.fitnesse = fitnesse_function
        self.fit = lambda x: self.fitnesse(x, self.target)
        self.mutation = mutation_function
        self.crossover = crossover_function
        self.selection = selection_function
        self.dnasize = dnasize = len(target)
        self.popul = popul

        class Gene:
            def __init__(self, fenotype):
                self.fenotype = fenotype
                self.fitness = fitnesse_function(fenotype, target)

            def __hash__(self,):
                return hash(self.fenotype)

            def __lt__(self, other):
                return self.fitness < other.fitness

            def parts(self):
                return self.fitness, self.fenotype

            def date(self, consort):
                return self if self < consort else consort

            def mate(self, consort):
                if self < consort:
                    return self
                me, consort = list(self.fenotype), list(consort.fenotype)
                xover = random.randint(-dnasize, dnasize)
                mutat = random.randint(-dnasize * 1, dnasize)
                return Gene(
                    "".join(chr(ord(male_gene) + xover // 2) if seq == mutat else male_gene
                    if seq < xover else female_gene for seq, (male_gene, female_gene) in enumerate(zip(me, consort))))

        self.population = ["".join([chr(i) for i in random.sample(range(97, 122), self.dnasize)]) for _ in range(popul)]
        self.fit_population = [Gene(fenotype) for fenotype in self.population]

    def find_best(self, population, fitnes):
        return min((fitnes(sample), sample) for sample in population)[1]

    def meiosis(self, male, female):
        xover = random.randint(-self.dnasize, self.dnasize)
        mutat = random.randint(-self.dnasize*4, self.dnasize)
        return [chr(ord(male_gene) + xover // 2) if seq < mutat else male_gene
                if seq < xover else female_gene for seq, (male_gene, female_gene) in enumerate(zip(male, female))]

    def dating(self, populace):
        return min(random.sample(populace, 2)), min(random.sample(populace, 2))

    def natural_selection(self):
        while len(self.fit_population) <= self.popul:
            self.fit_population.sort()
            population = self.fit_population
            elite_cut = self.popul//10
            populace = population[elite_cut:]
            elite = population[:elite_cut]
            self.fit_population += elite + [a.mate(b) for _ in populace for a, b in [self.dating(populace)]]
            self.fit_population = list(set(self.fit_population))
        while len(self.fit_population) > self.popul:
            self.fit_population.remove(max(random.sample(self.fit_population, 2)))
        self.fit_population.sort()

    def life(self):
        for generation in range(190):
            self.natural_selection()
            fitness, best = self.fit_population[0].parts()
            # print([a.fitness for a in self.fit_population])
            print([(a.fitness, a.fenotype) for a in self.fit_population])
            print("{2}. generation --  best: {0} ({1})".format(best, fitness, generation))
            if fitness == 0:
                break

    def live(self):
        current_gen = self.population  # self.initPopulation(30, 11)
        f = lambda x: self.fitnesse(x, self.target)
        for i in range(150):
            next_gen = []
            while len(next_gen) < len(current_gen):
                p1, p2 = self.selection(current_gen, f)
                c1, c2 = self.crossover(p1, p2)
                next_gen.append(mutation(c1))
                next_gen.append(mutation(c2))
            current_gen = next_gen
            best = self.find_best(current_gen, f)
            b = f(best)
            print("{2}. generation --  best: {0} ({1})".format(best, b, i))
            if b == 0:
                break

if __name__ == '__main__':
    ga = GA("helloworld", fitnesse, selection, crossover, mutation)
    ga.life()
