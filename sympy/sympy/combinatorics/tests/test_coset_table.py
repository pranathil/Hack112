# -*- coding: utf-8 -*-
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.coset_table import (CosetTable,
                    coset_enumeration_r, coset_enumeration_c)
from sympy.combinatorics.free_groups import free_group

"""
References
==========

[1] Holt, D., Eick, B., O'Brien, E.
"Handbook of Computational Group Theory"

[2] John J. Cannon; Lucien A. Dimino; George Havas; Jane M. Watson
Mathematics of Computation, Vol. 27, No. 123. (Jul., 1973), pp. 463-490.
"Implementation and Analysis of the Todd-Coxeter Algorithm"

"""

def test_scan_1():
    # Example 5.1 from [1]
    F, x, y = free_group("x, y")
    f = FpGroup(F, [x**3, y**3, x**-1*y**-1*x*y])
    c = CosetTable(f, [x])

    c.scan_and_fill(0, x)
    assert c.table == [[0, 0, None, None]]
    assert c.p == [0]
    assert c.n == 1
    assert c.omega == [0]

    c.scan_and_fill(0, x**3)
    assert c.table == [[0, 0, None, None]]
    assert c.p == [0]
    assert c.n == 1
    assert c.omega == [0]

    c.scan_and_fill(0, y**3)
    assert c.table == [[0, 0, 1, 2], [None, None, 2, 0], [None, None, 0, 1]]
    assert c.p == [0, 1, 2]
    assert c.n == 3
    assert c.omega == [0, 1, 2]

    c.scan_and_fill(0, x**-1*y**-1*x*y)
    assert c.table == [[0, 0, 1, 2], [None, None, 2, 0], [2, 2, 0, 1]]
    assert c.p == [0, 1, 2]
    assert c.n == 3
    assert c.omega == [0, 1, 2]

    c.scan_and_fill(1, x**3)
    assert c.table == [[0, 0, 1, 2], [3, 4, 2, 0], [2, 2, 0, 1], \
            [4, 1, None, None], [1, 3, None, None]]
    assert c.p == [0, 1, 2, 3, 4]
    assert c.n == 5
    assert c.omega == [0, 1, 2, 3, 4]

    c.scan_and_fill(1, y**3)
    assert c.table == [[0, 0, 1, 2], [3, 4, 2, 0], [2, 2, 0, 1], \
            [4, 1, None, None], [1, 3, None, None]]
    assert c.p == [0, 1, 2, 3, 4]
    assert c.n == 5
    assert c.omega == [0, 1, 2, 3, 4]

    c.scan_and_fill(1, x**-1*y**-1*x*y)
    assert c.table == [[0, 0, 1, 2], [1, 1, 2, 0], [2, 2, 0, 1], \
            [None, 1, None, None], [1, 3, None, None]]
    assert c.p == [0, 1, 2, 1, 1]
    assert c.n == 3
    assert c.omega == [0, 1, 2]

    # Example 5.2 from [1]
    f = FpGroup(F, [x**2, y**3, (x*y)**3])
    c = CosetTable(f, [x*y])

    c.scan_and_fill(0, x*y)
    assert c.table == [[1, None, None, 1], [None, 0, 0, None]]
    assert c.p == [0, 1]
    assert c.n == 2
    assert c.omega == [0, 1]

    c.scan_and_fill(0, x**2)
    assert c.table == [[1, 1, None, 1], [0, 0, 0, None]]
    assert c.p == [0, 1]
    assert c.n == 2
    assert c.omega == [0, 1]

    c.scan_and_fill(0, y**3)
    assert c.table == [[1, 1, 2, 1], [0, 0, 0, 2], [None, None, 1, 0]]
    assert c.p == [0, 1, 2]
    assert c.n == 3
    assert c.omega == [0, 1, 2]

    c.scan_and_fill(0, (x*y)**3)
    assert c.table == [[1, 1, 2, 1], [0, 0, 0, 2], [None, None, 1, 0]]
    assert c.p == [0, 1, 2]
    assert c.n == 3
    assert c.omega == [0, 1, 2]

    c.scan_and_fill(1, x**2)
    assert c.table == [[1, 1, 2, 1], [0, 0, 0, 2], [None, None, 1, 0]]
    assert c.p == [0, 1, 2]
    assert c.n == 3
    assert c.omega == [0, 1, 2]

    c.scan_and_fill(1, y**3)
    assert c.table == [[1, 1, 2, 1], [0, 0, 0, 2], [None, None, 1, 0]]
    assert c.p == [0, 1, 2]
    assert c.n == 3
    assert c.omega == [0, 1, 2]

    c.scan_and_fill(1, (x*y)**3)
    assert c.table == [[1, 1, 2, 1], [0, 0, 0, 2], [3, 4, 1, 0], [None, 2, 4, None], [2, None, None, 3]]
    assert c.p == [0, 1, 2, 3, 4]
    assert c.n == 5
    assert c.omega == [0, 1, 2, 3, 4]

    c.scan_and_fill(2, x**2)
    assert c.table == [[1, 1, 2, 1], [0, 0, 0, 2], [3, 3, 1, 0], [2, 2, 3, 3], [2, None, None, 3]]
    assert c.p == [0, 1, 2, 3, 3]
    assert c.n == 4
    assert c.omega == [0, 1, 2, 3]


