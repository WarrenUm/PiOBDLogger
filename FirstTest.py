#make sure pi is paired and connected OBDII bt

import obd
from obd import OBDStatus
import csv
from datetime import datetime
from datetime import date
from callBackFunctions import *
from logFunctions import *

obd.logger.setLevel(obd.logging.DEBUG)

speed = 0
rpm = 0
intake_temp = 0
maf = 0
load = 0
fuel_rail_press = 0
afr = 0
o2_trim = 0
timing_advance = 0
timestamp = datetime.now()
logFilename = "data_logging_" + str(date.today()) + ".csv"

carConnected = False
connection = obd.Async(fast=False)
print('Waiting for Connection...')
while carConnected == False:
    connection = obd.Async(fast=False)
    carConnected = obd.Async.is_connected()

print('Connection Established')


setupLogFile(logFilename)

def ecu_connections():
    connection.watch(obd.commands.SPEED, callback=get_speed)
    connection.watch(obd.commands.RPM, callback=get_rpm)
    connection.watch(obd.commands.ENGINE_LOAD, callback=get_load)
    connection.watch(obd.commands.GET_DTC, callback=get_dtc)
    connection.watch(obd.commands.COOLANT_TEMP, callback=get_coolant_temp)
    connection.watch(obd.commands.INTAKE_TEMP, callback=get_intake_temp)
    connection.watch(obd.commands.FUEL_RAIL_PRESSURE_DIRECT, callback=get_fuel_rail_press)
    connection.watch(obd.commands.COMMANDED_EQUIV_RATIO, callback=get_afr)
    connection.watch(obd.commands.MAF, callback=get_maf)
    connection.watch(obd.commands.TIMING_ADVANCE, callback=get_timing_a)
    connection.watch(obd.commands.LONG_O2_TRIM_B1, callback=get_o2)

    connection.start()


# Turn off debug mode
obd.logger.removeHandler(obd.console_handler)
ecu_connections()
run = True
logging = True
while run:
    if logging:
        print(rpm)
        log_to_file(logFilename)