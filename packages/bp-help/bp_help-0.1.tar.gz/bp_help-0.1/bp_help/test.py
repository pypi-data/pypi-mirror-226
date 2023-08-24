

from itertools import groupby
from operator import itemgetter

def conseq(args):
    i, x = args
    return i - x

days = [1, 3, 4, 5, 6, 7]
weeknr = 1
streak = 0

conseq_days = 0
for k, g in groupby(enumerate(days), conseq):
    conseq_days = list(map(itemgetter(1), g))
    print(conseq_days)
steak = len(conseq_days)
print(steak)
    # streak = max(map(len, map(itemgetter(1), g)))
#    print(streak)