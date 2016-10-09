import numpy as np
from bottle import template

LINE_WIDTH = 0.005 * 20
LINE_WIDTH_S = 0.0045 * 20
PI = np.pi

matrix = np.array(
    [[668, 582, 209, 110, 63, 34, 25, 21],
     [600, 432, 147, 101, 43, 20, 10, 16],
     [198, 148, 67, 27, 17, 8, 4, 6],
     [115, 106, 19, 19, 0, 6, 6, 2],
     [60, 43, 10, 10, 54, 2, 1, 3],
     [25, 23, 10, 7, 3, 3, 3, 0],
     [25, 13, 10, 0, 2, 0, 0, 0],
     [25, 15, 4, 1, 1, 0, 1, 0]
     ]
    , dtype=int)
matrix[0] = matrix[0] / 3.5
matrix[1] = matrix[1] // 3
matrix[2] = matrix[2] // 2
#
# matrix = np.array([[16, 3, 28, 0, 18],
#                    [18, 0, 12, 5, 29],
#                    [9, 11, 17, 27, 0],
#                    [19, 0, 31, 11, 12],
#                    [23, 17, 10, 0, 34]], dtype=int)


labels = ['Emma', 'Isabella', 'Ava', 'Olivia', 'Sophia', 'Isabella', 'Ava', 'Olivia']
# ideo_colors = ['tan', 'pink', 'orange', 'yellow', 'lightgreen', 'lightblue', 'cyan', 'purple']
ideo_colors = ['rgba(255, 100, 100, 0.75)',
               'rgba(253, 174, 97, 0.75)',
               'rgba(254, 254, 139, 0.75)',
               'rgba(97, 254, 139, 0.75)',
               'rgba(97, 183, 183, 0.75)',
               'rgba(97, 186, 254, 0.75)',
               'rgba(184, 97, 254, 0.75)',
               'rgba(254, 0, 184, 0.75)']  # brewer colors with alpha set on 0.75


def check_data(data_matrix):
    L, M = data_matrix.shape
    if L != M:
        raise ValueError('Data array must have (n,n) shape')
    return L


L = check_data(matrix)


def moduloAB(x, a, b):  # maps a real number onto the unit circle identified with
    # the interval [a,b), b-a=2*PI
    if a >= b:
        raise ValueError('Incorrect interval ends')
    y = (x - a) % (b - a)
    return y + b if y < 0 else y + a


def test_2PI(x):
    return 0 <= x < 2 * PI


row_sum = [np.sum(matrix[k, :]) for k in range(L)]

# set the gap between two consecutive ideograms
gap = 2 * PI * 0.0005 * 2
ideogram_length = 2 * PI * np.asarray(row_sum) / sum(row_sum) - gap * np.ones(L)


def get_ideogram_ends(ideogram_len, gap):
    ideo_ends = []
    left = 0
    for k in range(len(ideogram_len)):
        right = left + ideogram_len[k]
        ideo_ends.append([left, right])
        left = right + gap
    return ideo_ends


ideo_ends = get_ideogram_ends(ideogram_length, gap)
print(ideo_ends)


def make_ideogram_arc(R, phi, a=50):
    # R is the circle radius
    # phi is the list of ends angle coordinates of an arc
    # a is a parameter that controls the number of points to be evaluated on an arc
    if not test_2PI(phi[0]) or not test_2PI(phi[1]):
        phi = [moduloAB(t, 0, 2 * PI) for t in phi]
    length = (phi[1] - phi[0]) % 2 * PI
    nr = 5 if length <= PI / 4 else int(a * length / PI)

    if phi[0] < phi[1]:
        theta = np.linspace(phi[0], phi[1], nr)
    else:
        phi = [moduloAB(t, -PI, PI) for t in phi]
        theta = np.linspace(phi[0], phi[1], nr)
    return R * np.exp(1j * theta)


z = make_ideogram_arc(1.3, [11 * PI / 6, PI / 17])
print(z)