def test_coset_enumeration():
    # this test function contains the combined tests for the two strategies
    # i.e. HLT and Felsch strategies.

    # Example 5.1 from [1]
    F, x, y = free_group("x, y")
    f = FpGroup(F, [x**3, y**3, x**-1*y**-1*x*y])
    C_r = coset_enumeration_r(f, [x])
    C_r.compress(); C_r.standardize()
    C_c = coset_enumeration_c(f, [x])
    C_c.compress(); C_c.standardize()
    table1 = [[0, 0, 1, 2], [1, 1, 2, 0], [2, 2, 0, 1]]
    assert C_r.table == table1
    assert C_c.table == table1

    # E₁ from [2] Pg. 474
    F, r, s, t = free_group("r, s, t")
    E1 = FpGroup(F, [t**-1*r*t*r**-2, r**-1*s*r*s**-2, s**-1*t*s*t**-2])
    C_r = coset_enumeration_r(E1, [])
    C_r.compress()
    C_c = coset_enumeration_c(E1, [])
    C_c.compress()
    table2 = [[0, 0, 0, 0, 0, 0]]
    assert C_r.table == table2
    # test for issue #11449
    assert C_c.table == table2

    # Cox group from [2] Pg. 474
    F, a, b = free_group("a, b")
    Cox = FpGroup(F, [a**6, b**6, (a*b)**2, (a**2*b**2)**2, (a**3*b**3)**5])
    C_r = coset_enumeration_r(Cox, [a])
    C_r.compress(); C_r.standardize()
    C_c = coset_enumeration_c(Cox, [a])
    C_c.compress(); C_c.standardize()
    table3 = [[0, 0, 1, 2],
             [2, 3, 4, 0],
             [5, 1, 0, 6],
             [1, 7, 8, 9],
             [9, 10, 11, 1],
             [12, 2, 9, 13],
             [14, 9, 2, 11],
             [3, 12, 15, 16],
             [16, 17, 18, 3],
             [6, 4, 3, 5],
             [4, 19, 20, 21],
             [21, 22, 6, 4],
             [7, 5, 23, 24],
             [25, 23, 5, 18],
             [19, 6, 22, 26],
             [24, 27, 28, 7],
             [29, 8, 7, 30],
             [8, 31, 32, 33],
             [33, 34, 13, 8],
             [10, 14, 35, 35],
             [35, 36, 37, 10],
             [30, 11, 10, 29],
             [11, 38, 39, 14],
             [13, 39, 38, 12],
             [40, 15, 12, 41],
             [42, 13, 34, 43],
             [44, 35, 14, 45],
             [15, 46, 47, 34],
             [34, 48, 49, 15],
             [50, 16, 21, 51],
             [52, 21, 16, 49],
             [17, 50, 53, 54],
             [54, 55, 56, 17],
             [41, 18, 17, 40],
             [18, 28, 27, 25],
             [26, 20, 19, 19],
             [20, 57, 58, 59],
             [59, 60, 51, 20],
             [22, 52, 61, 23],
             [23, 62, 63, 22],
             [64, 24, 33, 65],
             [48, 33, 24, 61],
             [62, 25, 54, 66],
             [67, 54, 25, 68],
             [57, 26, 59, 69],
             [70, 59, 26, 63],
             [27, 64, 71, 72],
             [72, 73, 68, 27],
             [28, 41, 74, 75],
             [75, 76, 30, 28],
             [31, 29, 77, 78],
             [79, 77, 29, 37],
             [38, 30, 76, 80],
             [78, 81, 82, 31],
             [43, 32, 31, 42],
             [32, 83, 84, 85],
             [85, 86, 65, 32],
             [36, 44, 87, 88],
             [88, 89, 90, 36],
             [45, 37, 36, 44],
             [37, 82, 81, 79],
             [80, 74, 41, 38],
             [39, 42, 91, 92],
             [92, 93, 45, 39],
             [46, 40, 94, 95],
             [96, 94, 40, 56],
             [97, 91, 42, 82],
             [83, 43, 98, 99],
             [100, 98, 43, 47],
             [101, 87, 44, 90],
             [82, 45, 93, 97],
             [95, 102, 103, 46],
             [104, 47, 46, 105],
             [47, 106, 107, 100],
             [61, 108, 109, 48],
             [105, 49, 48, 104],
             [49, 110, 111, 52],
             [51, 111, 110, 50],
             [112, 53, 50, 113],
             [114, 51, 60, 115],
             [116, 61, 52, 117],
             [53, 118, 119, 60],
             [60, 70, 66, 53],
             [55, 67, 120, 121],
             [121, 122, 123, 55],
             [113, 56, 55, 112],
             [56, 103, 102, 96],
             [69, 124, 125, 57],
             [115, 58, 57, 114],
             [58, 126, 127, 128],
             [128, 128, 69, 58],
             [66, 129, 130, 62],
             [117, 63, 62, 116],
             [63, 125, 124, 70],
             [65, 109, 108, 64],
             [131, 71, 64, 132],
             [133, 65, 86, 134],
             [135, 66, 70, 136],
             [68, 130, 129, 67],
             [137, 120, 67, 138],
             [132, 68, 73, 131],
             [139, 69, 128, 140],
             [71, 141, 142, 86],
             [86, 143, 144, 71],
             [145, 72, 75, 146],
             [147, 75, 72, 144],
             [73, 145, 148, 120],
             [120, 149, 150, 73],
             [74, 151, 152, 94],
             [94, 153, 146, 74],
             [76, 147, 154, 77],
             [77, 155, 156, 76],
             [157, 78, 85, 158],
             [143, 85, 78, 154],
             [155, 79, 88, 159],
             [160, 88, 79, 161],
             [151, 80, 92, 162],
             [163, 92, 80, 156],
             [81, 157, 164, 165],
             [165, 166, 161, 81],
             [99, 107, 106, 83],
             [134, 84, 83, 133],
             [84, 167, 168, 169],
             [169, 170, 158, 84],
             [87, 171, 172, 93],
             [93, 163, 159, 87],
             [89, 160, 173, 174],
             [174, 175, 176, 89],
             [90, 90, 89, 101],
             [91, 177, 178, 98],
             [98, 179, 162, 91],
             [180, 95, 100, 181],
             [179, 100, 95, 152],
             [153, 96, 121, 148],
             [182, 121, 96, 183],
             [177, 97, 165, 184],
             [185, 165, 97, 172],
             [186, 99, 169, 187],
             [188, 169, 99, 178],
             [171, 101, 174, 189],
             [190, 174, 101, 176],
             [102, 180, 191, 192],
             [192, 193, 183, 102],
             [103, 113, 194, 195],
             [195, 196, 105, 103],
             [106, 104, 197, 198],
             [199, 197, 104, 109],
             [110, 105, 196, 200],
             [198, 201, 133, 106],
             [107, 186, 202, 203],
             [203, 204, 181, 107],
             [108, 116, 205, 206],
             [206, 207, 132, 108],
             [109, 133, 201, 199],
             [200, 194, 113, 110],
             [111, 114, 208, 209],
             [209, 210, 117, 111],
             [118, 112, 211, 212],
             [213, 211, 112, 123],
             [214, 208, 114, 125],
             [126, 115, 215, 216],
             [217, 215, 115, 119],
             [218, 205, 116, 130],
             [125, 117, 210, 214],
             [212, 219, 220, 118],
             [136, 119, 118, 135],
             [119, 221, 222, 217],
             [122, 182, 223, 224],
             [224, 225, 226, 122],
             [138, 123, 122, 137],
             [123, 220, 219, 213],
             [124, 139, 227, 228],
             [228, 229, 136, 124],
             [216, 222, 221, 126],
             [140, 127, 126, 139],
             [127, 230, 231, 232],
             [232, 233, 140, 127],
             [129, 135, 234, 235],
             [235, 236, 138, 129],
             [130, 132, 207, 218],
             [141, 131, 237, 238],
             [239, 237, 131, 150],
             [167, 134, 240, 241],
             [242, 240, 134, 142],
             [243, 234, 135, 220],
             [221, 136, 229, 244],
             [149, 137, 245, 246],
             [247, 245, 137, 226],
             [220, 138, 236, 243],
             [244, 227, 139, 221],
             [230, 140, 233, 248],
             [238, 249, 250, 141],
             [251, 142, 141, 252],
             [142, 253, 254, 242],
             [154, 255, 256, 143],
             [252, 144, 143, 251],
             [144, 257, 258, 147],
             [146, 258, 257, 145],
             [259, 148, 145, 260],
             [261, 146, 153, 262],
             [263, 154, 147, 264],
             [148, 265, 266, 153],
             [246, 267, 268, 149],
             [260, 150, 149, 259],
             [150, 250, 249, 239],
             [162, 269, 270, 151],
             [262, 152, 151, 261],
             [152, 271, 272, 179],
             [159, 273, 274, 155],
             [264, 156, 155, 263],
             [156, 270, 269, 163],
             [158, 256, 255, 157],
             [275, 164, 157, 276],
             [277, 158, 170, 278],
             [279, 159, 163, 280],
             [161, 274, 273, 160],
             [281, 173, 160, 282],
             [276, 161, 166, 275],
             [283, 162, 179, 284],
             [164, 285, 286, 170],
             [170, 188, 184, 164],
             [166, 185, 189, 173],
             [173, 287, 288, 166],
             [241, 254, 253, 167],
             [278, 168, 167, 277],
             [168, 289, 290, 291],
             [291, 292, 187, 168],
             [189, 293, 294, 171],
             [280, 172, 171, 279],
             [172, 295, 296, 185],
             [175, 190, 297, 297],
             [297, 298, 299, 175],
             [282, 176, 175, 281],
             [176, 294, 293, 190],
             [184, 296, 295, 177],
             [284, 178, 177, 283],
             [178, 300, 301, 188],
             [181, 272, 271, 180],
             [302, 191, 180, 303],
             [304, 181, 204, 305],
             [183, 266, 265, 182],
             [306, 223, 182, 307],
             [303, 183, 193, 302],
             [308, 184, 188, 309],
             [310, 189, 185, 311],
             [187, 301, 300, 186],
             [305, 202, 186, 304],
             [312, 187, 292, 313],
             [314, 297, 190, 315],
             [191, 316, 317, 204],
             [204, 318, 319, 191],
             [320, 192, 195, 321],
             [322, 195, 192, 319],
             [193, 320, 323, 223],
             [223, 324, 325, 193],
             [194, 326, 327, 211],
             [211, 328, 321, 194],
             [196, 322, 329, 197],
             [197, 330, 331, 196],
             [332, 198, 203, 333],
             [318, 203, 198, 329],
             [330, 199, 206, 334],
             [335, 206, 199, 336],
             [326, 200, 209, 337],
             [338, 209, 200, 331],
             [201, 332, 339, 240],
             [240, 340, 336, 201],
             [202, 341, 342, 292],
             [292, 343, 333, 202],
             [205, 344, 345, 210],
             [210, 338, 334, 205],
             [207, 335, 346, 237],
             [237, 347, 348, 207],
             [208, 349, 350, 215],
             [215, 351, 337, 208],
             [352, 212, 217, 353],
             [351, 217, 212, 327],
             [328, 213, 224, 323],
             [354, 224, 213, 355],
             [349, 214, 228, 356],
             [357, 228, 214, 345],
             [358, 216, 232, 359],
             [360, 232, 216, 350],
             [344, 218, 235, 361],
             [362, 235, 218, 348],
             [219, 352, 363, 364],
             [364, 365, 355, 219],
             [222, 358, 366, 367],
             [367, 368, 353, 222],
             [225, 354, 369, 370],
             [370, 371, 372, 225],
             [307, 226, 225, 306],
             [226, 268, 267, 247],
             [227, 373, 374, 233],
             [233, 360, 356, 227],
             [229, 357, 361, 234],
             [234, 375, 376, 229],
             [248, 231, 230, 230],
             [231, 377, 378, 379],
             [379, 380, 359, 231],
             [236, 362, 381, 245],
             [245, 382, 383, 236],
             [384, 238, 242, 385],
             [340, 242, 238, 346],
             [347, 239, 246, 381],
             [386, 246, 239, 387],
             [388, 241, 291, 389],
             [343, 291, 241, 339],
             [375, 243, 364, 390],
             [391, 364, 243, 383],
             [373, 244, 367, 392],
             [393, 367, 244, 376],
             [382, 247, 370, 394],
             [395, 370, 247, 396],
             [377, 248, 379, 397],
             [398, 379, 248, 374],
             [249, 384, 399, 400],
             [400, 401, 387, 249],
             [250, 260, 402, 403],
             [403, 404, 252, 250],
             [253, 251, 405, 406],
             [407, 405, 251, 256],
             [257, 252, 404, 408],
             [406, 409, 277, 253],
             [254, 388, 410, 411],
             [411, 412, 385, 254],
             [255, 263, 413, 414],
             [414, 415, 276, 255],
             [256, 277, 409, 407],
             [408, 402, 260, 257],
             [258, 261, 416, 417],
             [417, 418, 264, 258],
             [265, 259, 419, 420],
             [421, 419, 259, 268],
             [422, 416, 261, 270],
             [271, 262, 423, 424],
             [425, 423, 262, 266],
             [426, 413, 263, 274],
             [270, 264, 418, 422],
             [420, 427, 307, 265],
             [266, 303, 428, 425],
             [267, 386, 429, 430],
             [430, 431, 396, 267],
             [268, 307, 427, 421],
             [269, 283, 432, 433],
             [433, 434, 280, 269],
             [424, 428, 303, 271],
             [272, 304, 435, 436],
             [436, 437, 284, 272],
             [273, 279, 438, 439],
             [439, 440, 282, 273],
             [274, 276, 415, 426],
             [285, 275, 441, 442],
             [443, 441, 275, 288],
             [289, 278, 444, 445],
             [446, 444, 278, 286],
             [447, 438, 279, 294],
             [295, 280, 434, 448],
             [287, 281, 449, 450],
             [451, 449, 281, 299],
             [294, 282, 440, 447],
             [448, 432, 283, 295],
             [300, 284, 437, 452],
             [442, 453, 454, 285],
             [309, 286, 285, 308],
             [286, 455, 456, 446],
             [450, 457, 458, 287],
             [311, 288, 287, 310],
             [288, 454, 453, 443],
             [445, 456, 455, 289],
             [313, 290, 289, 312],
             [290, 459, 460, 461],
             [461, 462, 389, 290],
             [293, 310, 463, 464],
             [464, 465, 315, 293],
             [296, 308, 466, 467],
             [467, 468, 311, 296],
             [298, 314, 469, 470],
             [470, 471, 472, 298],
             [315, 299, 298, 314],
             [299, 458, 457, 451],
             [452, 435, 304, 300],
             [301, 312, 473, 474],
             [474, 475, 309, 301],
             [316, 302, 476, 477],
             [478, 476, 302, 325],
             [341, 305, 479, 480],
             [481, 479, 305, 317],
             [324, 306, 482, 483],
             [484, 482, 306, 372],
             [485, 466, 308, 454],
             [455, 309, 475, 486],
             [487, 463, 310, 458],
             [454, 311, 468, 485],
             [486, 473, 312, 455],
             [459, 313, 488, 489],
             [490, 488, 313, 342],
             [491, 469, 314, 472],
             [458, 315, 465, 487],
             [477, 492, 485, 316],
             [463, 317, 316, 468],
             [317, 487, 493, 481],
             [329, 447, 464, 318],
             [468, 319, 318, 463],
             [319, 467, 448, 322],
             [321, 448, 467, 320],
             [475, 323, 320, 466],
             [432, 321, 328, 437],
             [438, 329, 322, 434],
             [323, 474, 452, 328],
             [483, 494, 486, 324],
             [466, 325, 324, 475],
             [325, 485, 492, 478],
             [337, 422, 433, 326],
             [437, 327, 326, 432],
             [327, 436, 424, 351],
             [334, 426, 439, 330],
             [434, 331, 330, 438],
             [331, 433, 422, 338],
             [333, 464, 447, 332],
             [449, 339, 332, 440],
             [465, 333, 343, 469],
             [413, 334, 338, 418],
             [336, 439, 426, 335],
             [441, 346, 335, 415],
             [440, 336, 340, 449],
             [416, 337, 351, 423],
             [339, 451, 470, 343],
             [346, 443, 450, 340],
             [480, 493, 487, 341],
             [469, 342, 341, 465],
             [342, 491, 495, 490],
             [361, 407, 414, 344],
             [418, 345, 344, 413],
             [345, 417, 408, 357],
             [381, 446, 442, 347],
             [415, 348, 347, 441],
             [348, 414, 407, 362],
             [356, 408, 417, 349],
             [423, 350, 349, 416],
             [350, 425, 420, 360],
             [353, 424, 436, 352],
             [479, 363, 352, 435],
             [428, 353, 368, 476],
             [355, 452, 474, 354],
             [488, 369, 354, 473],
             [435, 355, 365, 479],
             [402, 356, 360, 419],
             [405, 361, 357, 404],
             [359, 420, 425, 358],
             [476, 366, 358, 428],
             [427, 359, 380, 482],
             [444, 381, 362, 409],
             [363, 481, 477, 368],
             [368, 393, 390, 363],
             [365, 391, 394, 369],
             [369, 490, 480, 365],
             [366, 478, 483, 380],
             [380, 398, 392, 366],
             [371, 395, 496, 497],
             [497, 498, 489, 371],
             [473, 372, 371, 488],
             [372, 486, 494, 484],
             [392, 400, 403, 373],
             [419, 374, 373, 402],
             [374, 421, 430, 398],
             [390, 411, 406, 375],
             [404, 376, 375, 405],
             [376, 403, 400, 393],
             [397, 430, 421, 377],
             [482, 378, 377, 427],
             [378, 484, 497, 499],
             [499, 499, 397, 378],
             [394, 461, 445, 382],
             [409, 383, 382, 444],
             [383, 406, 411, 391],
             [385, 450, 443, 384],
             [492, 399, 384, 453],
             [457, 385, 412, 493],
             [387, 442, 446, 386],
             [494, 429, 386, 456],
             [453, 387, 401, 492],
             [389, 470, 451, 388],
             [493, 410, 388, 457],
             [471, 389, 462, 495],
             [412, 390, 393, 399],
             [462, 394, 391, 410],
             [401, 392, 398, 429],
             [396, 445, 461, 395],
             [498, 496, 395, 460],
             [456, 396, 431, 494],
             [431, 397, 499, 496],
             [399, 477, 481, 412],
             [429, 483, 478, 401],
             [410, 480, 490, 462],
             [496, 497, 484, 431],
             [489, 495, 491, 459],
             [495, 460, 459, 471],
             [460, 489, 498, 498],
             [472, 472, 471, 491]]

    C_r.table == table3
    C_c.table == table3

    # Group denoted by B₂,₄ from [2] Pg. 474
    F, a, b = free_group("a, b")
    B_2_4 = FpGroup(F, [a**4, b**4, (a*b)**4, (a**-1*b)**4, (a**2*b)**4, \
            (a*b**2)**4, (a**2*b**2)**4, (a**-1*b*a*b)**4, (a*b**-1*a*b)**4])
    C_r = coset_enumeration_r(B_2_4, [a])
    C_c = coset_enumeration_c(B_2_4, [a])
    index_r = 0
    for i in range(len(C_r.p)):
        if C_r.p[i] == i:
            index_r += 1
    assert index_r == 1024

    index_c = 0
    for i in range(len(C_c.p)):
        if C_c.p[i] == i:
            index_c += 1
    assert index_c == 1024

    # trivial Macdonald group G(2,2) from [2] Pg. 480
    M = FpGroup(F, [b**-1*a**-1*b*a*b**-1*a*b*a**-2, a**-1*b**-1*a*b*a**-1*b*a*b**-2])
    C_r = coset_enumeration_r(M, [a])
    C_r.compress(); C_r.standardize()
    C_c = coset_enumeration_c(M, [a])
    C_c.compress(); C_c.standardize()
    table4 = [[0, 0, 0, 0]]
    assert C_r.table == table4
    assert C_c.table == table4


def test_look_ahead():
    # Section 3.2 [Test Example] Example (d) from [2]
    F, a, b, c = free_group("a, b, c")
    f = FpGroup(F, [a**11, b**5, c**4, (a*c)**3, b**2*c**-1*b**-1*c, a**4*b**-1*a**-1*b])
    H = [c, b, c**2]
    table0 = [[1, 2, 0, 0, 0, 0],
              [3, 0, 4, 5, 6, 7],
              [0, 8, 9, 10, 11, 12],
              [5, 1, 10, 13, 14, 15],
              [16, 5, 16, 1, 17, 18],
              [4, 3, 1, 8, 19, 20],
              [12, 21, 22, 23, 24, 1],
              [25, 26, 27, 28, 1, 24],
              [2, 10, 5, 16, 22, 28],
              [10, 13, 13, 2, 29, 30]]
    CosetTable.max_stack_size = 10
    C_c = coset_enumeration_c(f, H)
    C_c.compress(); C_c.standardize()
    assert C_c.table[: 10] == table0
