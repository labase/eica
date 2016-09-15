import random
import operator
from enplicow import Wisard
import sys
import math
__author__ = "elek"
__date__ = "$Dec 16, 2010 5:36:12 PM$"
C, S = "0", "9"
A, Z, AZ = ord(C), ord(S), ord(S) - ord(C) + 1
DATA = []


def signal_handler(*_):
    wfitnesse(GA.GA.fit_population[0].fenotype, result=True)
    sys.exit(0)


def fitnesse(ch, target):
        return sum(abs(ord(targ) - ord(sample)) for targ, sample in zip(list(ch), list(target)))


def wwfitnesse(ch, _=0, result=False):
    v, s, f, e =\
        int(ch[:4]), int(ch[4:7]), int(ch[7:10]), int(ch[10:13])
    bleacher = dict(V=v, S=s, E=e, F=f)
    # print(v, s, f, e, b, a, d, DATA[0])
    w = Wisard(DATA, 32 * 128, bleach=0, mapper=bleacher, enf=100, sup=10)
    confidence = w.single(print_result=result)
    print(confidence, 100 - confidence, "v:%d, s:%d, f:%d, e:%d" % (v, s, f, e))
    return 100 - confidence


def wfitnesse(ch, _=0, result=False):
    v, s, f, e, b, a, d =\
        int(ch[:4]), int(ch[4:7]), int(ch[7:10]), int(ch[10:13]), int(ch[13:16]), int(ch[16:19]), int(ch[19:21])
    bleacher = dict(V=v, S=s, E=e, F=f)
    # print(v, s, f, e, b, a, d, DATA[0])
    w = Wisard(DATA, 32 * 128, bleach=b, mapper=bleacher, enf=a, sup=d)
    confidence = w.single(result)
    print(confidence, 100 - confidence, "v:%d, s:%d, f:%d, e:%d, b:%d, a:%d, d:%d" % (v, s, f, e, b, a, d))
    return 100 - confidence


class SA:
    genes = dict()
    SA = None
    SASample = None

    def __init__(self, target, fitnesse_function, temperature_end=0, cooling_factor=0.9):
        self.dnasize = len(target)
        self.fitnesse = fitnesse_function
        self.temperature_end,  self.cooling_factor = temperature_end, cooling_factor
        self.best = ""
        SA.SA = self

        class Sample:
            def __init__(self, fenotype=None):
                self.fenotype = fenotype or "".join([chr(i) for i in random.sample(list(range(A, Z))*4, self.dnasize)])
                self.fitness = SA.genes[fenotype] if fenotype in SA.genes else fitnesse_function(fenotype, target)
                SA.genes[fenotype] = self
        self.current_sample = Sample()

        SA.SASample = Sample

    def anneal(self):
        temperature = 1000

        while temperature > self.temperature_end:
            new_sample = SA.SASample()
            diff = new_sample.fitness - self.current_sample.fitness
            if diff < 0 or math.exp(-diff / temperature) > random.random():
                self.current_sample = new_sample
            temperature *= self.cooling_factor


class GA:
    genes = dict()
    GA = None

    def __init__(self, target, fitnesse_function, popul=15):
        self.target = target
        self.fitnesse = fitnesse_function
        self.fit = lambda x: self.fitnesse(x, self.target)
        self.dnasize = dnasize = len(target)
        self.popul = popul
        self.best = ""
        GA.GA = self

        class Gene:

            def __init__(self, fenotype):
                self.fenotype = fenotype
                self.fitness = GA.genes[fenotype] if fenotype in GA.genes else fitnesse_function(fenotype, target)
                GA.genes[fenotype] = self.fitness

            def __hash__(self,):
                return hash(self.fenotype)

            def __eq__(self, other):
                return self.fenotype == other.fenotype

            def __ne__(self, other):
                return self.fenotype != other.fenotype

            def __lt__(self, other):
                return self.fitness < other.fitness

            def parts(self):
                return self.fitness, self.fenotype

            def date(self, consort):
                return self if self < consort else consort

            def mate(self, consort):
                def mutate(gene, sequence):
                    return chr((ord(gene)-A+xover//2) % AZ + A)\
                        if sequence == random.randint(-dnasize // 2, dnasize) else gene

                def cross_over(left, right, sequence):
                    return left if sequence < xover else right, sequence
                me, consort = list(self.fenotype), list(consort.fenotype)
                xover = random.randint(-dnasize // 2, dnasize)
                # mutat = random.randint(-dnasize * 4, dnasize)
                return [
                    Gene("".join(
                        mutate(*cross_over(male, female, seq)) for seq, (female, male) in enumerate(zip(me, consort)))),
                    Gene("".join(
                        mutate(*cross_over(male, female, seq)) for seq, (male, female) in enumerate(zip(me, consort))))]

        self.population = ["".join([chr(i) for i in random.sample(list(range(A, Z))*4, self.dnasize)])
                           for _ in range(popul*4)]
        self.population = [(self.fitnesse(sample), sample) for sample in self.population]
        self.population.sort(key=operator.itemgetter(0), reverse=True)
        self.population = [name for _, name in self.population[:popul]]
        self.fit_population = [Gene(fenotype) for fenotype in self.population]

    def natural_selection(self):

        def dating():
            return min(random.sample(populace, 2)).mate(min(random.sample(populace, 2)))
        while len(self.fit_population) <= self.popul:
            self.fit_population.sort()
            population = self.fit_population
            elite_cut = self.popul//20
            populace = population[elite_cut:]
            elite = population[:elite_cut]
            self.fit_population += elite + [a for _ in populace for a in dating()]
            self.fit_population = list(set(self.fit_population))
        while len(self.fit_population) > self.popul:
            self.fit_population.remove(max(random.sample(self.fit_population, 2)))
        self.fit_population.sort()

    def life(self):
        for generation in range(390):
            try:
                self.natural_selection()
                fitness, best = self.fit_population[0].parts()
                # print([a.fitness for a in self.fit_population])
                print([(a.fitness, a.fenotype) for a in self.fit_population])
                print("{2}. generation --  best: {0} ({1})".format(best, fitness, generation))
                if fitness == 0:
                    break
            except (KeyboardInterrupt, SystemExit):
                print("Result: ", self.fit_population[0].fenotype)
                print("Result: ", self.fitnesse(self.fit_population[0].fenotype, True))
                sys.exit(0)
        print(len(GA.genes))


def main():
    global DATA
    import csv
    with open('table.tab', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        data = [row for row in spamreader][3:]
        endtime = 128
        # data = Learn().build_with_User_table_for_prog(slicer=endtime)
        print(data[0])
        DATA = [(line[0], line[1],
                 Wisard.retinify([float(t) - float(t0) + 10 for t, t0 in zip(line[3:endtime], line[2:endtime])]))
                for line in data]

if __name__ == '__main__':
    main()
    ga = GA("0123456789987", wwfitnesse)  # , selection, crossover, mutation)
    # ga = GA("helloworld", fitnesse)  # , selection, crossover, mutation)
    ga.life()
