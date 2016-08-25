from learn import Learn
from random import shuffle, random
import operator
from constants import PRIMES, DATA
from constants import COLOR as K

__author__ = 'carlo'
RND = 3141
ZFATOR = 2  # 2 * FATOR
TOP = 50
ZO = 3

COLORS = [K.red, K.green, K.blue, K.fuchsia, K.teal, K.navy, K.maroon, K.yellow,
          K.purple, K.darkgoldenrod, K.lime, K.aqua, K.tomato, K.olivedrab, K.dodgerblue,
          K.lightpink, K.lightgreen, K.black, K.gray, K.silver]


def tupler(x):
    return [(bit,) + tup for bit in (0, 1) for tup in tupler(x - 1)] if x else [(0,), (1,)]


class Wisard:
    """Rede neural sem peso. :ref:`wisard'
    """

    def __init__(self, data, retinasize=3 * 4, bleach=0, mapper={i: i for i in range(4)}, enf=1, sup=0):
        self.data = data
        self.bleacher, self.enf, self.sup, self.retinasize = mapper, enf, sup, retinasize
        self.cortex = self.auto_bleach = {}
        self.bleach = bleach
        self.clazzes = list(mapper.keys())
        # self.cortex = [{t: 0 for t in tupler(ramorder-1)} for _ in range(retinasize//2)]
        self.reset_brain()

    def reset_brain(self):
        self.cortex = {key: [{(a, b): 0 for a in [0, 1] for b in [0, 1]} for _ in range(self.retinasize // 2)]
                       for key in self.clazzes}
        self.auto_bleach = {key: 1 for key in self.clazzes}

    def update_balance(self):
        for clazz in self.clazzes:
            auto = sum(next(ram.values() for ram in self.cortex[clazz]))
            print(clazz, auto)
            self.auto_bleach[clazz] = auto if auto else 1
        return None

    def learn_samples(self, samples):
        return len([self.learn(s[1], self.retinify(s[2:])) for s in samples if s[1]])

    def retinify_samples(self, samples):
        [self.retinify(sample[2:]) for sample in samples]

    @staticmethod
    def retinify(retina, threshold=32, band=8):
        def retinate(value, pix=0, bnd=0):
            return [pix] * int(float(bnd + (1 - pix) * value) // ZFATOR)

        def deretinate(value, pix=0):
            return [pix] * (TOP - (band + int(float(value) // ZFATOR)))

        # print(retina, [(int(float(ZO * v) // ZFATOR), (TOP - (2 * int(float(ZO * v) // ZFATOR)))) for v in retina])
        retina = [
            (retinate(value) + retinate(value, 1, band) + deretinate(value))[:threshold]
            for value in retina]
        return [pix for line in retina for pix in line]

    def learn(self, clazz, master_retina):
        def updater(lobe, index, off):
            return {index: lobe[index] + off}

        # if random() > 0.6:
        #     return
        clazzes = self.clazzes
        shuffle(clazzes)
        for cls in clazzes:
            retina = master_retina[:]
            [lobe.update(
                updater(lobe, (retina.pop(RND % len(retina)), retina.pop(RND % len(retina))),
                        self.enf if cls == clazz else self.sup if cls != "N" else 0))
             for lobe in self.cortex[cls] if len(retina)]

    def classify_samples(self, data):
        return [(s[0], s[1], self.classify(self.retinify(s[2:]))) for s in data]

    def run(self, data):
        self.reset_brain()
        self.learn_samples(data)  # [:8])
        self.update_balance()
        res = self.classify_samples(data)
        return res

    def main(self):
        global RND
        tot = {u[0]: {key: 0 if key != "U" else str(u[0]) + " " + str(u[1]) for _, key in enumerate("VSEFU")} for u in
               self.data}
        primes = PRIMES[:]
        for _ in range(1):
            # shuffle(data)
            RND = primes.pop()
            res = self.run(self.data)
            [tot[line[0]].update({cl: tot[line[0]][cl] + s for cl, s in line[2].items()}) for line in res]
        total = list(tot.keys())
        total.sort()
        total_conf = 0
        total_sec = 0
        for line in total:
            val = dict(tot[line])
            user = val.pop("U")[-1:]
            val = list(val.items())
            # print(val)
            val.sort(key=operator.itemgetter(1), reverse=True)
            first, sec, third = val[0][1], val[1][1], val[2][1]
            confidence = min(100 * abs(first - sec) // max(abs(first), 1), 100)
            conf = confidence if (user == val[0][0]) or ("e" == user) else -confidence
            secd = min(abs(sec // max(abs(first), 1)) * conf, 100)  # if (user == val[0][0]) or ("e" == user) else 0
            # conf = 100 * abs(first-sec) // max(abs(first), abs(sec))
            # conf = 100 * (max(first, 0)-max(sec, 0)) // first
            total_conf += conf
            total_sec += secd
            # print(tot[line]["U"] + "  " + "".join(["%s:%8.0f " % (a[-3:], b) for a, b in val]), "conf: %d" % conf)
            print("{name: >42} {val} conf: {conf}".format(name=tot[line]["U"],
                                                          val="".join(["%s:%8.0f " % (a[-3:], b) for a, b in val]),
                                                          conf=conf))
        print("total confidence %d" % (total_conf // len(total)))
        return

    def classify(self, retina):
        def calculate_for_claz(lobe, clazz):
            uma_retina = retina[:]
            bleach = 0  # min(self.auto_bleach.values())
            auto = 0  # (self.auto_bleach[clazz]-bleach)/1.9
            return sum(
                neuron[(uma_retina.pop(RND % len(uma_retina)), uma_retina.pop(RND % len(uma_retina)))]
                - self.bleach - bleach - self.bleacher[clazz] - auto for neuron in lobe if len(uma_retina))

        return {clazz: calculate_for_claz(lobe, clazz) for clazz, lobe in self.cortex.items()}


def show(retina):
    for i in range(32):
        print("".join([str(retina[j + 32 * i]) for j in range(32)]))
    return


def plot(data):
    import matplotlib.pyplot as plt
    from math import pi

    step = 2*pi/125
    theta = [ang*step for ang in range(125)]

    fig = plt.figure(figsize=(9, 9))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
    for n, (title, case_data) in enumerate(data):
        print("plot(data)", title, len(case_data))
        ax = fig.add_subplot(2, 2, n + 1, projection='polar')
        # plt.rgrids([0.2, 0.4, 0.6, 0.8])
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        for color, line in zip(COLORS, case_data):
            ax.plot(theta, line, color=color, linewidth=2)

        ax.set_rmax(15.0)
        ax.grid(True)
    # add legend relative to top-left plot
    # plt.subplot(2, 2, 1)
    # labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
    # legend = plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
    # plt.setp(legend.get_texts(), fontsize='small')

    plt.figtext(0.5, 0.965, 'Classes de aluno segundo a transitividade',
                ha='center', color='black', weight='bold', size='large')
    plt.show()


def _plot(data):
    import matplotlib.pyplot as plt
    from math import pi

    step = 2*pi/125
    theta = [ang*step for ang in range(125)]

    ax = plt.subplot(111, projection='polar')
    for color, line in zip(COLORS, data):
        ax.plot(theta, line, color=color, linewidth=2)
    ax.set_rmax(15.0)
    ax.grid(True)

    ax.set_title("A line plot on a polar axis", va='bottom')
    plt.show()


def main(_):
    endtime = 128
    data = Learn().build_with_User_table_for_prog(slicer=endtime)
    print(len(data[0]))
    data = [line[:2] + [float(t) - float(t0) + 10 for t, t0 in zip(line[3:endtime], line[2:endtime])] for line in data]
    print("Tabela gerada por rede neural sem peso para derivada segunda do tempo com prognóstico da carla")
    # bleacher = dict(V=805, S=-6, E=81, F=154)
    bleacher = dict(V=1329, S=-9, E=29, F=138)
    w = Wisard(data, 32 * endtime, bleach=838, mapper=bleacher, enf=239, sup=18)
    # bleacher = dict(V=603, S=0, E=81, F=154)
    # w = Wisard(data, 32 * endtime, bleach=600, mapper=bleacher, enf=110, sup=20)
    w.main()
    print(len(data[0][2:]))
    clazz_names = "V:Verdadeiro Sucesso,S:Sucesso Mínimo,E:Expulsão Simbólica,F:Falso Sucesso"
    clazz_name = {key: name for key, name in (kv.split(":")for kv in clazz_names.split(","))}
    clazz_data = {clazz_name[name]: [(dat[2:]+([0.0]*120))[:125] for dat in data if dat[1] == name] for name in clazz_name.keys()}
    plot_clazz = [(claz_name, clazz_data[claz_name]) for claz_name in clazz_data.keys()]
    plot(plot_clazz)
    # for dat in data:
    #     plot((dat[2:]+([0.0]*120))[:125])

if __name__ == '__main__':
    main(DATA)
    # print(PRIMES)
