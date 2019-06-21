# Federico Tondolo
# Summer 2019 at the Columbia University Medical Center 
import os
import csv
import sys
import pyabf
import numpy as np
import matplotlib.pyplot as plt

# Warning obfuscation to make print statements more aesthetically pleasing
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

def main():
    # Creating OUTPUT directory
    os.mkdir('OUTPUT')
    # Loop for every file inside current dir
    for filename in os.listdir('.'):
        # If file is an ABF file
        if (filename.endswith(".abf")):
            # Variable Initialisation
            abf = pyabf.ABF(filename)
            abf.setSweep(0)
            next_status=abf.sweepC[1]
            partial_sum=0
            counter=0
            channel=0
            # Plotting Bonanza
            if (len(abf.tagComments)> 0):
                plot_comments(abf)
            if ((abf.channelCount>1) | (abf.sweepCount>0)):
                plot_sweeps(abf, 1)
                plot_sweeps(abf, 2)
            plot_epoch(abf)
            # Loop for every sweep
            for y in range(abf.sweepCount):
                abf.setSweep(y)
                # Printing Epochs
                print('SWEEP #%d' % y)
                for i, p1 in enumerate(abf.sweepEpochs.p1s):
                    epochLevel = abf.sweepEpochs.levels[i]
                    epochType = abf.sweepEpochs.types[i]
                    print(f"Epoch index {i}: At point {p1} there is a {epochType} to level {epochLevel}")
                # Loop for every channel
                while channel < abf.channelCount:
                    channel+=1
                    x=channel-1
                    # Creation of CSV file
                    with open('./OUTPUT/%s-sweep%d-ch%d.csv' % (filename[:-4], y, channel), 'w') as csvfile:
                        filewriter = csv.writer(csvfile, delimiter=',',
                                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        filewriter.writerow(['Time (s)', 'Command (DAC)', 'Reading (ADC)', 'Average ADC per DAC'])
                        # Loop for entire recorded time
                        while (x <len(abf.sweepY)-1):
                            next_status=abf.sweepC[x+1]
                            # If DAC will not change
                            if (next_status==abf.sweepC[x]):
                                partial_sum+=abf.sweepY[x]
                                counter+=1
                                filewriter.writerow([abf.sweepX[x], abf.sweepC[x], abf.sweepY[x], 'TBD'])
                                x+=abf.channelCount
                            # If DAC will change
                            else:
                                partial_sum/=counter
                                counter=1
                                filewriter.writerow([abf.sweepX[x], abf.sweepC[x], abf.sweepY[x], partial_sum])
                                x+=abf.channelCount
                        # Final round
                        partial_sum/=counter
                        counter=1
                        filewriter.writerow([abf.sweepX[x], abf.sweepC[x], abf.sweepY[x], partial_sum])
        # If file is not an ABF recording 
        else:
            continue

# THE FUNCTIONS FROM HERE ONWARDS ARE ALMOST LINE FOR LINE THOSE SUPPLIED WITH PYABF

# Plot creation following recorded epochs
def plot_epoch(abfinput):
    # Window
    fig = plt.figure(figsize=(8, 5))
    # Graph 1
    ax1 = fig.add_subplot(211)
    ax1.plot(abfinput.sweepY, color='b')
    ax1.set_ylabel("ADC (measurement)")
    ax1.set_xlabel("Sweep point (index)")

    # Graph 2
    ax2 = fig.add_subplot(212)
    ax2.plot(abfinput.sweepC, color='r')
    ax2.set_ylabel("DAC (command)")
    ax2.set_xlabel("Sweep point (index)")

    # Loop through epochs
    for p1 in abfinput.sweepEpochs.p1s:
        ax1.axvline(p1, color='k', ls='--', alpha=.5)
        ax2.axvline(p1, color='k', ls='--', alpha=.5)

    # Show
    plt.tight_layout()
    plt.show()

def plot_sweeps(abfinput, ch):
    # Window
    plt.figure(figsize=(8, 5))
    plt.title("Sweeps For Channel %d"% ch)
    plt.ylabel(abfinput.sweepLabelY)
    plt.xlabel(abfinput.sweepLabelX)
    for i in range(abfinput.sweepCount):
        if (ch==1):
            abfinput.setSweep(i, channel=0)
            plt.plot(abfinput.sweepX, abfinput.sweepY, alpha=.5, label="Sweep %d"%(i+1))
        else:
            abfinput.setSweep(i, channel=1)
            plt.plot(abfinput.sweepX, abfinput.sweepY, alpha=.5, label="Sweep %d"%(i+1))
    # Show
    plt.legend()
    plt.show()

def plot_comments(abfinput):
    # Window
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
    # Show
    plt.legend()
    plt.title("ABF File with Tags")
    plt.show()

main()
