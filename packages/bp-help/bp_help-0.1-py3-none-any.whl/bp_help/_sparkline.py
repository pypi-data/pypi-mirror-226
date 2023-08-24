BARS = u'▁▂▃▄▅▆▇█'
import sys
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
data = [float(x) for x in data if x]
data = [(len(BARS)-1)*n/max(data) for n in data]
incr = min(data)
width = (max(data) - min(data)) / (len(BARS) - 1)
bins = [i*width+incr for i in range(len(BARS))]
indexes = []
for n in data:
    for i, thres in enumerate(bins):
        if thres <= n < thres+width:
            indexes.append(i)
            break
sparkline = ''.join(BARS[i] for i in indexes)
print(sparkline)