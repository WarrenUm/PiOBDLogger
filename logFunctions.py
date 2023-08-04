import csv

def setupLogFile(fileName):
    
    header = ['TIME','SPEED','RPM', 'Intake Temp.', 'MAF (g/s)', 'Engine Load', 'Fuel Rail Press.', 'AFR', 'Long B2 Trim', 'Timing Adv.']
    with open(fileName, "w", newline="") as dl:
        writer = csv.writer(dl)
        writer.writerow(header)


def log_to_file(fileName):
    timestamp = datetime.now()
    row = [str(speed), str(rpm), str(intake_temp), str(maf), str(load), str(fuel_rail_press), str(afr), str(o2_trim), str(timing_advance)]
    with open(fileName, "a", newline="") as dl:
        writer = csv.writer(dl)
        writer.writerow(row)