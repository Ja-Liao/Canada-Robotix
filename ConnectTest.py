import serial
import time
import string
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
from datetime import date

### modify the Port in line 12 below to the port used in your computer

# connect with arduino
arduino = serial.Serial(port = "COM3", baudrate = 9600)
# x-axis (will have to change this later to match the data collection period)
index = count() 
specifiedIntervalIndex = count()
timeAxis = []
powerAxis = []
specifiedIntervalTimeAxis = []
specifiedIntervalPowerAxis = []
# variable tracking whether or not the button on the breadboard has been pressed
collectingData = False

# change the collectionDuration variable to alter the amount of time spent collecting data after
# the button on the arduino has been pressed
collectionDuration = 75.6 # the system has a a lot of delay, to record 30s, write 75.6
minPower = 100000
maxPower = -100000
startTime = 0
fig, axs = plt.subplots(2, 1)
start_save_data_time = 0

def writeData(i):
    global collectingData
    global startTime
    global start_save_data_time
    
    # get data from the arduino
    encodedData = arduino.readline()
    # convert the data into a string
    decodedData = str(encodedData[0:len(encodedData)].decode("utf-8"))
    print(decodedData)

    # check if the button on the breadboard has been pressed
    if decodedData == "Button Pressed\r\n" and collectingData == False:
        # log the time at which specified data collection starts
        startTime = time.time()
        collectingData = True
        return
    else:
        # if the data is not a string, it should be a float, so convert it to a float
        decodedData = float(decodedData)

    global minPower
    global maxPower
    # check current power and update the min and/or max power values
    if(decodedData > maxPower):
        maxPower = decodedData
    if(decodedData < minPower):
        minPower = decodedData
    
    # print('index = ', index)
    # int_index = ''.join(x for x in str(index) if x.isdigit())
    # int_index = int(int_index)
    # print(int_index)
    
    index_time = next(index)
   
    # add a value to the x-axis (simulating time)
    timeAxis.append(index_time/5) # divided by 5 for 0.2s data cycle
    # add the power read from the arduino to the y-axis if applicable
    powerAxis.append(decodedData)
    string = ''
    if collectingData == True and time.time() - startTime <= collectionDuration:
        if start_save_data_time == 0:
            start_save_data_time = index_time/5
            # print('*', start_save_data_time)
        specifiedIntervalTimeAxis.append(next(specifiedIntervalIndex)/5)
        specifiedIntervalPowerAxis.append(decodedData)
        
        ## functions for 
        index_str = str(index)
        index_new = ''
        for i in index_str:
            if i.isdigit():
                index_new += i
                
        string = str(str(round((index_time/5 - start_save_data_time), 1))) + ", " + str(decodedData)
        
        savedata(string)
        # print(collectionDuration)
        # print(time.time() - startTime)
        
        
    print(str(index_time/5) + "s, " + str(decodedData) + "mW")
    
    axs[0].cla()
    axs[1].cla()
    axs[0].set(xlabel = "Time (s)", ylabel = "Power (mW)")
    axs[1].set(xlabel = "Time (s)", ylabel = "Power (mW)")
    axs[0].set_title("Power vs Time")
    axs[1].set_title("Power vs Time (Specified Interval)")
    axs[0].text(0, 2.58, "Max Power: {}\nMin Power: {}".format(maxPower, minPower), bbox=dict(facecolor="red", alpha=0.5))
    axs[1].text(0, 2.58, "Max Power: {}\nMin Power: {}".format(maxPower, minPower), bbox=dict(facecolor="red", alpha=0.5))

    # line graph
    axs[0].plot(timeAxis, powerAxis)
    axs[1].plot(specifiedIntervalTimeAxis, specifiedIntervalPowerAxis)

    # # bar graph
    # axs[0].bar(timeAxis, powerAxis)
    # axs[1].bar(specifiedIntervalTimeAxis, specifiedIntervalPowerAxis)

    # # scatter plot
    # axs[0].scatter(timeAxis, powerAxis)
    # axs[1].scatter(specifiedIntervalTimeAxis, specifiedIntervalPowerAxis)
    
def savedata(str):
    today = date.today()
    d1 = today.strftime("%Y%m%d")
    filename = d1 + '-Test-' + '.txt'
    
    with open(filename, 'a') as f:
        f.write(str + '\n')

# graph of live values (the interval variable is the period of data collection in milliseconds)
graph = FuncAnimation(plt.gcf(), writeData, interval = 200)
plt.tight_layout()
plt.show()