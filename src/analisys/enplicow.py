from learn import Learn
from random import shuffle
import operator
from constants import PRIMES, DATA
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

    def __init__(self, retinasize=3 * 4, bleach=0, ramorder=2, mapper={i: i for i in range(4)}, enf=1, sup=0):
        self.bleacher, self.enf, self.sup = mapper, enf, sup
        self.clazzes = list(mapper.keys())
        # self.cortex = [{t: 0 for t in tupler(ramorder-1)} for _ in range(retinasize//2)]
        self.cortex = {key: [{(a, b): 0 for a in [0, 1] for b in [0, 1]} for _ in range(retinasize // 2)]
                       for key in mapper.keys()}
        self.bleach = bleach

    def learn_samples(self, samples):
        return len([self.learn(s[1], self.retinify(s[2:])) for s in samples if s[1]])

    def retinify_samples(self, samples):
        [self.retinify(sample[2:]) for sample in samples]

    def retinify(self, retina, threshold=32, band=8):
        def retinate(value, pix=0, bnd=0):
            return [pix] * int(float(bnd + (1-pix) * value) // ZFATOR)

        def deretinate(value, pix=0):
            return [pix] * (TOP - (band + int(float(value) // ZFATOR)))
        # print(retina, [(int(float(ZO * v) // ZFATOR), (TOP - (2 * int(float(ZO * v) // ZFATOR)))) for v in retina])
        BDATA = [
            (retinate(value)+retinate(value, 1, band)+deretinate(value))[:threshold]
            for value in retina]
        return [pix for line in BDATA for pix in line]

    def _retinify(self, retina, threshold=32):
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

    def learn(self, clazz, master_retina, offset=10):
        def updater(lobe, index, off):
            return {index: lobe[index] + off}
        clazzes = self.clazzes
        shuffle(clazzes)
        for cls in clazzes:
            retina = master_retina[:]
            [lobe.update(
                updater(lobe, (retina.pop(RND % len(retina)), retina.pop(RND % len(retina))),
                        self.enf if cls == clazz else self.sup))
             for lobe in self.cortex[cls] if len(retina)]

    def _classify(self, retina):
        x = (len(retina) // 2)
        return ([self.cortex[ram][(retina.pop(RND % len(retina)), retina.pop(RND % len(retina)))] - self.bleach
                 for ram in range(x)])

    def classify_samples(self, data):
        return [(s[0], s[1], self.classify(self.retinify(s[2:]))) for s in data]

    def classify(self, retina):
        def calculate_for_claz(lobe, clazz):
            uma_retina = retina[:]
            return sum(neuron[(uma_retina.pop(RND % len(uma_retina)), uma_retina.pop(RND % len(uma_retina)))]
                       - self.bleach - self.bleacher[clazz] for neuron in lobe if len(uma_retina))
        return {clazz: calculate_for_claz(lobe, clazz) for clazz, lobe in self.cortex.items()}


def show(retina):
    for i in range(32):
            print("".join([str(retina[j+32*i])for j in range(32)]))
    return


def run(data):
    # bleacher = dict(V=60, S=0, E=8, F=15)
    # w = Wisard(32 * 32, bleach=62, mapper=bleacher, enf=11, sup=2)
    bleacher = dict(V=60, S=0, E=8, F=15)
    w = Wisard(32 * 64, bleach=62, mapper=bleacher, enf=11, sup=2)
    # show(w.retinify(data[0][2:]))
    # return
    w.learn_samples(data)
    res = w.classify_samples(data)
    return res


def _run(data):
    cls = "Iris-setosa Iris-versicolor Iris-virginica".split()
    w = Wisard(22 * 4, bleach=500, mapper={key: value for value, key in enumerate(cls)}, enf=10, sup=1)
    # show(w.retinify(data[0][2:]))
    # return
    w.learn_samples(data)
    res = w.classify_samples(data)
    return res


def _main(DATA):
    cls = "U Iris-setosa Iris-versicolor Iris-virginica".split()
    data = [[i, line.split(",")[-1]]+[float(p) for p in line.split(",")[:-1]] for i, line in enumerate(DATA)]
    tot = {u[0]: {key: 0 if key != "U" else str(u[0])+" "+str(u[1]) for _, key in enumerate(cls)} for u in data}
    primes = PRIMES[:]
    for _ in range(2):
        shuffle(data)
        RND = primes.pop()
        res = run(data)
        [tot[line[0]].update({cl:  tot[line[0]][cl] + s for cl, s in line[2].items()}) for line in res]
    total = list(tot.keys())
    total.sort()
    total_conf = 0
    for line in total:
        val = dict(tot[line])
        val.pop("U")
        val = list(val.items())
        # print(val)
        val.sort(key=operator.itemgetter(1), reverse=True)
        first, sec = val[0][1], val[1][1]
        conf = min(100 * abs(first-sec) // abs(first), 100)
        # conf = 100 * abs(first-sec) // max(abs(first), abs(sec))
        # conf = 100 * (max(first, 0)-max(sec, 0)) // first
        total_conf += conf
        print(tot[line]["U"] + "  " + "".join(["%s:%8.0f " % (a[-3:], b) for a, b in val]), "conf: %d" % conf)
        # print("{U}: {tot}".format(result))
    print("total confidence %d" % (total_conf//len(total)))
    return


def main(_):
    data = Learn().build_with_User_table_for_prog()
    data = [line[:2]+[float(t)-float(t0)+10 for t, t0 in zip(line[3:32], line[2:32])] for line in data]
    print("Tabela gerada por rede neural sem peso para derivada segunda do tempo com prognóstico da carla")
    tot = {u[0]: {key: 0 if key != "U" else str(u[0])+" "+str(u[1]) for _, key in enumerate("VSEFU")} for u in data}
    primes = PRIMES[:]
    for _ in range(20):
        shuffle(data)
        RND = primes.pop()
        res = run(data)
        [tot[line[0]].update({cl:  tot[line[0]][cl] + s for cl, s in line[2].items()}) for line in res]
    total = list(tot.keys())
    total.sort()
    total_conf = 0
    for line in total:
        val = dict(tot[line])
        user = val.pop("U")[-1:]
        val = list(val.items())
        # print(val)
        val.sort(key=operator.itemgetter(1), reverse=True)
        first, sec = val[0][1], val[1][1]
        conf = min(100 * abs(first-sec) // abs(first), 100) if (user == val[0][0]) or ("e" == user) else 0
        # conf = 100 * abs(first-sec) // max(abs(first), abs(sec))
        # conf = 100 * (max(first, 0)-max(sec, 0)) // first
        total_conf += conf
        # print(tot[line]["U"] + "  " + "".join(["%s:%8.0f " % (a[-3:], b) for a, b in val]), "conf: %d" % conf)
        print("{name: >42} {val} conf: {conf}".format(name=tot[line]["U"], val="".join(["%s:%8.0f " % (a[-3:], b) for a, b in val]) , conf=conf))
        # print("{U}: {tot}".format(result))
    print("total confidence %d" % (total_conf//len(total)))
    return

if __name__ == '___main__':
    main(DATA)

if __name__ == '__main__':
    main(DATA)
    # print(PRIMES)
