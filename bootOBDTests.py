import obd

roundDigits = 1
fuelCapGallons = 15.6
mpg = 24

obd.logger.setLevel(obd.logging.DEBUG)

connection = obd.OBD(fast=False)
while len(connection.supported_commands) < 100:
    connection = obd.OBD(fast=False)

print('Connection Established')
print('Gathering Vehicle Information')

vin = connection.query(obd.commands.VIN)
print(f'Vin #: {vin}')

fuelStatus = connection.query(obd.commands.FUEL_STATUS)[0]
print(f'Fuel Status: {fuelStatus}')

fuelType = connection.query(obd.commands.FUEL_TYPE)
print('Fuel Type: {fuelType}')

ethanolPercent = connection.query(obd.commands.ETHANOL_PERCENT).value.magnitude
print(f'Fuel Contains {ethanolPercent} Percent Ethanol')

fuelLevel = connection.query(obd.commands.FUEL_LEVEL).value.magnitude
print(f'Fuel Tank At {fuelLevel}%')

approximateGallonsLeft = round(((fuelLevel/100) * fuelCapGallons),roundDigits)
distanceRemaining = mpg * approximateGallonsLeft
print(f'You Have About {approximateGallonsLeft} Gallons Remaining And Can Drive Approximately {distanceRemaining}')