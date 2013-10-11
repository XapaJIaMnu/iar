import matplotlib.pyplot as plt

def plot(finalx,finaly):
	ax = plt.axes()
	plt.xlim((- abs(finalx + 30),abs(finalx + 30)))
	plt.ylim((- abs(finaly + 30),abs(finaly + 30)))
	ax.arrow(0, 0, finalx, finaly, head_width=20, head_length=30, fc='k', ec='k')
	plt.show()