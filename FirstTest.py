#make sure pi is paired and connected OBDII bt

import obd
from obd import OBDStatus
import csv
from datetime import datetime
from datetime import date
import time

obd.logger.setLevel(obd.logging.DEBUG)

def get_speed(s):
    global speed
    if not s.is_null():
        speed = float(s.value.magnitude) #for kph
        # speed = int(s.value.magnitude * .060934)  # for mph


def get_fuel_rail_press(fp):
    global fuel_rail_press
    if not fp.is_null():
        fuel_rail_press = float(fp.value.magnitude) * .145038  # kp to psi


def get_intake_temp(it):
    global intake_temp
    if not it.is_null():
        intake_temp = int(int(it.value.magnitude) * 1.8 + 32)  # C to F


def get_afr(af):
    global afr
    if not af.is_null():
        afr = float(af.value.magnitude) * 14.64 # Convert to AFR for normal gasoline engines


def get_rpm(r):
    global rpm
    if not r.is_null():
        rpm = int(r.value.magnitude)


def get_load(l):
    global load
    if not l.is_null():
        load = int(l.value.magnitude)


def get_coolant_temp(ct):
    global coolant_temp
    if not ct.is_null():
        coolant_temp = int(int(ct.value.magnitude) * 1.8 + 32) # convert to F


def get_intake_press(ip):
    global intake_pressure
    if not ip.is_null():
        intake_pressure = float(ip.value.magnitude)


def get_baro_press(bp):
    global baro_pressure
    if not bp.is_null():
        baro_pressure = float(bp.value.magnitude)


def get_dtc(c):
    global codes
    if not c.is_null():
        codes = c.value


def get_timing_a(ta):
    global timing_advance
    if not ta.is_null():
        timing_advance = str(ta.value).replace("degree", "") # in degrees / remove text from val
        timing_advance = float(timing_advance)


def get_maf(m):
    global maf
    if not m.is_null():
        maf = str(m.value).replace("gps", "")  # grams / second / remove text from val
        maf = float(maf)


def get_o2(o):
    global o2_trim
    if not o.is_null():
        o2_trim = str(o.value).replace("percent", "")  # +/- 3 percent normal range - negative = rich, positive = lean
        o2_trim = float(o2_trim)


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
        log_to_file()
        time.sleep(0.25)
