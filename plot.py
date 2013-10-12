import matplotlib.pyplot as plt

def plot(finalx,finaly):
	ax = plt.axes()
	plt.xlim((- abs(finalx + 30),abs(finalx + 30)))
	plt.ylim((- abs(finaly + 30),abs(finaly + 30)))
	ax.arrow(0, 0, finalx, finaly, head_width=20, head_length=30, fc='k', ec='k')
	plt.show()

def plotPath(xs, ys):
    maxXY = max(max(xs), max(ys))
#    maxY = max(ys)
    plt.xlim((-abs(maxXY + 30),abs(maxXY + 30)))
    plt.ylim((-abs(maxXY + 30),abs(maxXY + 30)))
    plt.plot(xs, ys)
    #for (x, y) in xys:
    #    .arrow(endx, endy, x, y, head_width=1, head_length=1, fc='k', ec='k')
    #    endx = x
    #    endy = y
    plt.show()

class InteractivePlot:
    def __init__(self):
        plt.ion()
        self.fig = plt.figure()
    
    def update(self, xs, ys):
        plt.clf()
        maxXY = max(max(xs), max(ys))
    #    maxY = max(ys)
        plt.xlim((-abs(maxXY + 30),abs(maxXY + 30)))
        plt.ylim((-abs(maxXY + 30),abs(maxXY + 30)))
        plt.plot(xs, ys)
        self.fig.canvas.draw()
