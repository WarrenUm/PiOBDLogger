#make sure pi is paired and connected OBDII bt

import obd
from obd import OBDStatus
import csv
from datetime import datetime
from datetime import date
from callBackFunctions import *

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
coolant_temp = 0
timestamp = datetime.now()
global logFilename 
logFilename  = "data_logging_" + str(date.today()) + ".csv"

def setupLogFile(fileName):
    
    header = ['TIME','SPEED','RPM', 'Intake Temp.', 'MAF (g/s)', 'Engine Load', 'Fuel Rail Press.', 'AFR', 'Long B2 Trim', 'Timing Adv.','Coolant Temp.']
    with open(fileName, "w", newline="") as dl:
        writer = csv.writer(dl)
        writer.writerow(header)


def log_to_file():
    timestamp = datetime.now()
    row = [str(timestamp),str(speed), str(rpm), str(intake_temp), str(maf), str(load), str(fuel_rail_press), str(afr), str(o2_trim), str(timing_advance), str(coolant_temp)]
    with open(logFilename, "a", newline="") as dl:
        writer = csv.writer(dl)
        writer.writerow(row)

carConnected = False
connection = obd.Async(fast=False)
while len(connection.supported_commands) < 100:
    connection = obd.Async(fast=False)

print('Connection Established')


setupLogFile(logFilename)

def ecu_connections():
    connection.watch(obd.commands.SPEED, callback=[get_speed,log_to_file])
    connection.watch(obd.commands.RPM, callback=[get_rpm,log_to_file])
    connection.watch(obd.commands.ENGINE_LOAD, callback=[get_load,log_to_file])
    connection.watch(obd.commands.GET_DTC, callback=get_dtc)
    connection.watch(obd.commands.COOLANT_TEMP, callback=[get_coolant_temp,log_to_file])
    connection.watch(obd.commands.INTAKE_TEMP, callback=[get_intake_temp,log_to_file])
    connection.watch(obd.commands.FUEL_RAIL_PRESSURE_DIRECT, callback=[get_fuel_rail_press,log_to_file])
    connection.watch(obd.commands.COMMANDED_EQUIV_RATIO, callback=[get_afr,log_to_file])
    connection.watch(obd.commands.MAF, callback=[get_maf,log_to_file])
    connection.watch(obd.commands.TIMING_ADVANCE, callback=[get_timing_a,log_to_file])
    connection.watch(obd.commands.LONG_O2_TRIM_B1, callback=[get_o2,log_to_file])

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