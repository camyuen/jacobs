#!/usr/bin/env python
from std_msgs.msg import Float32
from std_srvs.srv import * 
#from std_msgs.msg import Float32MultiArray
import rospy
import pexpect
import time
import os


def pulldata():

    import pexpect
    import time



    DEVICE = "54:6C:0E:B2:FA:84"

    print("Digiscan address:"),
    print(DEVICE)

    


    # Run gatttool interactively.
    print("Run gatttool...")
    child = pexpect.spawn("gatttool -I")
    child.sendline("sudo systemtl restart bluetooth")
    child.expect('.*')
    child.sendline("sudo hciconfig hci0 up")
    child.expect('.*')
    time.sleep(1)
    #os.system('sudo systemctl restart bluetooth')
    #os.system('sudo hciconfig hci0 up')  
    
# Connect to the device.
    print("Connecting to "),
    print(DEVICE),
    time.sleep(0.3)
    child.sendline("connect {0}".format(DEVICE))
    time.sleep(0.3)
    child.expect("Connection successful", timeout=None)
    print(" Connected!")

    # function to transform hex string like "0a cd" into signed integer
   # def hexStrToInt(hexstr):
   #     val = int(hexstr[0:2],16) + (int(hexstr[3:5],16)<<8)
   #     if ((val&0x8000)==0x8000): # treat signed 16bits
   #         val = -((val^0xffff)+1)
   #     return val


    # Digiscan

    child.sendline("char-write-cmd 27 01")      #enable sensors
    time.sleep(0.5)
    #child.expect("", timeout=None)
    time.sleep(0.5)
    child.sendline("char-read-hnd 24")            
    time.sleep(1)
    child.expect("Characteristic value/descriptor: ", timeout=None)
    print("fuck")
    #if (child.before == ):
    child.expect("\r\n", timeout=None)
        
    #data = 69
    #data = float(hexStrToInt(child.before[0:5])-1983.0)
    data = [float(hexStrToInt(child.before[0:5])-1983), float(hexStrToInt(child.before[12:17])-1983), float(hexStrToInt(child.before[24:29])-1983), float(hexStrToInt(child.before[36:41])-1983)] 
    #print val
    print("got past data")    
    child.sendline("disconnect")
    child.expect("\r\n", timeout=None)
    child.expect(" Invalid file descriptor.\r\n", timeout=None)
    child.expect("\r\n", timeout=None)
    child.sendline("exit")
    child.expect("\r\n", timeout=None)
    print data                                   
    return data

    # function to transform hex string like "0a cd" into signed integer
def hexStrToInt(hexstr):
	global val
	val = int(hexstr[0:2],16) + int(hexstr[3:5],16)
        if ((val&0x8000)==0x8000): # treat signed 16bits
        	val = -((val^0xffff)+1)
        return val



def handle_collect_data():
   # print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
   # return AddTwoIntsResponse(req.a + req.b)
	global data0
	global data1
	global data2
	global data3
	global data4
	data = pulldata()
	data1 = float(data[0])
	data2 = float(data[1])
	data3 = float(data[2])
	data4 = float(data[3])
	return data #WidaqDataResponse(array)
	return data1
	return data2
	return data3
	return data4
def widaq_data_server():
    rospy.init_node('widaq_data_server')
    s = rospy.Service('widaq_data',Empty, handle_collect_data())
    print "Ready to lick my nuts"
    pub=rospy.Publisher('Data1', Float32, queue_size=1)
    pub=rospy.Publisher('Data2', Float32, queue_size=1)
    pub=rospy.Publisher('Data3', Float32, queue_size=1)
    pub=rospy.Publisher('Data4', Float32, queue_size=1)

    rate=rospy.Rate(10)
    #rospy.spin()
    pub.publish(data1)
    pub.publish(data2)
    pub.publish(data3)
    pub.publish(data4)

    rate.sleep()	
if __name__ == "__main__":
    	widaq_data_server()

