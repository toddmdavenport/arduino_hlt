#!/usr/bin/python

import csv
import matplotlib.pyplot as plt

def csv_parser(date):
    with open('data/' + date, 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=",")
        time, set_t, probe = [], [], []
        for row in data:
            time.append(row[0]) 
            set_t.append(row[1])
            probe.append(row[2])
    return time, set_t, probe 

time, set_t, probe =  csv_parser('2012-11-30')
plt.plot(probe)
plt.ylabel('Degrees F')
plt.show()


#sample data set


