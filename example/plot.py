import matplotlib.pyplot as plt

xs = []
ys = []
with open('2.out', 'r') as f:
    for line in f.read().splitlines():
        x = float(line.split()[0])
        y = float(line.split()[1])
        xs.append(x)
        ys.append(y)

plt.plot(xs, ys)
#plt.ylabel('some numbers')

plt.xlim((900, 1600))

ax = plt.gca()
ax.invert_xaxis()

plt.savefig('spectrum.png')
