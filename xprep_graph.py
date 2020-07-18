#!/bin/env python3.6

import re
import os
import pandas as pd
import matplotlib
# Path needed for widows file system
from pathlib import Path 
#matplotlib.use('agg')
import matplotlib.pyplot as plt
#matplotlib inline

# get the student to put a known prp file local to the notebook for simplicity?
input_path = Path(r'.\62_Ruby_98.prp')
project_dir = os.getcwd()

with open(input_path) as file:
    contents = file.read()
    
# Search file for beginning and ending of stats table
x = re.search(" Inf",contents)
y = re.search("Merged",contents)

if x is None and y is None:
    pass
else:
    stats_table = contents[x.start():y.start()].split('\n')

    # Split the rows of the stats table into individual elements
    n = 0
    data = []
    for item in stats_table:
        data.append(stats_table[n].split())
        n+=1

    # Store the stats table as a pandas dataframe and remove last 5 rows (are empty or contain punctuation)
    df = pd.DataFrame(data,columns=['Resolution', 'dash', 'Resolution High',
                                    '#`Data','#Theory','%Complete', 'Redundancy',
                                    'Mean I','Mean I/s','R(int)','Rsigma'],dtype=float)
    df.drop(df.tail(5).index,inplace=True)

    x = df['Resolution High']

    y1 = df['R(int)']
    y2 = df['Mean I/s']
    y3 = df['%Complete']


# Set up the sub plot arrangement (left, right or top bottom)
# Setting up for two comparative plot spaces
    fig, (ax1, ax2) = plt.subplots(2, 1)

    
# First plot - Rint and Mean I/s vs. Resolution
    ax1.plot(x, y1, 'r', x, y2, 'b')
    xaxis = x
    yaxis1 = [float(i) for i in y1] 
    yaxis2 = [float(i) for i in y2]
    
    ax1.set_title('Rint and Mean I/s vs. Resolution', size=24)
    ax1.set_xlabel('Resolution', size=20)

# Set up parameters for the Rint graph
    ax1.set_ylabel('R(int)', color='r', size=16)
    ax1.tick_params('x', size=14, labelsize=18)
    ax1.tick_params('y', colors='r', size=14, labelsize=18)
    
    # Determine what scaling to use for the Rint graph
    if y1.max() > 0.5:
        ax1.set_ylim(0, 0.5)
    else:
        ax1.set_ylim(y1.min() - 0.01, y1.max() + 0.01)
        
# Set up parameters for overlaid Mean I/s graph
    ax1b = ax1.twinx()
    ax1b.plot(xaxis, yaxis2, 'blue', label='Mean I/s', color='b')
    ax1b.set_ylabel('Mean I/s', color='b', size=20)
    ax1b.tick_params('y', colors='b', size=14, labelsize=18)
    if y2.min() < 2.0:
        plt.axhline(y=2.0, color='black', linestyle='--')

# draw a cut off line at 2 I/s, the cutoff for shelxl refinements.
    plt.axhline(y=2.0, color='blue', linestyle='--')
    plt.gca().invert_xaxis()
    
# Second plot - Completeness vs. Resolution
    ax2.plot(x, y3, 'g')
    xaxis = x
    yaxis = [float(i) for i in y3] 
    ax2.set_title('Completeness vs. Resolution', size=24)
    ax2.set_xlabel('Resolution', size=20)
    ax2.set_ylabel('Completeness (%)', color='g', size=16)
    ax2.tick_params('x', size=14, labelsize=18)
    ax2.tick_params('y', colors='g',size=14, labelsize=16)
    ax2.set_xlim(df['Resolution High'].max()+0.1, df['Resolution High'].min()-0.1)
    ax2.set_ylim(0,105)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=1.5, top=2.5, wspace=0.2, hspace=0.4)
    plt.savefig(os.path.join(project_dir,'xprep.png'),bbox_inches='tight',pad_inches=0.1)