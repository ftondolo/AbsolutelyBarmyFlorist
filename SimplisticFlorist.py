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
            x=0
            for y in range(abf.sweepCount):
                abf.setSweep(y)
                while channel < abf.channelCount:
                    channel+=1
                    x=channel-1
                    with open('./OUTPUT/%s-sweep%d-ch%d.csv' % (filename[:-4], y, channel), 'w') as csvfile:
                        filewriter = csv.writer(csvfile, delimiter=',',
                                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        filewriter.writerow(['Time (s)', 'Command (DAC)', 'Reading (ADC)', 'Average ADC per DAC'])
                        while (x <len(abf.sweepY)):
                            if (previous_status==abf.sweepC[x]):
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

main()
