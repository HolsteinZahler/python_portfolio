import numpy as np
from matplotlib.pyplot import *
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import os

def read_ascii(fn):
    """ reads ascii file, returns  list of lines """
    try:
        inputfile = open(fn, 'r')
    except Exception as error:
        print(error)
        return
    lines = inputfile.readlines()
    inputfile.close()
    return lines

def read_ascii_column(fn):
    lines = read_ascii(fn)
    data = []
    for line in lines:
        st = line.split()
        if st[0] != '#' and st[0] != '!' and st[0] != '*': # possible comments identifiers
            data.append(float(i) for i in list(st))
    data = list(zip(*data))
    return data

my_cmap=matplotlib.cm.get_cmap('jet')
my_cmap.set_bad('w')


# set up initial and last ID-numbers
start=0
end=78
increment=26

#Number of digits in output
digits=4

#Set plot ranges
xlimit=2E-3
xlims=[-xlimit,xlimit]
ylims=xlims

digits=digits-1



count=int(start/increment)
for i in range(start,end+1,increment):
	print("Processing file "+str(i)+" for image "+str(count))
	x_fn = 'x_PHAD_%s.ssv'%str(i)
	y_fn = 'y_PHAD_%s.ssv'%str(i)

	x = read_ascii_column(fn = x_fn)[0]
	y = read_ascii_column(fn = y_fn)[0]

	# Comment to turn off tick marks
	ax = matplotlib.pyplot.subplot(111)
	ax.set_xticks([xlims[0],0,xlims[1]])
	ax.set_yticks([ylims[0],0,ylims[1]])
	# Sets minor tick marks
	XminorLocator = MultipleLocator(xlimit/2)
	YminorLocator = MultipleLocator(xlimit/2)
	ax.xaxis.set_minor_locator(XminorLocator)
	ax.yaxis.set_minor_locator(YminorLocator)

	# Comment to turn on tick marks
	#gca().tick_params(axis='x',labelbottom='False')
	#gca().tick_params(axis='y',labelleft='False')

    #histogramm 2D
    hist2d(x, y, norm=matplotlib.colors.LogNorm(), range=[xlims,ylims], bins=200, cmap=my_cmap, vmax=50)

	colorbar()
#    clim(0,50) #colorscale limits

	xlim(xlims) # X-axis limits
	ylim(ylims)

	xlabel('X, m') #labels
	ylabel('Y, m')
#    title('Density')
	if (count!=0):
		num_zeros=int(digits-np.floor(np.math.log(float(count),10.0)))
	else:
		num_zeros=digits
	image_label=str(0)
	for j in range(1,num_zeros):
		image_label=image_label+str(0)
	savefig('%s.png'%(image_label+str(count)), dpi=600)
	matplotlib.pyplot.clf()
	count+=1

# Must be edited so that number of zeros and X in %0X are the same
#Sets command for ffmpeg:
#command='ffmpeg -framerate 10 -start_number 0000 -i %4d.png video.mov'
#command='ffmpeg -framerate 10 -start_number 0000 -i %4d.png video.mp4'
#command='ffmpeg -r 1/5 -start_number 0000 -i %4d.png -c:v libx264 -vf fps=10 -pix_fmt yuv420p video.mp4'

#Uncomment to run annimation command
#os.system(command)
