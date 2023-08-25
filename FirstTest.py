#make sure pi is paired and connected OBDII bt

import obd
from obd import OBDStatus
import csv
from datetime import datetime
from datetime import date
import time

global roundDigits
roundDigits = 1

obd.logger.setLevel(obd.logging.DEBUG)

def getMeasure(measure):
    return round(float(measure),roundDigits)

def trimPercent(percentInput):
    return getMeasure(str(percentInput).replace("percent",""))

def trimDegree(degreeInput):
    return getMeasure(str(degreeInput).replace("degree",""))

def toFahrenheit(celciusInput):
    return getMeasure((float(celciusInput) * 1.8) + 32)

def trimUnit(measure,unitString):
    return getMeasure(str(measure).replace(unitString,""))

def kpToPsi(inputKp):
    return getMeasure(float(inputKp) * 0.145038)

def kphToMph(inputKph):
    return getMeasure(float(inputKph))


def get_speed(s):
    global speed
    if not s.is_null():
        speed = getMeasure(s.value.magnitude) #for kph
        # speed = kphToMph(s.value.magnitude)  # for mph
def get_fuel_rail_press(fp):
    global fuel_rail_press
    if not fp.is_null():
        fuel_rail_press = kpToPsi(fp.value.magnitude)  # kp to psi
def get_intake_temp(it):
    global intake_temp
    if not it.is_null():
        intake_temp = toFahrenheit(it.value.magnitude) # C to F
def get_afr(af):
    global afr
    if not af.is_null():
        afr = float(af.value.magnitude) * 14.64 # Convert to AFR for normal gasoline engines
def get_rpm(r):
    global rpm
    if not r.is_null():
        rpm = getMeasure(r.value.magnitude)
def get_load(l):
    global load
    if not l.is_null():
        load = getMeasure(l.value.magnitude)
def get_coolant_temp(ct):
    global coolant_temp
    if not ct.is_null():
        coolant_temp = toFahrenheit(ct.value.magnitude) # convert to F
def get_intake_press(ip):
    global intake_pressure
    if not ip.is_null():
        intake_pressure = getMeasure(ip.value.magnitude)
def get_baro_press(bp):
    global baro_pressure
    if not bp.is_null():
        baro_pressure = getMeasure(bp.value.magnitude)
def get_dtc(c):
    global codes
    if not c.is_null():
        codes = c.value
def get_timing_a(ta):
    global timing_advance
    if not ta.is_null():
        timing_advance = trimDegree(ta.value) # in degrees / remove text from val
def get_maf(m):
    global maf
    if not m.is_null():
        maf = trimUnit(m.value,"gps")  # grams / second / remove text from val
def get_o2(o):
    global o2_trim
    if not o.is_null():
        o2_trim = trimPercent(o.value)  # +/- 3 percent normal range - negative = rich, positive = lean

def getShortFuelTrim_1(shortFuelTrim_1Callback):
    global shortFuelTrim_1
    if not shortFuelTrim_1Callback.is_null():
        shortFuelTrim_1 = trimPercent(shortFuelTrim_1Callback.value)

def getCalibrationId(calibrationIdCallback):
    #test return value
    global calibrationId
    if not calibrationIdCallback.is_null():
        calibrationId = str(calibrationIdCallback.value)

def getCatalystTemp_B1S1(catalystTemp_B1S1Callback):
    global catalystTemp_B1S1
    if not catalystTemp_B1S1Callback.is_null():
        catalystTemp_B1S1 = toFahrenheit(catalystTemp_B1S1Callback.value.magnitude)

def getControlModuleVoltage(controlModuleVoltageCallback):
    global controlModuleVoltage
    if not controlModuleVoltageCallback.is_null():
        controlModuleVoltage = getMeasure(controlModuleVoltageCallback.value.magnitude)

def getObdCompliance(obdComplianceCallback):
    global obdCompliance
    if not obdComplianceCallback.is_null():
        obdCompliance = str(obdComplianceCallback.value)

def getThrottlePosition(throttlePositionCallback):
    global throttlePosition
    if not throttlePositionCallback.is_null():
        throttlePosition = trimPercent(throttlePositionCallback.value)

