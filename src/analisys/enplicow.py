from learn import Learn
from random import shuffle

__author__ = 'carlo'
RND = 3141
SBLEACH = 3
EBLEACH = 1
IBLEACH = 1
FATOR = 1
ZFATOR = 2  # 2 * FATOR
TOP = 50 // FATOR
ZO = 3


def tupler(x):
    return [(bit,) + tup for bit in (0, 1) for tup in tupler(x - 1)] if x else [(0,), (1,)]


class Wisard:
    """Rede neural sem peso. :ref:`wisard'
    """

    def __init__(self, retinasize=3 * 4, bleach=0, ramorder=2, mapper={i: i for i in range(4)}):
        self.mapper = mapper
        self.clazzes = mapper.keys()
        # self.cortex = [{t: 0 for t in tupler(ramorder-1)} for _ in range(retinasize//2)]
        self.cortex = {key: [{(a, b): 0 for a in [0, 1] for b in [0, 1]} for _ in range(retinasize // 2)]
                       for key in mapper.keys()}
        self.bleach = bleach

    def learn_samples(self, samples):
        return len([self.learn(s[1], self.retinify(s[2:])) for s in samples if s[1]])

    def retinify_samples(self, samples):
        [self.retinify(sample[2:]) for sample in samples]

    def retinify(self, retina, threshold=32):
        def retinate(value, pix=0):
            return [pix] * int(float(ZO * value) // ZFATOR)

        def deretinate(value, pix=0):
            return [pix] * (TOP - (2 * int(float(ZO * value) // ZFATOR)))
        # print(retina, [(int(float(ZO * v) // ZFATOR), (TOP - (2 * int(float(ZO * v) // ZFATOR)))) for v in retina])
        BDATA = [
            (retinate(value)+retinate(value, 1)+deretinate(value))[:threshold]
            for value in retina]
        return [pix for line in BDATA for pix in line]

    def _learn(self, clazz, retina, offset=1):
        def updater(ram, index):
            return {index: self.cortex[clazz][ram][index] + offset}

        # print(len(retina)//2)
        x = (len(retina) // 2)
        [self.cortex[clazz][ram].update(updater(ram, (retina.pop(RND % len(retina)), retina.pop(RND % len(retina)))))
         for ram in range(x)]

    def learn(self, clazz, retina, offset=2):
        def updater(lobe, index, off):
            return {index: lobe[index] + off}

        [lobe.update(
            updater(lobe, (retina.pop(RND % len(retina)), retina.pop(RND % len(retina))),
                    offset if cls == clazz else -offset/4.0))
         for cls in self.clazzes for lobe in self.cortex[cls] if len(retina)]

    def _classify(self, retina):
        x = (len(retina) // 2)
        return ([self.cortex[ram][(retina.pop(RND % len(retina)), retina.pop(RND % len(retina)))] - self.bleach
                 for ram in range(x)])

    def classify_samples(self, data):
        return [(s[1], self.classify(self.retinify(s[2:]))) for s in data]

    def classify(self, retina):
        def calculate_for_claz(lobe):
            uma_retina = retina[:]
            return sum(neuron[(uma_retina.pop(RND % len(uma_retina)), uma_retina.pop(RND % len(uma_retina)))]
                       - self.bleach for neuron in lobe if len(uma_retina))
        return {clazz: calculate_for_claz(lobe) for clazz, lobe in self.cortex.items()}


def show(retina):
    for i in range(4):
            print("".join([str(retina[j+32*i])for j in range(32)]))
    return


def run(data):
    cls = "Iris-setosa Iris-versicolor Iris-virginica".split()
    w = Wisard(32 * 4, bleach=1, mapper={key: value for value, key in enumerate(cls)})
    # show(w.retinify(data[0][2:]))
    # return
    w.learn_samples(data)
    res = w.classify_samples(data)
    return res


def main(DATA):
    cls = "U Iris-setosa Iris-versicolor Iris-virginica".split()
    data = [[str(i), line.split(",")[-1]]+[float(p) for p in line.split(",")[:-1]] for i, line in enumerate(DATA)]
    tot = [{key: 0 if key != "U" else str(u[0])+" "+str(u[1]) for _, key in enumerate(cls)} for u in data]
    for _ in range(100):
        shuffle(data)
        res = run(data)
        # print(res[0])
        [tt.update({cl:  tt[cl] + s for cl, s in line[1].items()}) for tt, line in zip(tot, res)]

    for line in tot:
        print(line)
    return


def _main():
    w = Wisard(32 * 32, bleach=5, mapper={key: value for value, key in enumerate("VSEF")})
    data = Learn().build_User_table_for_prog()
    data = [line[:2]+[float(t)-float(t0)+10 for t, t0 in zip(line[3:32], line[2:32])] for line in data]
    tot = [{key: 0 if key != "U" else u[0]+" "+str(u[1]) for _, key in enumerate("VSEFU")} for u in data]
    for _ in range(20):
        shuffle(data)
        res = run(data)
        [tt.update({cl:  tt[cl] + s for cl, s in line[1].items()}) for tt, line in zip(tot, res)]

    for line in tot:
        print(line)
    return

if __name__ == '___main__':
    main()

DATA = '''5.1,3.5,1.4,0.2,Iris-setosa
4.9,3.0,1.4,0.2,Iris-setosa
4.7,3.2,1.3,0.2,Iris-setosa
4.6,3.1,1.5,0.2,Iris-setosa
5.0,3.6,1.4,0.2,Iris-setosa
5.4,3.9,1.7,0.4,Iris-setosa
4.6,3.4,1.4,0.3,Iris-setosa
5.0,3.4,1.5,0.2,Iris-setosa
4.4,2.9,1.4,0.2,Iris-setosa
4.9,3.1,1.5,0.1,Iris-setosa
5.4,3.7,1.5,0.2,Iris-setosa
4.8,3.4,1.6,0.2,Iris-setosa
4.8,3.0,1.4,0.1,Iris-setosa
4.3,3.0,1.1,0.1,Iris-setosa
5.8,4.0,1.2,0.2,Iris-setosa
5.7,4.4,1.5,0.4,Iris-setosa
5.4,3.9,1.3,0.4,Iris-setosa
5.1,3.5,1.4,0.3,Iris-setosa
5.7,3.8,1.7,0.3,Iris-setosa
5.1,3.8,1.5,0.3,Iris-setosa
5.4,3.4,1.7,0.2,Iris-setosa
5.1,3.7,1.5,0.4,Iris-setosa
4.6,3.6,1.0,0.2,Iris-setosa
5.1,3.3,1.7,0.5,Iris-setosa
4.8,3.4,1.9,0.2,Iris-setosa
5.0,3.0,1.6,0.2,Iris-setosa
5.0,3.4,1.6,0.4,Iris-setosa
5.2,3.5,1.5,0.2,Iris-setosa
5.2,3.4,1.4,0.2,Iris-setosa
4.7,3.2,1.6,0.2,Iris-setosa
4.8,3.1,1.6,0.2,Iris-setosa
5.4,3.4,1.5,0.4,Iris-setosa
5.2,4.1,1.5,0.1,Iris-setosa
5.5,4.2,1.4,0.2,Iris-setosa
4.9,3.1,1.5,0.1,Iris-setosa
5.0,3.2,1.2,0.2,Iris-setosa
5.5,3.5,1.3,0.2,Iris-setosa
4.9,3.1,1.5,0.1,Iris-setosa
4.4,3.0,1.3,0.2,Iris-setosa
5.1,3.4,1.5,0.2,Iris-setosa
5.0,3.5,1.3,0.3,Iris-setosa
4.5,2.3,1.3,0.3,Iris-setosa
4.4,3.2,1.3,0.2,Iris-setosa
5.0,3.5,1.6,0.6,Iris-setosa
5.1,3.8,1.9,0.4,Iris-setosa
4.8,3.0,1.4,0.3,Iris-setosa
5.1,3.8,1.6,0.2,Iris-setosa
4.6,3.2,1.4,0.2,Iris-setosa
5.3,3.7,1.5,0.2,Iris-setosa
5.0,3.3,1.4,0.2,Iris-setosa
7.0,3.2,4.7,1.4,Iris-versicolor
6.4,3.2,4.5,1.5,Iris-versicolor
6.9,3.1,4.9,1.5,Iris-versicolor
5.5,2.3,4.0,1.3,Iris-versicolor
6.5,2.8,4.6,1.5,Iris-versicolor
5.7,2.8,4.5,1.3,Iris-versicolor
6.3,3.3,4.7,1.6,Iris-versicolor
4.9,2.4,3.3,1.0,Iris-versicolor
6.6,2.9,4.6,1.3,Iris-versicolor
5.2,2.7,3.9,1.4,Iris-versicolor
5.0,2.0,3.5,1.0,Iris-versicolor
5.9,3.0,4.2,1.5,Iris-versicolor
6.0,2.2,4.0,1.0,Iris-versicolor
6.1,2.9,4.7,1.4,Iris-versicolor
5.6,2.9,3.6,1.3,Iris-versicolor
6.7,3.1,4.4,1.4,Iris-versicolor
5.6,3.0,4.5,1.5,Iris-versicolor
5.8,2.7,4.1,1.0,Iris-versicolor
6.2,2.2,4.5,1.5,Iris-versicolor
5.6,2.5,3.9,1.1,Iris-versicolor
5.9,3.2,4.8,1.8,Iris-versicolor
6.1,2.8,4.0,1.3,Iris-versicolor
6.3,2.5,4.9,1.5,Iris-versicolor
6.1,2.8,4.7,1.2,Iris-versicolor
6.4,2.9,4.3,1.3,Iris-versicolor
6.6,3.0,4.4,1.4,Iris-versicolor
6.8,2.8,4.8,1.4,Iris-versicolor
6.7,3.0,5.0,1.7,Iris-versicolor
6.0,2.9,4.5,1.5,Iris-versicolor
5.7,2.6,3.5,1.0,Iris-versicolor
5.5,2.4,3.8,1.1,Iris-versicolor
5.5,2.4,3.7,1.0,Iris-versicolor
5.8,2.7,3.9,1.2,Iris-versicolor
6.0,2.7,5.1,1.6,Iris-versicolor
5.4,3.0,4.5,1.5,Iris-versicolor
6.0,3.4,4.5,1.6,Iris-versicolor
6.7,3.1,4.7,1.5,Iris-versicolor
6.3,2.3,4.4,1.3,Iris-versicolor
5.6,3.0,4.1,1.3,Iris-versicolor
5.5,2.5,4.0,1.3,Iris-versicolor
5.5,2.6,4.4,1.2,Iris-versicolor
6.1,3.0,4.6,1.4,Iris-versicolor
5.8,2.6,4.0,1.2,Iris-versicolor
5.0,2.3,3.3,1.0,Iris-versicolor
5.6,2.7,4.2,1.3,Iris-versicolor
5.7,3.0,4.2,1.2,Iris-versicolor
5.7,2.9,4.2,1.3,Iris-versicolor
6.2,2.9,4.3,1.3,Iris-versicolor
5.1,2.5,3.0,1.1,Iris-versicolor
5.7,2.8,4.1,1.3,Iris-versicolor
6.3,3.3,6.0,2.5,Iris-virginica
5.8,2.7,5.1,1.9,Iris-virginica
7.1,3.0,5.9,2.1,Iris-virginica
6.3,2.9,5.6,1.8,Iris-virginica
6.5,3.0,5.8,2.2,Iris-virginica
7.6,3.0,6.6,2.1,Iris-virginica
4.9,2.5,4.5,1.7,Iris-virginica
7.3,2.9,6.3,1.8,Iris-virginica
6.7,2.5,5.8,1.8,Iris-virginica
7.2,3.6,6.1,2.5,Iris-virginica
6.5,3.2,5.1,2.0,Iris-virginica
6.4,2.7,5.3,1.9,Iris-virginica
6.8,3.0,5.5,2.1,Iris-virginica
5.7,2.5,5.0,2.0,Iris-virginica
5.8,2.8,5.1,2.4,Iris-virginica
6.4,3.2,5.3,2.3,Iris-virginica
6.5,3.0,5.5,1.8,Iris-virginica
7.7,3.8,6.7,2.2,Iris-virginica
7.7,2.6,6.9,2.3,Iris-virginica
6.0,2.2,5.0,1.5,Iris-virginica
6.9,3.2,5.7,2.3,Iris-virginica
5.6,2.8,4.9,2.0,Iris-virginica
7.7,2.8,6.7,2.0,Iris-virginica
6.3,2.7,4.9,1.8,Iris-virginica
6.7,3.3,5.7,2.1,Iris-virginica
7.2,3.2,6.0,1.8,Iris-virginica
6.2,2.8,4.8,1.8,Iris-virginica
6.1,3.0,4.9,1.8,Iris-virginica
6.4,2.8,5.6,2.1,Iris-virginica
7.2,3.0,5.8,1.6,Iris-virginica
7.4,2.8,6.1,1.9,Iris-virginica
7.9,3.8,6.4,2.0,Iris-virginica
6.4,2.8,5.6,2.2,Iris-virginica
6.3,2.8,5.1,1.5,Iris-virginica
6.1,2.6,5.6,1.4,Iris-virginica
7.7,3.0,6.1,2.3,Iris-virginica
6.3,3.4,5.6,2.4,Iris-virginica
6.4,3.1,5.5,1.8,Iris-virginica
6.0,3.0,4.8,1.8,Iris-virginica
6.9,3.1,5.4,2.1,Iris-virginica
6.7,3.1,5.6,2.4,Iris-virginica
6.9,3.1,5.1,2.3,Iris-virginica
5.8,2.7,5.1,1.9,Iris-virginica
6.8,3.2,5.9,2.3,Iris-virginica
6.7,3.3,5.7,2.5,Iris-virginica
6.7,3.0,5.2,2.3,Iris-virginica
6.3,2.5,5.0,1.9,Iris-virginica
6.5,3.0,5.2,2.0,Iris-virginica
6.2,3.4,5.4,2.3,Iris-virginica
5.9,3.0,5.1,1.8,Iris-virginica'''.split()

if __name__ == '__main__':
    main(DATA)