def map_data(data_matrix, row_value, ideogram_length):
    mapped = np.zeros(data_matrix.shape)
    for j in range(L):
        mapped[:, j] = ideogram_length * data_matrix[:, j] / row_value
    return mapped


mapped_data = map_data(matrix, row_sum, ideogram_length)
idx_sort = np.argsort(mapped_data, axis=1)


def make_ribbon_ends(mapped_data, ideo_ends, idx_sort):
    L = mapped_data.shape[0]
    ribbon_boundary = np.zeros((L, L + 1))
    for k in range(L):
        start = ideo_ends[k][0]
        ribbon_boundary[k][0] = start
        for j in range(1, L + 1):
            J = idx_sort[k][j - 1]
            ribbon_boundary[k][j] = start + mapped_data[k][J]
            start = ribbon_boundary[k][j]
    return [[(ribbon_boundary[k][j], ribbon_boundary[k][j + 1]) for j in range(L)] for k in range(L)]


ribbon_ends = make_ribbon_ends(mapped_data, ideo_ends, idx_sort)
print('ribbon ends starting from the ideogram[2]\n', ribbon_ends[2])


def control_pts(angle, radius):
    # angle is a  3-list containing angular coordinates of the control points b0, b1, b2
    # radius is the distance from b1 to the  origin O(0,0)

    if len(angle) != 3:
        raise InvalidInputError('angle must have len =3')
    b_cplx = np.array([np.exp(1j * angle[k]) for k in range(3)])
    b_cplx[1] *= radius
    return list(zip(b_cplx.real, b_cplx.imag))


def ctrl_rib_chords(l, r, radius):
    # this function returns a 2-list containing control poligons of the two quadratic Bezier
    # curves that are opposite sides in a ribbon
    # l (r) the list of angular variables of the ribbon arc ends defining
    # the ribbon starting (ending) arc
    # radius is a common parameter for both control polygons
    if len(l) != 2 or len(r) != 2:
        raise ValueError('the arc ends must be elements in a list of len 2')
    return [control_pts([l[j], (l[j] + r[j]) / 2, r[j]], radius) for j in range(2)]


ribbon_color = [L * [ideo_colors[k]] for k in range(L)]

ribbon_color[0][4] = ideo_colors[4]
ribbon_color[1][2] = ideo_colors[2]
ribbon_color[2][3] = ideo_colors[3]
ribbon_color[2][4] = ideo_colors[4]


def make_q_bezier(b):  # defines the Plotly SVG path for a quadratic Bezier curve defined by the
    # list of its control points
    # if len(b) != 3:
    #     raise valueError('control poligon must have 3 points')
    A, B, C = b
    return 'M ' + str(A[0]) + ' ' + str(A[1]) + ' ' + 'Q ' + \
           str(B[0]) + ' ' + str(B[1]) + ' ' + \
           str(C[0]) + ' ' + str(C[1])


b = [(1, 4), (-0.5, 2.35), (3.745, 1.47)]

make_q_bezier(b)


def make_ribbon_arc(theta0, theta1):
    if test_2PI(theta0) and test_2PI(theta1):
        if theta0 < theta1:
            theta0 = moduloAB(theta0, -PI, PI)
            theta1 = moduloAB(theta1, -PI, PI)
            if theta0 * theta1 > 0:
                raise ValueError('incorrect angle coordinates for ribbon')

        nr = int(40 * (theta0 - theta1) / PI)
        if nr <= 2:
            nr = 3
        theta = np.linspace(theta0, theta1, nr)
        pts = np.exp(1j * theta)  # points on arc in polar complex form

        string_arc = ''
        for k in range(len(theta)):
            string_arc += ' L ' + str(pts.real[k]) + ' ' + str(pts.imag[k]) + ' '
        return string_arc
    else:
        raise ValueError('the angle coordinates for an arc side of a ribbon must be in [0, 2*pi]')


make_ribbon_arc(np.pi / 3, np.pi / 6)


