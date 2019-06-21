import os
import csv
import sys
import pyabf
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Creating OUTPUT directory
    os.mkdir('OUTPUT')
    # Loops for every file inside current dir
    for filename in os.listdir('.'):
        # If file is a video file
        if (filename.endswith(".abf")):
            abf = pyabf.ABF(filename)
            abf.setSweep(0)
            previous_status=abf.sweepC[0]
            partial_sum=0
            counter=0
            channel=0
            if (len(abf.tagComments)> 0):
                plot_comments(abf)
            if (abf.channelCount>1):
                plot_channels(abf)
            if (abf.sweepCount>0):
                plot_sweeps(abf)
            plot_epoch(abf)
            for y in range(abf.sweepCount):
                abf.setSweep(y)
                print('SWEEP #%d' % y)
                for i, p1 in enumerate(abf.sweepEpochs.p1s):
                    epochLevel = abf.sweepEpochs.levels[i]
                    epochType = abf.sweepEpochs.types[i]
                    print(f"Epoch index {i}: At point {p1} there is a {epochType} to level {epochLevel}")
                while channel < abf.channelCount:
                    channel+=1
                    x=channel-1
                    with open('./OUTPUT/%s-sweep%d-ch%d.csv' % (filename[:-4], y, channel), 'w') as csvfile:
                        filewriter = csv.writer(csvfile, delimiter=',',
                                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        filewriter.writerow(['Time (s)', 'Command (DAC)', 'Reading (ADC)', 'Average ADC per DAC'])
                        while (x <len(abf.sweepY)):
                            if ((x!=len(abf.sweepY)-1) | (previous_status==abf.sweepC[x])):
                                partial_sum+=abf.sweepY[x]
                                counter+=1
                                filewriter.writerow([abf.sweepX[x], abf.sweepC[x], abf.sweepY[x], 'TBD'])
                                x+=abf.channelCount
                            else:
                                partial_sum/=counter
                                previous_status=abf.sweepC[x]
                                counter=1
                                filewriter.writerow([abf.sweepX[x], abf.sweepC[x], abf.sweepY[x], partial_sum])
                                x+=abf.channelCount
        # If file is not a video 
        else:
            continue

def plot_epoch(abfinput):
    fig = plt.figure(figsize=(8, 5))
    ax1 = fig.add_subplot(211)
    ax1.plot(abfinput.sweepY, color='b')
    ax1.set_ylabel("ADC (measurement)")
    ax1.set_xlabel("Sweep point (index)")

    ax2 = fig.add_subplot(212)
    ax2.plot(abfinput.sweepC, color='r')
    ax2.set_ylabel("DAC (command)")
    ax2.set_xlabel("Sweep point (index)")

    for p1 in abfinput.sweepEpochs.p1s:
        ax1.axvline(p1, color='k', ls='--', alpha=.5)
        ax2.axvline(p1, color='k', ls='--', alpha=.5)

    plt.tight_layout()
    plt.show()

def plot_sweeps(abfinput):
    plt.figure(figsize=(8, 5))
    plt.title("Sweeps")
    plt.ylabel(abfinput.sweepLabelY)
    plt.xlabel(abfinput.sweepLabelX)
    for i in range(abfinput.sweepCount):
        abfinput.setSweep(i)
        plt.plot(abfinput.sweepX, abfinput.sweepY, alpha=.5, label="sweep %d"%(i+1))
    plt.legend()
    plt.show()

def plot_channels(abfinput):
    fig = plt.figure(figsize=(8, 5))
    # plot the first channel
    abfinput.setSweep(sweepNumber=0, channel=0)
    plt.plot(abfinput.sweepX, abfinput.sweepY, label="Channel 1")
    # plot the second channel
    abfinput.setSweep(sweepNumber=0, channel=1)
    plt.plot(abfinput.sweepX, abfinput.sweepY, label="Channel 2")
    # decorate the plot
    plt.ylabel(abfinput.sweepLabelY)
    plt.xlabel(abfinput.sweepLabelX)
    plt.axis([25, 45, -70, 50])
    plt.legend()
    plt.show()

def plot_comments(abfinput):
    # create a plot with time on the horizontal axis
    plt.figure(figsize=(8, 5))
    for sweep in abfinput.sweepList:
        abfinput.setSweep(sweep, absoluteTime=True) # <-- relates to sweepX
        plt.plot(abfinput.sweepX, abfinput.sweepY, lw=.5, alpha=.5, color='C0')
    plt.margins(0, .5)
    plt.ylabel(abfinput.sweepLabelY)
    plt.xlabel(abfinput.sweepLabelX)
    # now add the tags as vertical lines
    for i, tagTimeSec in enumerate(abfinput.tagTimesSec):
        posX = abfinput.tagTimesSec[i]
        comment = abfinput.tagComments[i]
        color = "C%d"%(i+1)
        plt.axvline(posX, label=comment, color=color, ls='--')
    plt.legend()
    plt.title("ABF File with Tags")
    plt.show()

main()
