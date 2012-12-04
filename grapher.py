#!/usr/bin/python

import csv, matplotlib

def csv_parser(date):
    with open('data/' + date, 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=",")
        time, set_t, probe = [], [], []
        for row in data:
            time.append(row[0]) 
            set_t.append(row[1])
            probe.append(row[2])
    return time, set_t, probe 

print csv_parser('2012-11-30')


