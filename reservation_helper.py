#!/usr/bin/env python

##############################################################################
## Program :   reservation_helper.py                                        ##
## Author  :   Tyler Bartlett                                               ##
## Github  :   https://github.com/tylerbartlett/aws_reservation_helper      ##
##############################################################################

"""
Exports a csv file that contains how many on demand instances you are running minus the number of reservations by instance type

Usage:
    chef_on PLATFORM-ENVIRONMENT_REGION
    python reservation_helper.py
"""

import csv
import os
import subprocess
import sys
try:
    import transposer
except ImportError:
    print 'Cannot import transposer...'
    print 'Install transposer with \'pip install transposer\''
    sys.exit()

reservations_needed = {}

instance_types = [
"c3.large", "c3.xlarge", "c3.2xlarge", "c3.4xlarge", "c3.8xlarge",
"d2.xlarge", "d2.2xlarge", "d2.4xlarge", "d2.8xlarge",
"f1.2xlarge", "f1.16xlarge",
"g2.2xlarge", "g2.8xlarge",
"i2.xlarge", "i2.2xlarge", "i2.4xlarge", "i2.8xlarge",
"m3.medium", "m3.large", "m3.xlarge", "m3.2xlarge",
"m4.large", "m4.xlarge", "m4.2xlarge", "m4.4xlarge", "m4.10xlarge", "m4.16xlarge",
"p2.xlarge", "p2.8xlarge", "p2.16xlarge",
"r3.large", "r3.xlarge", "r3.2xlarge", "r3.4xlarge", "r3.8xlarge",
"r4.large", "r4.xlarge", "r4.2xlarge", "r4.4xlarge", "r4.8xlarge", "r4.16xlarge",
"t2.nano", "t2.micro", "t2.small" "t2.medium", "t2.large", "t2.xlarge", "t2.2xlarge",
"x1.16xlarge", "x1.32xlarge" ]

print "Looking up Total Instances and Reservations via AWS CLI"
for instance in instance_types:
    total_command = "aws ec2 describe-instances --filters \"Name=instance-state-name,Values=running\" | grep %s | wc -l" % (instance)
    total = subprocess.check_output(total_command, shell=True)
    reservations_command = "aws ec2 describe-reserved-instances --filters \"Name=instance-type,Values=%s\" \"Name=state,Values=active,payment-pending,payment-failed\" | cut -f7 -d$\'\\t\' | awk \'{total += $1}END{ print total}\'" % (instance)
    reservations = subprocess.check_output(reservations_command, shell=True)
    try:
        int(total)
    except ValueError:
        total = 0
    try:
         int(reservations)
    except ValueError:
        reservations = 0
    themath = int(total) - int(reservations)
    if themath != 0:
        reservations_needed.update({instance:themath})
        print ".",
    else:
        print ".",
        continue

pwd = os.environ['PWD']
print ""
print "Creating csv file in %s named reservations_needed.csv" % (pwd)

with open('reservations_needed.csv', 'wb') as f:
    w = csv.DictWriter(f, reservations_needed.keys())
    w.writeheader()
    w.writerow(reservations_needed)

transposer.transpose(i='reservations_needed.csv', o='reservations_needed.csv')