def getO2_B1S1(o2_B1S1Callback):
    global o2_B1S1
    if not o2_B1S1Callback.is_null():
        o2_B1S1 = getMeasure(o2_B1S1Callback.value.magnitude)

def getAcceleratorPositionE(acceleratorPositionECallback):
    global acceleratorPositionE
    if not acceleratorPositionECallback.is_null():
        acceleratorPositionE = trimPercent(acceleratorPositionECallback.value)

def getEngineRuntime(engineRuntimeCallback):
    global engineRuntime
    if not engineRuntimeCallback.is_null():
        engineRuntime = getMeasure(engineRuntimeCallback.value.magnitude)

def getCommandedEquivalenceRatio(commandedEquivalenceRatioCallback):
    global commandedEquivalenceRatio
    if not commandedEquivalenceRatioCallback.is_null():
        commandedEquivalenceRatio = getMeasure(commandedEquivalenceRatioCallback.value.magnitude)

def getO2_B1S2(o2_B1S2Callback):
    global o2_B1S2
    if not o2_B1S2Callback.is_null():
        o2_B1S2 = getMeasure(o2_B1S2Callback.value.magnitude)

def getRelativeThrottlePosition(relativeThrottlePositionCallback):
    global relativeThrottlePosition
    if not relativeThrottlePositionCallback.is_null():
        relativeThrottlePosition = trimPercent(relativeThrottlePositionCallback.value)

def getElmVoltage(elmVoltageCallback):
    global elmVoltage
    if not elmVoltageCallback.is_null():
        elmVoltage = getMeasure(elmVoltageCallback.value.magnitude)

def getAcceleratorPositionD(acceleratorPositionDCallback):
    global acceleratorPositionD
    if not acceleratorPositionDCallback.is_null():
        acceleratorPositionD = trimPercent(acceleratorPositionDCallback.value)

def getCommandedEvaporativePurge(commandedEvaporativePurgeCallback):
    global commandedEvaporativePurge
    if not commandedEvaporativePurgeCallback.is_null():
        commandedEvaporativePurge = trimPercent(commandedEvaporativePurgeCallback.value)

def getFuelPressure(fuelPressureCallback):
    global fuelPressure
    if not fuelPressureCallback.is_null():
        fuelPressure = kpToPsi(fuelPressureCallback.value.magnitude)

def getLongFuelTrim_1(longFuelTrim_1Callback):
    global longFuelTrim_1
    if not longFuelTrim_1Callback.is_null():
        longFuelTrim_1 = trimPercent(longFuelTrim_1Callback.value)

def getCommandedThrottleActuator(commandedThrottleActuatorCallback):
    global commandedThrottleActuator
    if not commandedThrottleActuatorCallback.is_null():
        commandedThrottleActuator = trimPercent(commandedThrottleActuatorCallback.value)

def getFuelLevel(fuelLevelCallback):
    global fuelLevel
    if not fuelLevelCallback.is_null():
        fuelLevel = trimPercent(fuelLevelCallback.value)

def getThrottlePosition_B(throttlePosition_BCallback):
    global throttlePosition_B
    if not throttlePosition_BCallback.is_null():
        throttlePosition_B = trimPercent(throttlePosition_BCallback.value)

def getAbsoluteLoad(absoluteLoadCallback):
    global absoluteLoad
    if not absoluteLoadCallback.is_null():
        absoluteLoad = trimPercent(absoluteLoadCallback.value)

def getAmbientAirTemperature(ambientAirTemperatureCallback):
    global ambientAirTemperature
    if not ambientAirTemperatureCallback.is_null():
        ambientAirTemperature = toFahrenheit(ambientAirTemperatureCallback.value.magnitude)

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
    connection.watch(obd.commands.SHORT_FUEL_TRIM_1, callback=getShortFuelTrim_1)

    connection.start()


# Turn off debug mode
obd.logger.removeHandler(obd.console_handler)
ecu_connections()
run = True
logging = True
lastRun = time.monotonic()
while run:
    currentRun = time.monotonic()
        if currentRun - lastRun >= 1:
        if logging:
            log_to_file()
