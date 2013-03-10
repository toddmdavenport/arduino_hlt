#!/usr/bin/python

import serial, time, datetime, argparse

"""Script to control an electric hot liquor tank throught an arduino
and collect temperature data from sensor"""

def main():
    #command line arguments
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Script to control an electric hot liquor tank throught an arduino and collect sensor and state data")
    parser.add_argument("-t", "--settemp", help="sets the target temp in deg F. Range is 1 to 200", type=int)
    parser.add_argument("-n", "--on", help= "turns the controller to an 'ON' state", action="store_true")
    parser.add_argument("-f", "--off", help= "turns the controller to an 'OFF' state", action="store_true")
    parser.add_argument("-d", "--data", help= "requestes available data from the controller", action="store_true")
    parser.add_argument("-w","--web", help= "get data formated for web interface.",action="store_true")
    args = parser.parse_args()
    #open a serial connection and save it to 'ser'
    try:
        ser = serial.Serial('/dev/ttyACM0',9600,timeout=3)
        time.sleep(1)
    except:
        print "Could not connect to the serila device."
        raise SystemExit
    
    if args.settemp: 
        if args.settemp >= 1 and args.settemp <= 200:   
            ser.write("t"+str(args.settemp)) # writes a set temp to the controller 
        else:
            print( "%i is not between 1 and 200" % args.settemp) 
        time.sleep(2)

    # turns the controller to an ON state.
    # If it is not "ON" the controller cannont
    #activate the heating element but a target
    # temp can be set
    if args.on: 
        ser.write("n")
        time.sleep(2)
    #set the system to an "OFF" standby state.
    if args.off:
        ser.write("f")
        time.sleep(2)
    # request operation data and collect response
    if args.data:
        ser.write("d")
        sys_data = ser.read(size=35) #newlines are in win format. Causing problems.
        data_logger(sys_data)
    #request and retrun data for flask web frontend
    if args.web:
        ser.write("d")
        sys_data = ser.read(size=35)
        print(sys_data)
    #closing serial connection
    ser.close()

def data_logger(data):
    """Takes sensor and state info from the serial line, formats, date stamps and writes it to a file."""
    if data[0:3] == "OFF":
        return 
    else:
        data = data.strip()
        probe_temp = data[data.find(":")+1 : data.find("s")]
        set_temp = data[data.rfind(":") + 1:]
        myfile = open("/home/tdavenport/arduino_hlt/data/" + time.strftime("%Y-%m-%d"),'a')
        myfile.write(",".join([time.strftime("%H:%M:%S") ,set_temp, probe_temp]) )
        myfile.close()

if __name__ == "__main__":
        main()
