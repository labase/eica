# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Enplicaw
# Copyright 2013-2015 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
#
# Enplicaw é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>

from random import choice
import operator
from constants import PRIMES, DATA
from constants import COLOR as K

__author__ = 'carlo'
__version__ = "0.3.0"
RND = 3141
ZFATOR = 2  # 2 * FATOR
TOP = 50
ZO = 3
LGN = -1000
COLORS = [K.red, K.green, K.blue, K.fuchsia, K.teal, K.navy, K.maroon, K.yellow,
          K.purple, K.darkgoldenrod, K.lime, K.aqua, K.tomato, K.olivedrab, K.dodgerblue,
          K.lightpink, K.lightgreen, K.black, K.gray, K.silver]


def tupler(x):
    return [(bit,) + tup for bit in (0, 1) for tup in tupler(x - 1)] if x else [(0,), (1,)]


class Wisard:
    """Rede neural sem peso. :ref:`wisard'
    """

    def __init__(self, data, retinasize=3 * 4, bleach=0, mapper={i: i for i in range(4)}, enf=1, sup=0,
                 unsupervised=False):
        self.data = data
        self.bleacher, self.enf, self.sup, self.retinasize, self.unsupervised = \
            mapper, enf, sup, retinasize, unsupervised
        self.auto_bleach = {}
        self.bleach = bleach
        self.clazzes = list(mapper.keys())

        class Cortex:

            def __init__(self, data_, clazz, bleaching):
                self.data, self.clazz, self.bleacher, self.cortex = data_, clazz, bleaching, [{(0, 0): []}]
                self.reset_cortex()

            def reset_cortex(self):
                lgn = list(range(retinasize))
                self.cortex = [{(a, b): 0 if not b == LGN else lgn.pop(RND % len(lgn))
                                for a in [0, 1] for b in [0, 1, LGN]} for _ in range(retinasize // 2)]

            def learn(self, sample_clazz, master_retina):
                cortex, clazz = self.cortex, self.clazz
                for neuron in cortex:
                    neuron[(master_retina[neuron[(0, LGN)]], master_retina[neuron[(1, LGN)]])
                           ] += enf if sample_clazz == clazz else sup if sample_clazz != "N" else 0

            def classify(self):
                retina = self.data
                if not retina:
                    return
                return {self.clazz: sum(
                    neuron[(retina[neuron[(0, LGN)]], retina[neuron[(1, LGN)]])]
                    for neuron in self.cortex) - len(retina) * (self.bleach + self.bleacher)}

        self.cortex = [Cortex(data, clazz, bleach) for clazz, bleach in mapper.items()]
        self.reset_brain()

    def reset_brain(self):
        [cortex.reset_cortex() for cortex in self.cortex]

    def learn_samples(self):
        enf, sup, samples, unsupervised, clazzes = self.enf, self.sup, self.data, self.unsupervised, self.clazzes
        # print(len(samples[0][2]), samples[0])
        cortices = [(cortex.clazz, cortex.cortex) for cortex in self.cortex]
        for _, sample_clazz, master_retina in samples:
            if unsupervised:
                sample_clazz = choice(clazzes)
                # print(sample_clazz)
            if sample_clazz:
                for clazz, cortex in cortices:
                    for neuron in cortex:
                        neuron[(master_retina[neuron[(0, LGN)]], master_retina[neuron[(1, LGN)]])
                               ] += enf if sample_clazz == clazz else sup if sample_clazz != "N" else 0

    def rank_samples(self):
        histo_classes = {clazz: [] for clazz in self.clazzes}
        res = self.classify_samples()
        [histo_classes[cl].append((s, name)) for name, _, line in res for cl, s in line.items()]
        ordered_histos = {}
        ordered_notes = {}
        ordered_cutter = {}
        for clazz, histo in histo_classes.items():
            histo.sort()
            minh = histo[0][0]
            ordered_histos[clazz] = [name for _, name in histo]
            ordered_notes[clazz] = [abs(10 * (noteh - note) / max(1, note))
                                    for (noteh, _), (note, _) in zip(histo, histo[1:])]
            print(clazz, [name for _, name in histo], [note - minh for note, _ in histo], ordered_notes[clazz])
            ordered_cutter[clazz] = ordered_notes[clazz].index(max(ordered_notes[clazz]))

        ranker = {}
        for sample, clazz, _ in self.data:
            rank = [(histo.index(sample) if histo.index(sample) > ordered_cutter[clazz] else histo.index(sample) // 4,
                     clazz) for clazz, histo in ordered_histos.items()]
            rank.sort(reverse=True)
            ranker[sample] = [clazz, rank[0][1]]
            print(sample, rank)
        return ranker

    def classify_samples(self):
        bleach, retinasize, samples = self.bleach, self.retinasize, self.data
        # print("classify_samples", samples[0])
        cortices = [(cortex.clazz, cortex.bleacher, cortex.cortex) for cortex in self.cortex]
        return [
            (name, sample_clazz,
             {clazz: sum(
                 neuron[(retina[neuron[(0, LGN)]], retina[neuron[(1, LGN)]])]
                 for neuron in cortex) - retinasize * (bleach + bleacher)}
             ) for clazz, bleacher, cortex in cortices
            for name, sample_clazz, retina in samples]

    def run(self):
        self.reset_brain()
        self.learn_samples()  # [:8])
        # self.update_balance()
        res = self.classify_samples()
        return res

    def single(self, namer=-1, result=False):
        global RND
        histo_classes = {clazz: [] for clazz in self.clazzes}
        clazzes = self.clazzes + ["U"]
        tot = {u[0]: {key: 0 if key != "U" else str(u[0]) + " " + str(u[1]) for key in clazzes} for u in
               self.data}
        primes = PRIMES[:]
        for _ in range(1):
            # shuffle(data)
            RND = primes.pop()
            res = self.run()
            [histo_classes[cl].append((s, name)) for name, _, line in res for cl, s in line.items()]
            [tot[name].update({cl: tot[name][cl] + s for cl, s in line.items()}) for name, _, line in res]
        total = list(tot.keys())
        total.sort()
        total_conf = 0
        total_sec = 0
        for line in total:
            val = dict(tot[line])
            user = val.pop("U")[namer:] if "U" in val else ""
            val = list(val.items())
            # print(val)
            val.sort(key=operator.itemgetter(1), reverse=True)
            first, sec, third = val[0][1], val[1][1], val[2][1]
            confidence = min(100 * abs(first - sec) // max(abs(first), 1), 100)
            conf = confidence if (user == val[0][0][namer:]) or ("e" == user) else -2 * confidence
            secd = min(abs(sec // max(abs(first), 1)) * conf, 100)  # if (user == val[0][0]) or ("e" == user) else 0
            # conf = 100 * abs(first-sec) // max(abs(first), abs(sec))
            # conf = 100 * (max(first, 0)-max(sec, 0)) // first
            total_conf += conf
            total_sec += secd
            if result:
                print("{name: >42} {val} conf: {conf}".format(name=tot[line]["U"] if "U" in tot[line] else "",
                                                              val="".join(["%s:%8.0f " % (a[-3:], b) for a, b in val]),
                                                              conf=conf))
        print("total confidence %f" % (1.0 * total_conf / len(total)))
        if result:
            import sys
            sys.exit(0)
        if False:
            ordered_histos = {}
            ordered_notes = {}
            ordered_cutter = {}
            for clazz, histo in histo_classes.items():
                histo.sort()
                minh = histo[0][0]
                ordered_histos[clazz] = [name for _, name in histo]
                ordered_notes[clazz] = [abs(10 * (noteh - note) / note) for (noteh, _), (note, _)
                                        in zip(histo, histo[1:])]
                print(clazz, [name for _, name in histo], [note - minh for note, _ in histo], ordered_notes[clazz])
                ordered_cutter[clazz] = ordered_notes[clazz].index(max(ordered_notes[clazz]))

            for sample in range(148):
                rank = [(histo.index(sample) if histo.index(sample) > ordered_cutter[clazz]
                         else histo.index(sample) // 4, clazz) for clazz, histo in ordered_histos.items()]
                rank.sort(reverse=True)
                print(sample, rank)
            return
        return 1.0 * total_conf / len(total)

    def main(self, namer=-1):
        global RND
        histo_classes = {clazz: [] for clazz in self.clazzes}
        clazzes = self.clazzes + ["U"]
        tot = {u[0]: {key: 0 if key != "U" else str(u[0]) + " " + str(u[1]) for key in clazzes} for u in
               self.data}
        primes = PRIMES[:]
        for _ in range(1):
            # shuffle(data)
            RND = primes.pop()
            res = self.run()
            [histo_classes[cl].append((s, name)) for name, _, line in res for cl, s in line.items()]
            [tot[name].update({cl: tot[name][cl] + s for cl, s in line.items()}) for name, _, line in res]
        total = list(tot.keys())
        total.sort()
        total_conf = 0
        total_sec = 0
        for line in total:
            val = dict(tot[line])
            user = val.pop("U")[namer:] if "U" in val else ""
            val = list(val.items())
            # print(val)
            val.sort(key=operator.itemgetter(1), reverse=True)
            first, sec, third = val[0][1], val[1][1], val[2][1]
            confidence = min(100 * abs(first - sec) // max(abs(first), 1), 100)
            conf = confidence if (user == val[0][0][namer:]) or ("e" == user) else -2 * confidence
            secd = min(abs(sec // max(abs(first), 1)) * conf, 100)  # if (user == val[0][0]) or ("e" == user) else 0
            # conf = 100 * abs(first-sec) // max(abs(first), abs(sec))
            # conf = 100 * (max(first, 0)-max(sec, 0)) // first
            total_conf += conf
            total_sec += secd

            # print(tot[line]["U"] + "  " + "".join(["%s:%8.0f " % (a[-3:], b) for a, b in val]), "conf: %d" % conf)
            print("{name: >52} {val} conf: {conf}".format(name=tot[line]["U"] if "U" in tot[line] else "",
                                                          val="".join(["%s:%8.0f " % (a[-3:], b) for a, b in val]),
                                                          conf=conf))
        print("total confidence %f" % (1.0 * total_conf / len(total)))
        if False:
            ordered_histos = {}
            ordered_notes = {}
            ordered_cutter = {}
            for clazz, histo in histo_classes.items():
                histo.sort()
                minh = histo[0][0]
                ordered_histos[clazz] = [name for _, name in histo]
                ordered_notes[clazz] = [abs(10 * (noteh - note) / note) for (noteh, _), (note, _)
                                        in zip(histo, histo[1:])]
                print(clazz, [name for _, name in histo], [note - minh for note, _ in histo], ordered_notes[clazz])
                ordered_cutter[clazz] = ordered_notes[clazz].index(max(ordered_notes[clazz]))

            for sample in range(148):
                rank = [(histo.index(sample) if histo.index(sample) > ordered_cutter[clazz]
                         else histo.index(sample) // 4, clazz) for clazz, histo in ordered_histos.items()]
                rank.sort(reverse=True)
                print(sample, rank)
            return
        return 1.0 * total_conf / len(total)

    def _single(self, namer=-1):
        res = self.run()
        clazzes = self.clazzes + ["U"]
        tot = {u[0]: {key: 0 if key != "U" else str(u[0]) + " " + str(u[1]) for key in clazzes} for u in
               self.data}
        [tot[name].update({cl: tot[name][cl] + s for cl, s in line.items()}) for name, _, line in res]
        total = list(tot.keys())
        total.sort()
        total_conf = 0
        total_sec = 0
        for line in total:
            val = dict(tot[line])
            user = val.pop("U")[namer:] if "U" in val else ""
            val = list(val.items())
            # print(val)
            val.sort(key=operator.itemgetter(1), reverse=True)
            first, sec, third = val[0][1], val[1][1], val[2][1]
            confidence = min(100 * abs(first - sec) // max(abs(first), 1), 100)
            conf = confidence if (user == val[0][0][namer:]) or ("e" == user) else -2 * confidence
            secd = min(abs(sec // max(abs(first), 1)) * conf, 100)  # if (user == val[0][0]) or ("e" == user) else 0
            # conf = 100 * abs(first-sec) // max(abs(first), abs(sec))
            # conf = 100 * (max(first, 0)-max(sec, 0)) // first
            total_conf += conf
            total_sec += secd
        return 1.0 * total_conf / len(total)

    def unsupervised_class(self, _=-1):
        self.reset_brain()
        self.learn_samples()
        self.rank_samples()

    def retinify_samples(self, samples):
        [self.retinify(sample[2:]) for sample in samples]

    @staticmethod
    def retinify(retina, threshold=32, band=8, zoom=4, retinasize=128):
        def retinate(value, pix=0, bnd=0):
            return [pix] * int(bnd + (1 - pix) * float(value) * zoom // ZFATOR)

        def deretinate(value, pix=0):
            return [pix] * (TOP - (band + int(float(value) * zoom // ZFATOR)))

        # print(retina, [(int(float(ZO * v) // ZFATOR), (TOP - (2 * int(float(ZO * v) // ZFATOR)))) for v in retina])
        retina += [0]*retinasize
        retina = [
            (retinate(value) + retinate(value, 1, band) + deretinate(value))[:threshold]
            for value in retina]
        return [pix for line in retina for pix in line]

    @staticmethod
    def sense_domain(data):
        def updater(neuron, index, off):
            return {index: neuron[index] + off}

        data = [[float(p) for p in line.split(",")[:-1]] for i, line in enumerate(data)]

        retina = Wisard.retinify(data[0])
        lobe = [{(a, b): 0 for a in [0, 1] for b in [0, 1]} for _ in range(len(retina) // 2)]
        master_retina = [0 for _ in range(len(retina))]
        for sample in data:
            retina = Wisard.retinify(sample)
            [master_retina.__setitem__(pix, master_retina[pix] + retina[pix]) for pix in range(len(master_retina))]
            [neuron.update(
                updater(neuron, (retina.pop(RND % len(retina)), retina.pop(RND % len(retina))), 1))
             for neuron in lobe]
        domain = list(set(master_retina[:]))
        domain.sort()
        domain = [(tre, sum(1 for pix in master_retina if tre == pix)) for tre in domain]
        print(domain, len(master_retina), len(data), len(data[0]), sum(dm[1] for dm in domain[1:-1]))
        domain = list(set([val for neuron in lobe for val in neuron.values()]))
        domain.sort()
        domain = [(tre, sum(1 for neuron in lobe for val in neuron.values() if tre == val)) for tre in domain]
        print(domain, len(lobe), sum(dm[1] for dm in domain[1:-1])), sum(dm[0] for dm in domain[1:-1])
        return Wisard.split_classes(domain, lobe, master_retina)

    @staticmethod
    def split_classes(domain, lobe, master_retina):
        cutter = sum(dm[0] * dm[1] for dm in domain[1:-1]) // 2
        lower_half = []
        higher_half = []
        wheighted_sum = 0
        for wheight, count in domain[1:-1]:
            if wheighted_sum > cutter:
                break
            wheighted_sum += wheight * count
            [lower_half.append(neuron) if wheighted_sum < cutter else higher_half.append(neuron) for neuron in lobe
             if any(neuron[(a, b)] == wheight for a in [0, 1] for b in [0, 1])]
        print(cutter, len(lower_half), len(higher_half), wheighted_sum)

        show([1 if pix else 0 for pix in master_retina])
        return {"l": lower_half, "h": higher_half}

    def unsupervised_learn(self, data):
        clazzes = self.sense_domain(data)
        self.cortex = clazzes
        self.bleacher = {key: 0 for key in clazzes.keys()}
        [[i, line.split(",")[-1]] + [float(p) for p in line.split(",")[:-1]] for i, line in enumerate(data)]
        result = self.classify_samples()
        for line in result:
            print(line)
        print("##################################################################")
        data = [dt for dt, rs in zip(data, result) if rs[2]["h"] == 253]
        clazzes = self.sense_domain(data)
        self.cortex = clazzes
        self.bleacher = {key: 0 for key in clazzes.keys()}
        [[i, line.split(",")[-1]] + [float(p) for p in line.split(",")[:-1]] for i, line in enumerate(data)]
        result = self.classify_samples()
        for line in result:
            print(line)


def show(retina):
    for i in range(32):
        print("".join([str(retina[j + 32 * i]) for j in range(32)]))
    return


def plot(data):
    import matplotlib.pyplot as plt
    from math import pi

    step = 2 * pi / 125
    theta = [ang * step for ang in range(125)]

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


def gmain(ch="216501166744497073410"):
    from learn import Learn
    endtime = 128
    data = Learn().build_with_User_table_for_prog(slicer=endtime)
    print(len(data[0]))
    data = [(line[0], line[1],
             Wisard.retinify([float(t) - float(t0) + 10 for t, t0 in zip(line[3:endtime], line[2:endtime])]))
            for line in data]
    print("Tabela gerada por rede neural sem peso para derivada segunda do tempo com prognóstico da carla")
    # bleacher = dict(V=805, S=-6, E=81, F=154)
    # bleacher = dict(V=1485, S=-359, E=34, F=139) 199321270259550360019
    v, s, f, e, b, a, d =\
        int(ch[:4]), int(ch[4:7]), int(ch[7:10]), int(ch[10:13]), int(ch[13:16]), int(ch[16:19]), int(ch[19:21])
    bleacher = dict(V=v, S=s, E=e, F=f)
    w = Wisard(data, 32 * endtime, bleach=b, mapper=bleacher, enf=a, sup=d)
    # bleacher = dict(V=893, S=-304, E=-48, F=25)
    # w = Wisard(data, 32 * endtime, bleach=995, mapper=bleacher, enf=452, sup=39, unsupervised=unsupervised)
    # bleacher = dict(V=603, S=0, E=81, F=154)
    # w = Wisard(data, 32 * endtime, bleach=600, mapper=bleacher, enf=110, sup=20)
    w.main()
    print(len(data[0][2:]))


def main(_=0, unsupervised=False):
    from learn import Learn
    endtime = 128
    data = Learn().build_with_User_table_for_prog(slicer=endtime)
    print(len(data[0]))
    data = [(line[0], line[1],
             Wisard.retinify([float(t) - float(t0) + 10 for t, t0 in zip(line[3:endtime], line[2:endtime])]))
            for line in data]
    print("Tabela gerada por rede neural sem peso para derivada segunda do tempo com prognóstico da carla")
    # bleacher = dict(V=805, S=-6, E=81, F=154)
    # 83.36 16.64 v:2165, s:11, f:667, e:422, b:970, a:734, d:10
    bleacher = dict(V=1602, S=-15, E=59, F=165)  # 199321270259550360019
    # bleacher = dict(V=1615, S=-15, E=42, F=169)  # 199321270259550360019
    # bleacher = dict(V=2531, S=169, E=634, F=856)
    # w = Wisard(data, 32 * endtime, bleach=913, mapper=bleacher, enf=609, sup=18, unsupervised=unsupervised)
    w = Wisard(data, 32 * endtime, bleach=913, mapper=bleacher, enf=609, sup=18, unsupervised=unsupervised)
    # bleacher = dict(V=893, S=-304, E=-48, F=25)
    # w = Wisard(data, 32 * endtime, bleach=995, mapper=bleacher, enf=452, sup=39, unsupervised=unsupervised)
    # bleacher = dict(V=603, S=0, E=81, F=154)
    # w = Wisard(data, 32 * endtime, bleach=600, mapper=bleacher, enf=110, sup=20)
    w.main()
    print(len(data[0][2:]))
    """
    clazz_names = "V:Verdadeiro Sucesso,S:Sucesso Mínimo,E:Expulsão Simbólica,F:Falso Sucesso"
    clazz_name = {key: name for key, name in (kv.split(":") for kv in clazz_names.split(","))}
    clazz_data = {clazz_name[name]: [(dat[2:] + ([0.0] * 120))[:125] for dat in data if dat[1] == name]
                  for name in clazz_name.keys()}
    plot_clazz = [(claz_name, clazz_data[claz_name]) for claz_name in clazz_data.keys()]
    plot(plot_clazz)
    # for dat in data:
    #     plot((dat[2:]+([0.0]*120))[:125])"""


if __name__ == '__main__':
    main()
    # main("116208942029867439738")
    # main(DATA, unsupervised=False)
    # Wisard.sense_domain(DATA)
    # Wisard().unsupervised_learn(DATA)
