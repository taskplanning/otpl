# Generated from pddl22.g4 by ANTLR 4.10.1
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,78,966,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,
        2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,
        13,7,13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,
        19,2,20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,
        26,7,26,2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,
        32,2,33,7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,
        39,7,39,2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,
        45,2,46,7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,2,
        52,7,52,2,53,7,53,2,54,7,54,2,55,7,55,2,56,7,56,2,57,7,57,2,58,7,
        58,2,59,7,59,2,60,7,60,2,61,7,61,2,62,7,62,2,63,7,63,2,64,7,64,2,
        65,7,65,2,66,7,66,2,67,7,67,2,68,7,68,2,69,7,69,2,70,7,70,2,71,7,
        71,2,72,7,72,2,73,7,73,2,74,7,74,2,75,7,75,2,76,7,76,2,77,7,77,1,
        0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,
        4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,
        6,1,6,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,
        7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,
        8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,
        8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,10,1,
        10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,
        10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,
        11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,
        11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,12,1,
        12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,
        12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,13,1,
        13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,
        13,1,13,1,13,1,13,1,13,1,13,1,13,1,14,1,14,1,14,1,14,1,14,1,14,1,
        14,1,14,1,14,1,15,1,15,1,15,1,15,1,15,1,16,1,16,1,16,1,16,1,16,1,
        16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,
        17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,
        17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,18,1,18,1,18,1,
        18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,
        18,1,18,1,18,1,18,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,
        19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,20,1,20,1,
        20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,
        20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,21,1,21,1,21,1,21,1,
        21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,21,1,22,1,22,1,22,1,22,1,
        22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,23,1,23,1,23,1,23,1,
        23,1,23,1,23,1,23,1,24,1,24,1,25,1,25,1,25,1,25,1,25,1,25,1,25,1,
        25,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,
        27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,
        28,1,28,1,28,1,28,1,28,1,28,1,28,1,28,1,28,1,28,1,28,1,28,1,29,1,
        29,1,29,1,29,1,29,1,29,1,29,1,29,1,29,1,30,1,30,1,30,1,30,1,30,1,
        30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,31,1,31,1,31,1,31,1,
        31,1,31,1,31,1,31,1,31,1,31,1,31,1,31,1,31,1,31,1,32,1,32,1,32,1,
        32,1,32,1,32,1,32,1,32,1,33,1,33,1,33,1,34,1,34,1,34,1,34,1,34,1,
        35,1,35,1,35,1,35,1,36,1,36,1,36,1,36,1,36,1,37,1,37,1,37,1,37,1,
        37,1,37,1,37,1,38,1,38,1,38,1,38,1,38,1,38,1,38,1,38,1,39,1,39,1,
        39,1,39,1,39,1,39,1,39,1,39,1,40,1,40,1,41,1,41,1,42,1,42,1,42,1,
        43,1,43,1,43,1,44,1,44,1,45,1,45,1,46,1,46,1,47,1,47,1,47,1,47,1,
        47,1,47,1,48,1,48,1,48,1,48,1,48,1,48,1,48,1,49,1,49,1,49,1,49,1,
        49,1,49,1,49,1,49,1,49,1,50,1,50,1,50,1,50,1,50,1,50,1,50,1,50,1,
        50,1,50,1,50,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,52,1,
        52,1,52,1,52,1,52,1,52,1,52,1,52,1,52,1,53,1,53,1,53,1,53,1,53,1,
        53,1,53,1,53,1,53,1,53,1,53,1,53,1,53,1,53,1,53,1,53,1,53,1,53,1,
        54,1,54,1,54,1,54,1,54,1,54,1,54,1,54,1,54,1,54,1,55,1,55,1,55,1,
        55,1,55,1,55,1,55,1,55,1,55,1,55,1,55,1,56,1,56,1,56,1,56,1,56,1,
        56,1,56,1,56,1,56,1,56,1,57,1,57,1,58,1,58,1,58,1,58,1,59,1,59,1,
        59,1,60,1,60,1,60,1,60,1,60,1,60,1,60,1,60,1,60,1,60,1,61,1,61,1,
        61,1,61,1,61,1,61,1,61,1,61,1,62,1,62,1,62,1,62,1,62,1,62,1,62,1,
        62,1,62,1,63,1,63,1,63,1,63,1,63,1,63,1,63,1,63,1,63,1,63,1,64,1,
        64,1,64,1,64,1,64,1,64,1,64,1,65,1,65,1,65,1,65,1,65,1,65,1,65,1,
        66,1,66,1,66,1,66,1,66,1,66,1,66,1,66,1,66,1,67,1,67,1,67,1,67,1,
        67,1,67,1,67,1,67,1,67,1,68,1,68,1,68,1,68,1,68,1,68,1,68,1,68,1,
        68,1,69,1,69,1,69,1,69,1,69,1,69,1,69,1,69,1,69,1,69,1,69,1,70,1,
        70,1,70,1,70,3,70,871,8,70,1,71,1,71,1,71,1,71,3,71,877,8,71,1,72,
        1,72,1,72,1,72,1,72,1,72,1,72,1,72,1,72,1,72,1,72,1,72,1,72,1,72,
        1,72,1,72,3,72,895,8,72,1,73,1,73,1,73,1,73,1,73,1,73,1,73,1,73,
        3,73,905,8,73,1,73,4,73,908,8,73,11,73,12,73,909,1,73,1,73,1,73,
        1,73,1,73,1,73,3,73,918,8,73,1,74,1,74,5,74,922,8,74,10,74,12,74,
        925,9,74,1,75,3,75,928,8,75,1,75,4,75,931,8,75,11,75,12,75,932,1,
        75,3,75,936,8,75,1,75,4,75,939,8,75,11,75,12,75,940,1,75,1,75,4,
        75,945,8,75,11,75,12,75,946,3,75,949,8,75,1,76,1,76,5,76,953,8,76,
        10,76,12,76,956,9,76,1,76,1,76,1,77,4,77,961,8,77,11,77,12,77,962,
        1,77,1,77,0,0,78,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,
        11,23,12,25,13,27,14,29,15,31,16,33,17,35,18,37,19,39,20,41,21,43,
        22,45,23,47,24,49,25,51,26,53,27,55,28,57,29,59,30,61,31,63,32,65,
        33,67,34,69,35,71,36,73,37,75,38,77,39,79,40,81,41,83,42,85,43,87,
        44,89,45,91,46,93,47,95,48,97,49,99,50,101,51,103,52,105,53,107,
        54,109,55,111,56,113,57,115,58,117,59,119,60,121,61,123,62,125,63,
        127,64,129,65,131,66,133,67,135,68,137,69,139,70,141,71,143,72,145,
        73,147,74,149,75,151,76,153,77,155,78,1,0,4,2,0,65,90,97,122,5,0,
        45,45,48,57,65,90,95,95,97,122,2,0,10,10,13,13,3,0,9,10,13,13,32,
        32,983,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,
        0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,
        0,0,21,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,0,27,1,0,0,0,0,29,1,0,0,
        0,0,31,1,0,0,0,0,33,1,0,0,0,0,35,1,0,0,0,0,37,1,0,0,0,0,39,1,0,0,
        0,0,41,1,0,0,0,0,43,1,0,0,0,0,45,1,0,0,0,0,47,1,0,0,0,0,49,1,0,0,
        0,0,51,1,0,0,0,0,53,1,0,0,0,0,55,1,0,0,0,0,57,1,0,0,0,0,59,1,0,0,
        0,0,61,1,0,0,0,0,63,1,0,0,0,0,65,1,0,0,0,0,67,1,0,0,0,0,69,1,0,0,
        0,0,71,1,0,0,0,0,73,1,0,0,0,0,75,1,0,0,0,0,77,1,0,0,0,0,79,1,0,0,
        0,0,81,1,0,0,0,0,83,1,0,0,0,0,85,1,0,0,0,0,87,1,0,0,0,0,89,1,0,0,
        0,0,91,1,0,0,0,0,93,1,0,0,0,0,95,1,0,0,0,0,97,1,0,0,0,0,99,1,0,0,
        0,0,101,1,0,0,0,0,103,1,0,0,0,0,105,1,0,0,0,0,107,1,0,0,0,0,109,
        1,0,0,0,0,111,1,0,0,0,0,113,1,0,0,0,0,115,1,0,0,0,0,117,1,0,0,0,
        0,119,1,0,0,0,0,121,1,0,0,0,0,123,1,0,0,0,0,125,1,0,0,0,0,127,1,
        0,0,0,0,129,1,0,0,0,0,131,1,0,0,0,0,133,1,0,0,0,0,135,1,0,0,0,0,
        137,1,0,0,0,0,139,1,0,0,0,0,141,1,0,0,0,0,143,1,0,0,0,0,145,1,0,
        0,0,0,147,1,0,0,0,0,149,1,0,0,0,0,151,1,0,0,0,0,153,1,0,0,0,0,155,
        1,0,0,0,1,157,1,0,0,0,3,165,1,0,0,0,5,167,1,0,0,0,7,174,1,0,0,0,
        9,176,1,0,0,0,11,191,1,0,0,0,13,199,1,0,0,0,15,207,1,0,0,0,17,231,
        1,0,0,0,19,258,1,0,0,0,21,268,1,0,0,0,23,295,1,0,0,0,25,320,1,0,
        0,0,27,346,1,0,0,0,29,367,1,0,0,0,31,376,1,0,0,0,33,381,1,0,0,0,
        35,399,1,0,0,0,37,422,1,0,0,0,39,442,1,0,0,0,41,462,1,0,0,0,43,486,
        1,0,0,0,45,499,1,0,0,0,47,512,1,0,0,0,49,520,1,0,0,0,51,522,1,0,
        0,0,53,530,1,0,0,0,55,542,1,0,0,0,57,555,1,0,0,0,59,567,1,0,0,0,
        61,576,1,0,0,0,63,590,1,0,0,0,65,604,1,0,0,0,67,612,1,0,0,0,69,615,
        1,0,0,0,71,620,1,0,0,0,73,624,1,0,0,0,75,629,1,0,0,0,77,636,1,0,
        0,0,79,644,1,0,0,0,81,652,1,0,0,0,83,654,1,0,0,0,85,656,1,0,0,0,
        87,659,1,0,0,0,89,662,1,0,0,0,91,664,1,0,0,0,93,666,1,0,0,0,95,668,
        1,0,0,0,97,674,1,0,0,0,99,681,1,0,0,0,101,690,1,0,0,0,103,701,1,
        0,0,0,105,710,1,0,0,0,107,719,1,0,0,0,109,737,1,0,0,0,111,747,1,
        0,0,0,113,758,1,0,0,0,115,768,1,0,0,0,117,770,1,0,0,0,119,774,1,
        0,0,0,121,777,1,0,0,0,123,787,1,0,0,0,125,795,1,0,0,0,127,804,1,
        0,0,0,129,814,1,0,0,0,131,821,1,0,0,0,133,828,1,0,0,0,135,837,1,
        0,0,0,137,846,1,0,0,0,139,855,1,0,0,0,141,866,1,0,0,0,143,876,1,
        0,0,0,145,894,1,0,0,0,147,904,1,0,0,0,149,919,1,0,0,0,151,948,1,
        0,0,0,153,950,1,0,0,0,155,960,1,0,0,0,157,158,5,40,0,0,158,159,5,
        100,0,0,159,160,5,101,0,0,160,161,5,102,0,0,161,162,5,105,0,0,162,
        163,5,110,0,0,163,164,5,101,0,0,164,2,1,0,0,0,165,166,5,40,0,0,166,
        4,1,0,0,0,167,168,5,100,0,0,168,169,5,111,0,0,169,170,5,109,0,0,
        170,171,5,97,0,0,171,172,5,105,0,0,172,173,5,110,0,0,173,6,1,0,0,
        0,174,175,5,41,0,0,175,8,1,0,0,0,176,177,5,40,0,0,177,178,5,58,0,
        0,178,179,5,114,0,0,179,180,5,101,0,0,180,181,5,113,0,0,181,182,
        5,117,0,0,182,183,5,105,0,0,183,184,5,114,0,0,184,185,5,101,0,0,
        185,186,5,109,0,0,186,187,5,101,0,0,187,188,5,110,0,0,188,189,5,
        116,0,0,189,190,5,115,0,0,190,10,1,0,0,0,191,192,5,58,0,0,192,193,
        5,115,0,0,193,194,5,116,0,0,194,195,5,114,0,0,195,196,5,105,0,0,
        196,197,5,112,0,0,197,198,5,115,0,0,198,12,1,0,0,0,199,200,5,58,
        0,0,200,201,5,116,0,0,201,202,5,121,0,0,202,203,5,112,0,0,203,204,
        5,105,0,0,204,205,5,110,0,0,205,206,5,103,0,0,206,14,1,0,0,0,207,
        208,5,58,0,0,208,209,5,110,0,0,209,210,5,101,0,0,210,211,5,103,0,
        0,211,212,5,97,0,0,212,213,5,116,0,0,213,214,5,105,0,0,214,215,5,
        118,0,0,215,216,5,101,0,0,216,217,5,45,0,0,217,218,5,112,0,0,218,
        219,5,114,0,0,219,220,5,101,0,0,220,221,5,99,0,0,221,222,5,111,0,
        0,222,223,5,110,0,0,223,224,5,100,0,0,224,225,5,105,0,0,225,226,
        5,116,0,0,226,227,5,105,0,0,227,228,5,111,0,0,228,229,5,110,0,0,
        229,230,5,115,0,0,230,16,1,0,0,0,231,232,5,58,0,0,232,233,5,100,
        0,0,233,234,5,105,0,0,234,235,5,115,0,0,235,236,5,106,0,0,236,237,
        5,117,0,0,237,238,5,110,0,0,238,239,5,99,0,0,239,240,5,116,0,0,240,
        241,5,105,0,0,241,242,5,118,0,0,242,243,5,101,0,0,243,244,5,45,0,
        0,244,245,5,112,0,0,245,246,5,114,0,0,246,247,5,101,0,0,247,248,
        5,99,0,0,248,249,5,111,0,0,249,250,5,110,0,0,250,251,5,100,0,0,251,
        252,5,105,0,0,252,253,5,116,0,0,253,254,5,105,0,0,254,255,5,111,
        0,0,255,256,5,110,0,0,256,257,5,115,0,0,257,18,1,0,0,0,258,259,5,
        58,0,0,259,260,5,101,0,0,260,261,5,113,0,0,261,262,5,117,0,0,262,
        263,5,97,0,0,263,264,5,108,0,0,264,265,5,105,0,0,265,266,5,116,0,
        0,266,267,5,121,0,0,267,20,1,0,0,0,268,269,5,58,0,0,269,270,5,101,
        0,0,270,271,5,120,0,0,271,272,5,105,0,0,272,273,5,115,0,0,273,274,
        5,116,0,0,274,275,5,101,0,0,275,276,5,110,0,0,276,277,5,116,0,0,
        277,278,5,105,0,0,278,279,5,97,0,0,279,280,5,108,0,0,280,281,5,45,
        0,0,281,282,5,112,0,0,282,283,5,114,0,0,283,284,5,101,0,0,284,285,
        5,99,0,0,285,286,5,111,0,0,286,287,5,110,0,0,287,288,5,100,0,0,288,
        289,5,105,0,0,289,290,5,116,0,0,290,291,5,105,0,0,291,292,5,111,
        0,0,292,293,5,110,0,0,293,294,5,115,0,0,294,22,1,0,0,0,295,296,5,
        58,0,0,296,297,5,117,0,0,297,298,5,110,0,0,298,299,5,105,0,0,299,
        300,5,118,0,0,300,301,5,101,0,0,301,302,5,114,0,0,302,303,5,115,
        0,0,303,304,5,97,0,0,304,305,5,108,0,0,305,306,5,45,0,0,306,307,
        5,112,0,0,307,308,5,114,0,0,308,309,5,101,0,0,309,310,5,99,0,0,310,
        311,5,111,0,0,311,312,5,110,0,0,312,313,5,100,0,0,313,314,5,105,
        0,0,314,315,5,116,0,0,315,316,5,105,0,0,316,317,5,111,0,0,317,318,
        5,110,0,0,318,319,5,115,0,0,319,24,1,0,0,0,320,321,5,58,0,0,321,
        322,5,113,0,0,322,323,5,117,0,0,323,324,5,97,0,0,324,325,5,110,0,
        0,325,326,5,116,0,0,326,327,5,105,0,0,327,328,5,102,0,0,328,329,
        5,105,0,0,329,330,5,101,0,0,330,331,5,100,0,0,331,332,5,45,0,0,332,
        333,5,112,0,0,333,334,5,114,0,0,334,335,5,101,0,0,335,336,5,99,0,
        0,336,337,5,111,0,0,337,338,5,110,0,0,338,339,5,100,0,0,339,340,
        5,105,0,0,340,341,5,116,0,0,341,342,5,105,0,0,342,343,5,111,0,0,
        343,344,5,110,0,0,344,345,5,115,0,0,345,26,1,0,0,0,346,347,5,58,
        0,0,347,348,5,99,0,0,348,349,5,111,0,0,349,350,5,110,0,0,350,351,
        5,100,0,0,351,352,5,105,0,0,352,353,5,116,0,0,353,354,5,105,0,0,
        354,355,5,111,0,0,355,356,5,110,0,0,356,357,5,97,0,0,357,358,5,108,
        0,0,358,359,5,45,0,0,359,360,5,101,0,0,360,361,5,102,0,0,361,362,
        5,102,0,0,362,363,5,101,0,0,363,364,5,99,0,0,364,365,5,116,0,0,365,
        366,5,115,0,0,366,28,1,0,0,0,367,368,5,58,0,0,368,369,5,102,0,0,
        369,370,5,108,0,0,370,371,5,117,0,0,371,372,5,101,0,0,372,373,5,
        110,0,0,373,374,5,116,0,0,374,375,5,115,0,0,375,30,1,0,0,0,376,377,
        5,58,0,0,377,378,5,97,0,0,378,379,5,100,0,0,379,380,5,108,0,0,380,
        32,1,0,0,0,381,382,5,58,0,0,382,383,5,100,0,0,383,384,5,117,0,0,
        384,385,5,114,0,0,385,386,5,97,0,0,386,387,5,116,0,0,387,388,5,105,
        0,0,388,389,5,118,0,0,389,390,5,101,0,0,390,391,5,45,0,0,391,392,
        5,97,0,0,392,393,5,99,0,0,393,394,5,116,0,0,394,395,5,105,0,0,395,
        396,5,111,0,0,396,397,5,110,0,0,397,398,5,115,0,0,398,34,1,0,0,0,
        399,400,5,58,0,0,400,401,5,100,0,0,401,402,5,117,0,0,402,403,5,114,
        0,0,403,404,5,97,0,0,404,405,5,116,0,0,405,406,5,105,0,0,406,407,
        5,111,0,0,407,408,5,110,0,0,408,409,5,45,0,0,409,410,5,105,0,0,410,
        411,5,110,0,0,411,412,5,101,0,0,412,413,5,113,0,0,413,414,5,117,
        0,0,414,415,5,97,0,0,415,416,5,108,0,0,416,417,5,105,0,0,417,418,
        5,116,0,0,418,419,5,105,0,0,419,420,5,101,0,0,420,421,5,115,0,0,
        421,36,1,0,0,0,422,423,5,58,0,0,423,424,5,99,0,0,424,425,5,111,0,
        0,425,426,5,110,0,0,426,427,5,116,0,0,427,428,5,105,0,0,428,429,
        5,110,0,0,429,430,5,117,0,0,430,431,5,111,0,0,431,432,5,117,0,0,
        432,433,5,115,0,0,433,434,5,45,0,0,434,435,5,101,0,0,435,436,5,102,
        0,0,436,437,5,102,0,0,437,438,5,101,0,0,438,439,5,99,0,0,439,440,
        5,116,0,0,440,441,5,115,0,0,441,38,1,0,0,0,442,443,5,58,0,0,443,
        444,5,100,0,0,444,445,5,101,0,0,445,446,5,114,0,0,446,447,5,105,
        0,0,447,448,5,118,0,0,448,449,5,101,0,0,449,450,5,100,0,0,450,451,
        5,45,0,0,451,452,5,112,0,0,452,453,5,114,0,0,453,454,5,101,0,0,454,
        455,5,100,0,0,455,456,5,105,0,0,456,457,5,99,0,0,457,458,5,97,0,
        0,458,459,5,116,0,0,459,460,5,101,0,0,460,461,5,115,0,0,461,40,1,
        0,0,0,462,463,5,58,0,0,463,464,5,116,0,0,464,465,5,105,0,0,465,466,
        5,109,0,0,466,467,5,101,0,0,467,468,5,100,0,0,468,469,5,45,0,0,469,
        470,5,105,0,0,470,471,5,110,0,0,471,472,5,105,0,0,472,473,5,116,
        0,0,473,474,5,105,0,0,474,475,5,97,0,0,475,476,5,108,0,0,476,477,
        5,45,0,0,477,478,5,108,0,0,478,479,5,105,0,0,479,480,5,116,0,0,480,
        481,5,101,0,0,481,482,5,114,0,0,482,483,5,97,0,0,483,484,5,108,0,
        0,484,485,5,115,0,0,485,42,1,0,0,0,486,487,5,58,0,0,487,488,5,112,
        0,0,488,489,5,114,0,0,489,490,5,101,0,0,490,491,5,102,0,0,491,492,
        5,101,0,0,492,493,5,114,0,0,493,494,5,101,0,0,494,495,5,110,0,0,
        495,496,5,99,0,0,496,497,5,101,0,0,497,498,5,115,0,0,498,44,1,0,
        0,0,499,500,5,58,0,0,500,501,5,99,0,0,501,502,5,111,0,0,502,503,
        5,110,0,0,503,504,5,115,0,0,504,505,5,116,0,0,505,506,5,114,0,0,
        506,507,5,97,0,0,507,508,5,105,0,0,508,509,5,110,0,0,509,510,5,116,
        0,0,510,511,5,115,0,0,511,46,1,0,0,0,512,513,5,40,0,0,513,514,5,
        58,0,0,514,515,5,116,0,0,515,516,5,121,0,0,516,517,5,112,0,0,517,
        518,5,101,0,0,518,519,5,115,0,0,519,48,1,0,0,0,520,521,5,45,0,0,
        521,50,1,0,0,0,522,523,5,40,0,0,523,524,5,101,0,0,524,525,5,105,
        0,0,525,526,5,116,0,0,526,527,5,104,0,0,527,528,5,101,0,0,528,529,
        5,114,0,0,529,52,1,0,0,0,530,531,5,40,0,0,531,532,5,58,0,0,532,533,
        5,99,0,0,533,534,5,111,0,0,534,535,5,110,0,0,535,536,5,115,0,0,536,
        537,5,116,0,0,537,538,5,97,0,0,538,539,5,110,0,0,539,540,5,116,0,
        0,540,541,5,115,0,0,541,54,1,0,0,0,542,543,5,40,0,0,543,544,5,58,
        0,0,544,545,5,112,0,0,545,546,5,114,0,0,546,547,5,101,0,0,547,548,
        5,100,0,0,548,549,5,105,0,0,549,550,5,99,0,0,550,551,5,97,0,0,551,
        552,5,116,0,0,552,553,5,101,0,0,553,554,5,115,0,0,554,56,1,0,0,0,
        555,556,5,40,0,0,556,557,5,58,0,0,557,558,5,102,0,0,558,559,5,117,
        0,0,559,560,5,110,0,0,560,561,5,99,0,0,561,562,5,116,0,0,562,563,
        5,105,0,0,563,564,5,111,0,0,564,565,5,110,0,0,565,566,5,115,0,0,
        566,58,1,0,0,0,567,568,5,40,0,0,568,569,5,58,0,0,569,570,5,97,0,
        0,570,571,5,99,0,0,571,572,5,116,0,0,572,573,5,105,0,0,573,574,5,
        111,0,0,574,575,5,110,0,0,575,60,1,0,0,0,576,577,5,58,0,0,577,578,
        5,112,0,0,578,579,5,97,0,0,579,580,5,114,0,0,580,581,5,97,0,0,581,
        582,5,109,0,0,582,583,5,101,0,0,583,584,5,116,0,0,584,585,5,101,
        0,0,585,586,5,114,0,0,586,587,5,115,0,0,587,588,5,32,0,0,588,589,
        5,40,0,0,589,62,1,0,0,0,590,591,5,58,0,0,591,592,5,112,0,0,592,593,
        5,114,0,0,593,594,5,101,0,0,594,595,5,99,0,0,595,596,5,111,0,0,596,
        597,5,110,0,0,597,598,5,100,0,0,598,599,5,105,0,0,599,600,5,116,
        0,0,600,601,5,105,0,0,601,602,5,111,0,0,602,603,5,110,0,0,603,64,
        1,0,0,0,604,605,5,58,0,0,605,606,5,101,0,0,606,607,5,102,0,0,607,
        608,5,102,0,0,608,609,5,101,0,0,609,610,5,99,0,0,610,611,5,116,0,
        0,611,66,1,0,0,0,612,613,5,40,0,0,613,614,5,41,0,0,614,68,1,0,0,
        0,615,616,5,40,0,0,616,617,5,97,0,0,617,618,5,110,0,0,618,619,5,
        100,0,0,619,70,1,0,0,0,620,621,5,40,0,0,621,622,5,111,0,0,622,623,
        5,114,0,0,623,72,1,0,0,0,624,625,5,40,0,0,625,626,5,110,0,0,626,
        627,5,111,0,0,627,628,5,116,0,0,628,74,1,0,0,0,629,630,5,40,0,0,
        630,631,5,105,0,0,631,632,5,109,0,0,632,633,5,112,0,0,633,634,5,
        108,0,0,634,635,5,121,0,0,635,76,1,0,0,0,636,637,5,40,0,0,637,638,
        5,101,0,0,638,639,5,120,0,0,639,640,5,105,0,0,640,641,5,115,0,0,
        641,642,5,116,0,0,642,643,5,115,0,0,643,78,1,0,0,0,644,645,5,40,
        0,0,645,646,5,102,0,0,646,647,5,111,0,0,647,648,5,114,0,0,648,649,
        5,97,0,0,649,650,5,108,0,0,650,651,5,108,0,0,651,80,1,0,0,0,652,
        653,5,62,0,0,653,82,1,0,0,0,654,655,5,60,0,0,655,84,1,0,0,0,656,
        657,5,62,0,0,657,658,5,61,0,0,658,86,1,0,0,0,659,660,5,60,0,0,660,
        661,5,61,0,0,661,88,1,0,0,0,662,663,5,43,0,0,663,90,1,0,0,0,664,
        665,5,42,0,0,665,92,1,0,0,0,666,667,5,47,0,0,667,94,1,0,0,0,668,
        669,5,40,0,0,669,670,5,119,0,0,670,671,5,104,0,0,671,672,5,101,0,
        0,672,673,5,110,0,0,673,96,1,0,0,0,674,675,5,97,0,0,675,676,5,115,
        0,0,676,677,5,115,0,0,677,678,5,105,0,0,678,679,5,103,0,0,679,680,
        5,110,0,0,680,98,1,0,0,0,681,682,5,115,0,0,682,683,5,99,0,0,683,
        684,5,97,0,0,684,685,5,108,0,0,685,686,5,101,0,0,686,687,5,45,0,
        0,687,688,5,117,0,0,688,689,5,112,0,0,689,100,1,0,0,0,690,691,5,
        115,0,0,691,692,5,99,0,0,692,693,5,97,0,0,693,694,5,108,0,0,694,
        695,5,101,0,0,695,696,5,45,0,0,696,697,5,100,0,0,697,698,5,111,0,
        0,698,699,5,119,0,0,699,700,5,110,0,0,700,102,1,0,0,0,701,702,5,
        105,0,0,702,703,5,110,0,0,703,704,5,99,0,0,704,705,5,114,0,0,705,
        706,5,101,0,0,706,707,5,97,0,0,707,708,5,115,0,0,708,709,5,101,0,
        0,709,104,1,0,0,0,710,711,5,100,0,0,711,712,5,101,0,0,712,713,5,
        99,0,0,713,714,5,114,0,0,714,715,5,101,0,0,715,716,5,97,0,0,716,
        717,5,115,0,0,717,718,5,101,0,0,718,106,1,0,0,0,719,720,5,40,0,0,
        720,721,5,58,0,0,721,722,5,100,0,0,722,723,5,117,0,0,723,724,5,114,
        0,0,724,725,5,97,0,0,725,726,5,116,0,0,726,727,5,105,0,0,727,728,
        5,118,0,0,728,729,5,101,0,0,729,730,5,45,0,0,730,731,5,97,0,0,731,
        732,5,99,0,0,732,733,5,116,0,0,733,734,5,105,0,0,734,735,5,111,0,
        0,735,736,5,110,0,0,736,108,1,0,0,0,737,738,5,58,0,0,738,739,5,100,
        0,0,739,740,5,117,0,0,740,741,5,114,0,0,741,742,5,97,0,0,742,743,
        5,116,0,0,743,744,5,105,0,0,744,745,5,111,0,0,745,746,5,110,0,0,
        746,110,1,0,0,0,747,748,5,58,0,0,748,749,5,99,0,0,749,750,5,111,
        0,0,750,751,5,110,0,0,751,752,5,100,0,0,752,753,5,105,0,0,753,754,
        5,116,0,0,754,755,5,105,0,0,755,756,5,111,0,0,756,757,5,110,0,0,
        757,112,1,0,0,0,758,759,5,63,0,0,759,760,5,100,0,0,760,761,5,117,
        0,0,761,762,5,114,0,0,762,763,5,97,0,0,763,764,5,116,0,0,764,765,
        5,105,0,0,765,766,5,111,0,0,766,767,5,110,0,0,767,114,1,0,0,0,768,
        769,5,61,0,0,769,116,1,0,0,0,770,771,5,35,0,0,771,772,5,116,0,0,
        772,773,5,41,0,0,773,118,1,0,0,0,774,775,5,35,0,0,775,776,5,116,
        0,0,776,120,1,0,0,0,777,778,5,40,0,0,778,779,5,58,0,0,779,780,5,
        100,0,0,780,781,5,101,0,0,781,782,5,114,0,0,782,783,5,105,0,0,783,
        784,5,118,0,0,784,785,5,101,0,0,785,786,5,100,0,0,786,122,1,0,0,
        0,787,788,5,112,0,0,788,789,5,114,0,0,789,790,5,111,0,0,790,791,
        5,98,0,0,791,792,5,108,0,0,792,793,5,101,0,0,793,794,5,109,0,0,794,
        124,1,0,0,0,795,796,5,40,0,0,796,797,5,58,0,0,797,798,5,100,0,0,
        798,799,5,111,0,0,799,800,5,109,0,0,800,801,5,97,0,0,801,802,5,105,
        0,0,802,803,5,110,0,0,803,126,1,0,0,0,804,805,5,40,0,0,805,806,5,
        58,0,0,806,807,5,111,0,0,807,808,5,98,0,0,808,809,5,106,0,0,809,
        810,5,101,0,0,810,811,5,99,0,0,811,812,5,116,0,0,812,813,5,115,0,
        0,813,128,1,0,0,0,814,815,5,40,0,0,815,816,5,58,0,0,816,817,5,105,
        0,0,817,818,5,110,0,0,818,819,5,105,0,0,819,820,5,116,0,0,820,130,
        1,0,0,0,821,822,5,40,0,0,822,823,5,58,0,0,823,824,5,103,0,0,824,
        825,5,111,0,0,825,826,5,97,0,0,826,827,5,108,0,0,827,132,1,0,0,0,
        828,829,5,40,0,0,829,830,5,58,0,0,830,831,5,109,0,0,831,832,5,101,
        0,0,832,833,5,116,0,0,833,834,5,114,0,0,834,835,5,105,0,0,835,836,
        5,99,0,0,836,134,1,0,0,0,837,838,5,109,0,0,838,839,5,105,0,0,839,
        840,5,110,0,0,840,841,5,105,0,0,841,842,5,109,0,0,842,843,5,105,
        0,0,843,844,5,122,0,0,844,845,5,101,0,0,845,136,1,0,0,0,846,847,
        5,109,0,0,847,848,5,97,0,0,848,849,5,120,0,0,849,850,5,105,0,0,850,
        851,5,109,0,0,851,852,5,105,0,0,852,853,5,122,0,0,853,854,5,101,
        0,0,854,138,1,0,0,0,855,856,5,116,0,0,856,857,5,111,0,0,857,858,
        5,116,0,0,858,859,5,97,0,0,859,860,5,108,0,0,860,861,5,45,0,0,861,
        862,5,116,0,0,862,863,5,105,0,0,863,864,5,109,0,0,864,865,5,101,
        0,0,865,140,1,0,0,0,866,870,5,63,0,0,867,871,3,149,74,0,868,871,
        3,143,71,0,869,871,3,145,72,0,870,867,1,0,0,0,870,868,1,0,0,0,870,
        869,1,0,0,0,871,142,1,0,0,0,872,873,5,97,0,0,873,877,5,116,0,0,874,
        875,5,65,0,0,875,877,5,84,0,0,876,872,1,0,0,0,876,874,1,0,0,0,877,
        144,1,0,0,0,878,879,5,115,0,0,879,880,5,116,0,0,880,881,5,97,0,0,
        881,882,5,114,0,0,882,895,5,116,0,0,883,884,5,101,0,0,884,885,5,
        110,0,0,885,895,5,100,0,0,886,887,5,69,0,0,887,888,5,78,0,0,888,
        895,5,68,0,0,889,890,5,83,0,0,890,891,5,84,0,0,891,892,5,65,0,0,
        892,893,5,82,0,0,893,895,5,84,0,0,894,878,1,0,0,0,894,883,1,0,0,
        0,894,886,1,0,0,0,894,889,1,0,0,0,895,146,1,0,0,0,896,897,5,111,
        0,0,897,898,5,118,0,0,898,899,5,101,0,0,899,905,5,114,0,0,900,901,
        5,79,0,0,901,902,5,86,0,0,902,903,5,69,0,0,903,905,5,82,0,0,904,
        896,1,0,0,0,904,900,1,0,0,0,905,907,1,0,0,0,906,908,5,32,0,0,907,
        906,1,0,0,0,908,909,1,0,0,0,909,907,1,0,0,0,909,910,1,0,0,0,910,
        917,1,0,0,0,911,912,5,97,0,0,912,913,5,108,0,0,913,918,5,108,0,0,
        914,915,5,65,0,0,915,916,5,76,0,0,916,918,5,76,0,0,917,911,1,0,0,
        0,917,914,1,0,0,0,918,148,1,0,0,0,919,923,7,0,0,0,920,922,7,1,0,
        0,921,920,1,0,0,0,922,925,1,0,0,0,923,921,1,0,0,0,923,924,1,0,0,
        0,924,150,1,0,0,0,925,923,1,0,0,0,926,928,5,45,0,0,927,926,1,0,0,
        0,927,928,1,0,0,0,928,930,1,0,0,0,929,931,2,48,57,0,930,929,1,0,
        0,0,931,932,1,0,0,0,932,930,1,0,0,0,932,933,1,0,0,0,933,949,1,0,
        0,0,934,936,5,45,0,0,935,934,1,0,0,0,935,936,1,0,0,0,936,938,1,0,
        0,0,937,939,2,48,57,0,938,937,1,0,0,0,939,940,1,0,0,0,940,938,1,
        0,0,0,940,941,1,0,0,0,941,942,1,0,0,0,942,944,5,46,0,0,943,945,2,
        48,57,0,944,943,1,0,0,0,945,946,1,0,0,0,946,944,1,0,0,0,946,947,
        1,0,0,0,947,949,1,0,0,0,948,927,1,0,0,0,948,935,1,0,0,0,949,152,
        1,0,0,0,950,954,5,59,0,0,951,953,8,2,0,0,952,951,1,0,0,0,953,956,
        1,0,0,0,954,952,1,0,0,0,954,955,1,0,0,0,955,957,1,0,0,0,956,954,
        1,0,0,0,957,958,6,76,0,0,958,154,1,0,0,0,959,961,7,3,0,0,960,959,
        1,0,0,0,961,962,1,0,0,0,962,960,1,0,0,0,962,963,1,0,0,0,963,964,
        1,0,0,0,964,965,6,77,0,0,965,156,1,0,0,0,16,0,870,876,894,904,909,
        917,923,927,932,935,940,946,948,954,962,1,6,0,0
    ]

