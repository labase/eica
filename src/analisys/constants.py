PRIMES = [int(p) for p in """   6143   6151   6163   6173   6197   6199   6203   6211   6217   6221
   6229   6247   6257   6263   6269   6271   6277   6287   6299   6301
   6311   6317   6323   6329   6337   6343   6353   6359   6361   6367
   6373   6379   6389   6397   6421   6427   6449   6451   6469   6473
   6481   6491   6521   6529   6547   6551   6553   6563   6569   6571
   6577   6581   6599   6607   6619   6637   6653   6659   6661   6673
   6679   6689   6691   6701   6703   6709   6719   6733   6737   6761
   6763   6779   6781   6791   6793   6803   6823   6827   6829   6833
   6841   6857   6863   6869   6871   6883   6899   6907   6911   6917
   6947   6949   6959   6961   6967   6971   6977   6983   6991   6997
   7001   7013   7019   7027   7039   7043   7057   7069   7079   7103
   7109   7121   7127   7129   7151   7159   7177   7187   7193   7207
   7211   7213   7219   7229   7237   7243   7247   7253   7283   7297
   7307   7309   7321   7331   7333   7349   7351   7369   7393   7411
   7417   7433   7451   7457   7459   7477   7481   7487   7489   7499
   7507   7517   7523   7529   7537   7541   7547   7549   7559   7561
   7573   7577   7583   7589   7591   7603   7607   7621   7639   7643
   7649   7669   7673   7681   7687   7691   7699   7703   7717   7723
   7727   7741   7753   7757   7759   7789   7793   7817   7823   7829
   7841   7853   7867   7873   7877   7879   7883   7901   7907   7919
""".split()]

_COLORS = dict(
    aliceblue='#F0F8FF', antiquewhite='#FAEBD7', aqua='#00FFFF',
    aquamarine='#7FFFD4', azure='#F0FFFF', beige='#F5F5DC', bisque='#FFE4C4',
    black='#000000', blanchedalmond='#FFEBCD', blue='#0000FF', blueviolet='#8A2BE2',
    brown='#A52A2A', burlywood='#DEB887', cadetblue='#5F9EA0', chartreuse='#7FFF00',
    chocolate='#D2691E', coral='#FF7F50', cornflowerblue='#6495ED',
    cornsilk='#FFF8DC', crimson='#DC143C', cyan='#00FFFF', darkblue='#00008B',
    darkcyan='#008B8B', darkgoldenrod='#B8860B', darkgray='#A9A9A9',
    darkgreen='#006400', darkgrey='#A9A9A9', darkkhaki='#BDB76B',
    darkmagenta='#8B008B', darkolivegreen='#556B2F', darkorange='#FF8C00',
    darkorchid='#9932CC', darkred='#8B0000', darksalmon='#E9967A',
    darkseagreen='#8FBC8F', darkslateblue='#483D8B', darkslategray='#2F4F4F',
    darkslategrey='#2F4F4F', darkturquoise='#00CED1', darkviolet='#9400D3',
    deeppink='#FF1493', deepskyblue='#00BFFF', dimgray='#696969', dimgrey='#696969',
    dodgerblue='#1E90FF', firebrick='#B22222', floralwhite='#FFFAF0',
    forestgreen='#228B22', fuchsia='#FF00FF', gainsboro='#DCDCDC',
    ghostwhite='#F8F8FF', gold='#FFD700', goldenrod='#DAA520', gray='#808080',
    grey='#808080', green='#008000', greenyellow='#ADFF2F', honeydew='#F0FFF0',
    hotpink='#FF69B4', indianred='#CD5C5C', indigo='#4B0082', ivory='#FFFFF0',
    khaki='#F0E68C', lavender='#E6E6FA', lavenderblush='#FFF0F5',
    lawngreen='#7CFC00', lemonchiffon='#FFFACD', lightblue='#ADD8E6',
    lightcoral='#F08080', lightcyan='#E0FFFF', lightgoldenrodyellow='#FAFAD2',
    lightgray='#D3D3D3', lightgreen='#90EE90', lightgrey='#D3D3D3',
    lightpink='#FFB6C1', lightsalmon='#FFA07A', lightseagreen='#20B2AA',
    lightskyblue='#87CEFA', lightslategray='#778899', lightslategrey='#778899',
    lightsteelblue='#B0C4DE', lightyellow='#FFFFE0', lime='#00FF00',
    limegreen='#32CD32', linen='#FAF0E6', magenta='#FF00FF', maroon='#800000',
    mediumaquamarine='#66CDAA', mediumblue='#0000CD', mediumorchid='#BA55D3',
    mediumpurple='#9370DB', mediumseagreen='#3CB371', mediumslateblue='#7B68EE',
    mediumspringgreen='#00FA9A', mediumturquoise='#48D1CC',
    mediumvioletred='#C71585', midnightblue='#191970', mintcream='#F5FFFA',
    mistyrose='#FFE4E1', moccasin='#FFE4B5', navajowhite='#FFDEAD', navy='#000080',
    oldlace='#FDF5E6', olive='#808000', olivedrab='#6B8E23', orange='#FFA500',
    orangered='#FF4500', orchid='#DA70D6', palegoldenrod='#EEE8AA',
    palegreen='#98FB98', paleturquoise='#AFEEEE', palevioletred='#DB7093',
    papayawhip='#FFEFD5', peachpuff='#FFDAB9', peru='#CD853F', pink='#FFC0CB',
    plum='#DDA0DD', powderblue='#B0E0E6', purple='#800080', red='#FF0000',
    rosybrown='#BC8F8F', royalblue='#4169E1', saddlebrown='#8B4513',
    salmon='#FA8072', sandybrown='#F4A460', seagreen='#2E8B57', seashell='#FFF5EE',
    sienna='#A0522D', silver='#C0C0C0', skyblue='#87CEEB', slateblue='#6A5ACD',
    slategray='#708090', slategrey='#708090', snow='#FFFAFA', springgreen='#00FF7F',
    steelblue='#4682B4', tan='#D2B48C', teal='#008080', thistle='#D8BFD8',
    tomato='#FF6347', turquoise='#40E0D0', violet='#EE82EE', wheat='#F5DEB3',
    white='#FFFFFF', whitesmoke='#F5F5F5', yellow='#FFFF00', yellowgreen='#9ACD32',
    __getitem__= staticmethod(lambda color:getattr(
        COLOR, color and ''.join(color.split()).lower(), '#000000'))
)
COLOR = type('_Color_',(object,),_COLORS)()

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
