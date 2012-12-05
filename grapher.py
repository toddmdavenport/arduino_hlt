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
#
#
#11:16:11,182,77.34
#11:20:16,10,82.96
#11:23:31,10,81.61
#11:29:41,10,81.27
#11:52:43,10,80.26
#11:53:05,10,80.26
#11:54:05,10,80.15
#11:55:05,10,80.15
#11:56:05,10,80.15
#11:57:05,10,80.04
#11:58:05,10,80.04
#11:59:05,10,79.93
#12:00:05,10,79.93
#12:01:05,10,79.93
#12:02:06,10,79.93
#12:03:05,10,79.81
#12:04:05,10,79.81
#12:05:05,10,79.81
#12:06:05,10,79.70
#12:07:05,10,79.70
#12:08:05,10,79.70
#12:10:05,180,80.04
#12:11:05,180,83.41
#12:12:06,180,84.76
#12:13:05,180,86.45
#12:17:05,180,90.72
#12:18:06,180,91.74
#12:19:05,180,93.65
#12:20:05,180,95.11
#12:21:05,180,96.69
#12:22:05,180,98.15
#12:23:05,180,99.84
#12:24:05,180,101.52
#12:25:05,180,102.99
#12:26:05,180,104.56
#12:27:05,180,105.69
#12:28:05,180,107.71
#12:29:05,180,108.95
#12:30:05,180,110.75
#12:31:06,180,112.44
#12:32:05,180,113.67
#12:33:05,180,115.25
#12:34:05,180,116.82
#12:35:05,180,118.29
#12:36:05,180,120.09
#12:37:06,180,121.55
#12:38:05,180,123.01
#12:39:05,180,124.47
#12:40:05,180,125.71
#12:41:05,180,127.51
#12:42:05,180,129.31
#12:43:05,180,131.00
#12:44:05,180,132.69
#12:45:05,180,134.71
#12:46:05,180,136.51
#12:47:05,180,138.54
#12:48:05,180,140.23
#12:49:05,180,141.91
#12:50:06,180,143.71
#12:51:05,180,145.29
#12:52:05,180,146.98
#12:53:05,180,148.66
#12:54:05,180,150.24
#12:55:05,180,151.70
#12:56:06,180,153.16
#12:57:05,180,154.74
#12:58:05,180,156.31
#12:59:05,180,157.77
#13:00:05,180,159.58
#13:01:05,180,160.93
#13:02:05,180,162.50
#13:03:06,180,164.08
#13:04:05,180,165.65
#13:05:05,180,166.89
#13:06:05,180,168.46
#13:07:05,180,170.04
#13:08:05,180,171.61
#13:09:06,180,173.08
#13:10:05,180,174.43
#13:11:05,180,176.11
#13:12:05,180,177.58
#13:13:05,180,179.04
#13:14:05,180,180.27
#13:15:05,180,179.94
#13:16:06,180,180.61
#13:17:05,180,179.94
#13:18:05,180,180.39
#13:19:05,180,180.16
#13:20:05,180,180.05
#13:21:05,180,180.16
#13:22:05,180,180.27
#13:23:05,180,180.05
#13:24:05,180,180.16
#13:25:05,180,179.71
#13:26:05,180,180.84
#13:27:05,180,180.16
#13:28:05,180,180.16
#13:29:06,180,180.05
#13:30:05,180,180.61
#13:31:05,180,180.27
#13:32:05,180,180.05
#13:33:05,180,180.27
#13:34:05,180,179.94
#13:35:05,180,180.84
#13:36:05,180,180.50
#13:37:05,180,180.05
#13:38:05,180,180.50
#13:39:05,180,180.61
#13:40:05,180,180.27
#13:41:05,180,179.94
#13:42:06,180,180.95
#13:43:05,180,180.61
#13:44:05,180,180.27
#13:45:05,180,179.83
#13:46:05,180,180.72
#13:47:05,180,180.61
#13:48:05,180,180.27
#13:49:05,180,179.94
#13:50:05,180,180.84
#13:51:05,180,180.72
#13:52:05,180,180.39
#13:53:05,180,180.05
#13:54:05,180,180.61
#13:55:06,180,180.72
#13:56:05,180,180.39
#13:57:05,180,180.16
#13:58:05,180,179.83
#13:59:05,180,180.84
#14:00:05,180,180.50
#14:01:05,180,180.16
#14:02:05,180,179.94