def make_layout(title, plot_size):
    return
    # axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
    #             zeroline=False,
    #             showgrid=False,
    #             showticklabels=False,
    #             title=''
    #             )
    #
    # return Layout(title=title,
    #               xaxis=XAxis(axis),
    #               yaxis=YAxis(axis),
    #               showlegend=False,
    #               width=plot_size,
    #               height=plot_size,
    #               margin=Margin(t=25, b=25, l=25, r=25),
    #               hovermode='closest',
    #               shapes=[]  # to this list one appends below the dicts defining the ribbon,
    #               # respectively the ideogram shapes
    #               )


def make_ideo_shape(path, line_color, fill_color):
    # line_color is the color of the shape boundary
    # fill_collor is the color assigned to an ideogram
    return dict(
        line=dict(
            color=line_color,
            width=LINE_WIDTH_S
        ),

        path=path,
        type='path',
        fillcolor=fill_color,
    )


def make_ribbon(l, r, line_color, fill_color, radius=0.2):
    # l=[l[0], l[1]], r=[r[0], r[1]]  represent the opposite arcs in the ribbon
    # line_color is the color of the shape boundary
    # fill_color is the fill color for the ribbon shape
    poligon = ctrl_rib_chords(l, r, radius)
    b, c = poligon

    return dict(
        line=dict(
            color=line_color, width=LINE_WIDTH
        ),
        path=make_q_bezier(b) + make_ribbon_arc(r[0], r[1]) + make_q_bezier(c[::-1]) + make_ribbon_arc(l[1], l[0]),
        type='path',
        fillcolor=fill_color,
    )


def make_self_rel(l, line_color, fill_color, radius):
    # radius is the radius of Bezier control point b_1
    b = control_pts([l[0], (l[0] + l[1]) / 2, l[1]], radius)
    return dict(
        line=dict(
            color=line_color, width=LINE_WIDTH
        ),
        path=make_q_bezier(b) + make_ribbon_arc(l[1], l[0]),
        type='path',
        fillcolor=fill_color,
    )


def invPerm(perm):
    # function that returns the inverse of a permutation, perm
    inv = [0] * len(perm)
    for i, s in enumerate(perm):
        inv[s] = i
    return inv


layout = []

radii_sribb = [0.4, 0.40, 0.35, 0.39, 0.12, 0.30, 0.35, 0.39, 0.12]  # these value are set after a few trials

ribbon_info = []
for k in range(L):

    sigma = idx_sort[k]
    sigma_inv = invPerm(sigma)
    for j in range(k, L):
        if matrix[k][j] == 0 and matrix[j][k] == 0:
            continue
        eta = idx_sort[j]
        eta_inv = invPerm(eta)
        l = ribbon_ends[k][sigma_inv[j]]

        if j == k:
            layout.append(make_self_rel(l, 'rgb(175,175,175)',
                                        ideo_colors[k], radius=radii_sribb[k]))
            z = 0.9 * np.exp(1j * (l[0] + l[1]) / 2)
            # the text below will be displayed when hovering the mouse over the ribbon
            text = labels[k] + ' commented on ' + '{:d}'.format(matrix[k][k]) + ' of ' + 'herself Fb posts',
            # ribbon_info.append(Scatter(x=z.real,
            #                            y=z.imag,
            #                            mode='markers',
            #                            marker=Marker(size=0.5, color=ideo_colors[k]),
            #                            text=text,
            #                            hoverinfo='text'
            #                            )
            #                    )
        else:
            r = ribbon_ends[j][eta_inv[k]]
            zi = 0.9 * np.exp(1j * (l[0] + l[1]) / 2)
            zf = 0.9 * np.exp(1j * (r[0] + r[1]) / 2)
            # texti and textf are the strings that will be displayed when hovering the mouse
            # over the two ribbon ends
            texti = labels[k] + ' commented on ' + '{:d}'.format(matrix[k][j]) + ' of ' + \
                    labels[j] + ' Fb posts',

            textf = labels[j] + ' commented on ' + '{:d}'.format(matrix[j][k]) + ' of ' + \
                    labels[k] + ' Fb posts',
            # ribbon_info.append(Scatter(x=zi.real,
            #                            y=zi.imag,
            #                            mode='markers',
            #                            marker=Marker(size=0.5, color=ribbon_color[k][j]),
            #                            text=texti,
            #                            hoverinfo='text'
            #                            )
            #                    ),
            # ribbon_info.append(Scatter(x=zf.real,
            #                            y=zf.imag,
            #                            mode='markers',
            #                            marker=Marker(size=0.5, color=ribbon_color[k][j]),
            #                            text=textf,
            #                            hoverinfo='text'
            #                            )
            #                    )
            r = (r[1], r[0])  # IMPORTANT!!!  Reverse these arc ends because otherwise you get
            # a twisted ribbon
            # append the ribbon shape
            layout.append(make_ribbon(l, r, 'rgb(175,175,175)', ribbon_color[k][j]))

