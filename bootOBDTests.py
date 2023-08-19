import obd

roundDigits = 3
fuelCapGallons = 15.6
mpg = 24

# obd.logger.setLevel(obd.logging.DEBUG)

connection = obd.OBD(fast=False)
while len(connection.supported_commands) < 100:
    connection = obd.OBD(fast=False)

print('Connection Established')
print('Gathering Vehicle Information')

vin = connection.query(obd.commands.VIN).value
print(f'Vin #: {vin}')

fuelStatus = connection.query(obd.commands.FUEL_STATUS).value[0]
print(f'Fuel Status: {fuelStatus}')

fuelType = connection.query(obd.commands.FUEL_TYPE).value
print(f'Fuel Type: {fuelType}')

ethanolPercent = round(connection.query(obd.commands.ETHANOL_PERCENT).value.magnitude,roundDigits)
print(f'Fuel Contains {ethanolPercent} Percent Ethanol')

fuelLevel = round(connection.query(obd.commands.FUEL_LEVEL).value.magnitude,roundDigits)
print(f'Fuel Tank At {fuelLevel}%')

approximateGallonsLeft = round(((fuelLevel/100) * fuelCapGallons),roundDigits)
distanceRemaining = round((mpg * approximateGallonsLeft),roundDigits)
print(f'You Have About {approximateGallonsLeft} Gallons Remaining And Can Drive Approximately {distanceRemaining} Miles')
