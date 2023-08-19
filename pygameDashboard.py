import obd
from pygame.locals import *
import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.mouse.set_visible(False)

def draw_screen():
    
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, pygame.Rect(5, 5, 150, 150), 2)
    pygame.draw.rect(screen, WHITE, pygame.Rect(270, 5, 150, 150), 2)
    pygame.draw.rect(screen, WHITE, pygame.Rect(155, 100, 115, 115), 2)
    
    vinF = pygame.font.SysFont(None, 50)
    vinText = vinF.render("Vin", True, WHITE)
    screen.blit(vinText, (15, 160))
     
    fuelStatusF = pygame.font.SysFont(None, 50)
    fuelStatusText = fuelStatusF.render("Fuel Status", True, WHITE)
    screen.blit(fuelStatusText, (310, 160))
    
    ethanolPercentF = pygame.font.SysFont(None, 50)
    fuelPercentText = ethanolPercentF.render("Ethanol Percent", True, WHITE)
    screen.blit(fuelPercentText, (175, 60))

running =  True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.display.quit()
                pygame.quit()
    
    draw_screen()
   
    vinFont = pygame.font.SysFont(None, 50)
    vinTxt = vinFont.render(str(vin), True, WHITE)
    
    fuelStatusFont = pygame.font.SysFont(None, 75)
    fuelStatusTxt = fuelStatusFont.render(str(fuelStatus), True, WHITE)
    
    ethanolPercentFont = pygame.font.SysFont(None, 75)
    ethanolPercentTxt = ethanolPercentFont.render(str(ethanolPercent) + "%", True, WHITE)
    
    screen.blit(vinTxt, (22, 50))

    screen.blit(fuelStatusTxt, (285, 50))
    
    screen.blit(ethanolPercentTxt, (172, 130))
    
    pygame.display.update()
    pygame.display.flip()
    
pygame.quit()