ideograms = []
for k in range(len(ideo_ends)):
    z = make_ideogram_arc(1.1, ideo_ends[k])
    zi = make_ideogram_arc(1.0, ideo_ends[k])
    m = len(z)
    n = len(zi)
    # ideograms.append(Scatter(x=z.real,
    #                          y=z.imag,
    #                          mode='lines',
    #                          line=Line(color=ideo_colors[k], shape='spline', width=0.25),
    #                          text=labels[k] + '<br>' + '{:d}'.format(row_sum[k]),
    #                          hoverinfo='text'
    #                          )
    #                  )

    path = 'M '
    for s in range(m):
        path += str(z.real[s]) + ' ' + str(z.imag[s]) + ' L '

    Zi = np.array(zi.tolist()[::-1])

    for s in range(m):
        path += str(Zi.real[s]) + ' ' + str(Zi.imag[s]) + ' L '
    path += str(z.real[0]) + ' ' + str(z.imag[0])

    layout.append(make_ideo_shape(path, 'rgb(150,150,150)', ideo_colors[k]))

data = (ideograms + ribbon_info)

# print(layout)
for d in layout:
    print(list(d.keys()))

SVG = '''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="25cm" height="26cm" viewBox="-120 -120 240 255"
     xmlns="http://www.w3.org/2000/svg" version="1.1">
  <title>Ideograma de transição de estados EICA</title>
  <desc>Ideograma de transição de estados EICA</desc>
<g
     id="layer1">
    % for sid, shape in enumerate(layout):
        <path id="line{{sid}}" d="{{shape["path"]}}" stroke="{{shape["line"]["color"]}}"
        stroke-width="{{shape["line"]["width"]}}" fill="{{shape["fillcolor"]}}" />
    % end
    % for sid, label in enumerate(labels):
        <rect id="cue{{sid}}" x="{{sid*26 - 105}}" y="120" width="10" height="10"
        stroke-width="{{label["width"]*4}}" fill="{{label["fillcolor"]}}" />
        <text id="cue{{sid}}"  x="{{sid*26+10 - 105}}" y="126" font-size="4" fill="black">EICA{{sid}}</text>
    % end
  </g>
</svg> '''


# layout = [{'fillcolor': 0, 'line': 0, 'type': 0, 'path': 0}]


def scale(v):
    return " ".join(l if l.isalpha() else str(float(l) * 100) for l in v.split())


intlayout = [{k: v if k != "path" else scale(v) for k, v in shape.items()} for shape in layout]
templater = template(SVG, layout=intlayout, labels=[dict(width=LINE_WIDTH, fillcolor=color) for color in ideo_colors])
filename = "ideogram.svg"
with open(filename, 'w') as hfile:
    hfile.write(templater)

# fig = Figure(data=data, layout=layout)
#
# url = py.plot(fig, filename='chord-diagram-Fb')
