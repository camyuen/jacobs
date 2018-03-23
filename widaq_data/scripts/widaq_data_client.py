#!/usr/bin/env python

import sys
import rospy
from std_srvs.srv import *

def widaq_data_client():
    rospy.wait_for_service('widaq_data')
    try:
        widaq_data_array = rospy.ServiceProxy('widaq_data', Empty)
        array = widaq_data_array()
        return array.widaq_array 
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    #if len(sys.argv) == 3:
     #   x = int(sys.argv[1])
     #   y = int(sys.argv[2])
   # else:
    #    print usage()
     #   sys.exit(1)
   # print "Requesting %s+%s"%(x, y)
   # print "%s + %s = %s"%(x, y, add_two_ints_client(x, y))

	
	print "s%"%(widaq_data_client())