class pddl22Lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    T__14 = 15
    T__15 = 16
    T__16 = 17
    T__17 = 18
    T__18 = 19
    T__19 = 20
    T__20 = 21
    T__21 = 22
    T__22 = 23
    T__23 = 24
    T__24 = 25
    T__25 = 26
    T__26 = 27
    T__27 = 28
    T__28 = 29
    T__29 = 30
    T__30 = 31
    T__31 = 32
    T__32 = 33
    T__33 = 34
    T__34 = 35
    T__35 = 36
    T__36 = 37
    T__37 = 38
    T__38 = 39
    T__39 = 40
    T__40 = 41
    T__41 = 42
    T__42 = 43
    T__43 = 44
    T__44 = 45
    T__45 = 46
    T__46 = 47
    T__47 = 48
    T__48 = 49
    T__49 = 50
    T__50 = 51
    T__51 = 52
    T__52 = 53
    T__53 = 54
    T__54 = 55
    T__55 = 56
    T__56 = 57
    T__57 = 58
    T__58 = 59
    T__59 = 60
    T__60 = 61
    T__61 = 62
    T__62 = 63
    T__63 = 64
    T__64 = 65
    T__65 = 66
    T__66 = 67
    T__67 = 68
    T__68 = 69
    T__69 = 70
    VARIABLE = 71
    AT = 72
    TIME_SPECIFIER_SUFFIX = 73
    OVER_ALL = 74
    NAME = 75
    NUMBER = 76
    COMMENT = 77
    WS = 78

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'(define'", "'('", "'domain'", "')'", "'(:requirements'", "':strips'", 
            "':typing'", "':negative-preconditions'", "':disjunctive-preconditions'", 
            "':equality'", "':existential-preconditions'", "':universal-preconditions'", 
            "':quantified-preconditions'", "':conditional-effects'", "':fluents'", 
            "':adl'", "':durative-actions'", "':duration-inequalities'", 
            "':continuous-effects'", "':derived-predicates'", "':timed-initial-literals'", 
            "':preferences'", "':constraints'", "'(:types'", "'-'", "'(either'", 
            "'(:constants'", "'(:predicates'", "'(:functions'", "'(:action'", 
            "':parameters ('", "':precondition'", "':effect'", "'()'", "'(and'", 
            "'(or'", "'(not'", "'(imply'", "'(exists'", "'(forall'", "'>'", 
            "'<'", "'>='", "'<='", "'+'", "'*'", "'/'", "'(when'", "'assign'", 
            "'scale-up'", "'scale-down'", "'increase'", "'decrease'", "'(:durative-action'", 
            "':duration'", "':condition'", "'?duration'", "'='", "'#t)'", 
            "'#t'", "'(:derived'", "'problem'", "'(:domain'", "'(:objects'", 
            "'(:init'", "'(:goal'", "'(:metric'", "'minimize'", "'maximize'", 
            "'total-time'" ]

    symbolicNames = [ "<INVALID>",
            "VARIABLE", "AT", "TIME_SPECIFIER_SUFFIX", "OVER_ALL", "NAME", 
            "NUMBER", "COMMENT", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "T__17", "T__18", "T__19", 
                  "T__20", "T__21", "T__22", "T__23", "T__24", "T__25", 
                  "T__26", "T__27", "T__28", "T__29", "T__30", "T__31", 
                  "T__32", "T__33", "T__34", "T__35", "T__36", "T__37", 
                  "T__38", "T__39", "T__40", "T__41", "T__42", "T__43", 
                  "T__44", "T__45", "T__46", "T__47", "T__48", "T__49", 
                  "T__50", "T__51", "T__52", "T__53", "T__54", "T__55", 
                  "T__56", "T__57", "T__58", "T__59", "T__60", "T__61", 
                  "T__62", "T__63", "T__64", "T__65", "T__66", "T__67", 
                  "T__68", "T__69", "VARIABLE", "AT", "TIME_SPECIFIER_SUFFIX", 
                  "OVER_ALL", "NAME", "NUMBER", "COMMENT", "WS" ]

    grammarFileName = "pddl22.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.10.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


