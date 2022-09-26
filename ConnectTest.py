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
collectionDuration = 40 # the system has a few second delay, to record 30s, write 40~
minPower = 100000
maxPower = -100000
startTime = 0
fig, axs = plt.subplots(2, 1)

def writeData(i):
    global collectingData
    global startTime
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

    # add a value to the x-axis (simulating time)
    timeAxis.append(next(index))
    # add the power read from the arduino to the y-axis if applicable
    powerAxis.append(decodedData)
    string = ''
    if collectingData == True and time.time() - startTime <= collectionDuration:
        specifiedIntervalTimeAxis.append(next(specifiedIntervalIndex))
        specifiedIntervalPowerAxis.append(decodedData)
        
        index_str = str(index)
        index_new = ''
        for i in index_str:
            if i.isdigit():
                index_new += i
                
        string = index_new + ", " + str(decodedData)
        
        savedata(string)
        print(collectionDuration)
        print(time.time() - startTime)
        
        
    print(str(index) + "s, " + str(decodedData) + "mW")
    # with open('20220926-Test-0001.txt', 'w') as f:
    #     f.write('Time Power\n')
    #     f.write(str(index) + "s, " + str(decodedData) + "mW\n")
    
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
graph = FuncAnimation(plt.gcf(), writeData, interval = 1000)
plt.tight_layout()
plt.show()