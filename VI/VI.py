import pygame
import sys
from decimal import *
import os
pygame.init()

screen = pygame.display.set_mode((1080,720))

pygame.display.set_caption("Velocity Incremental")

#所有变量绝对不要加s ! ! ! 防止一些莫名其妙的错误 ! ! !
clock = pygame.time.Clock()
dt = 20

getcontext().prec = 8
getcontext().traps[InvalidOperation] = False

Precision = Decimal('0.01')
ActualPrecision = Decimal('0.0001')

def Judge_positionInArea(targetx,targety,areax1,areay1,areax2,areay2):
    if (areax1 <= targetx and targetx <= areax2 and areay1 <= targety and targety <= areay2):
        return True
    else:
        return False

#保存存档
def save_formattext(text):
    return str(text) + '\n'
def save():
    lines = [save_formattext(game_main_energy), save_formattext(game_main_energy_increase),save_formattext(game_main_velocity), save_formattext(game_main_acceleratorAmount), save_formattext(game_main_boosterAmount), save_formattext(game_main_chargerAmount), save_formattext(game_main_duplicatorAmount), save_formattext(game_energization_layerisUnlocked), save_formattext(game_energization_energyParticle), save_formattext(game_energization_energizerAmount), save_formattext(game_energization_frequency), save_formattext(game_energization_upgrade[0]), save_formattext(game_energization_upgrade[1]), save_formattext(game_energization_upgrade[2]), save_formattext(game_energization_upgrade[3]), save_formattext(game_energization_upgrade[4]), save_formattext(game_energization_upgrade[5]), save_formattext(game_planet[1].status), save_formattext(game_planet[2].status), save_formattext(game_planet[3].status), save_formattext(game_light_layerisUnlocked), save_formattext(game_light_lightPower)]
    with open('saves\SaveFile.txt', 'w') as f:
        f.writelines(lines)

def str2bool(x):
    if x == "True":
        return True
    elif x == "False":
        return False
    else:
        print("Error")
        return True

class Planet():
    def __init__(self, id, x, y, cost, status=0):
        self.id = id
        self.pos = (x, y)
        self.cost = cost
        self.status = status
    def shown(self):
        if (self.id == 0):
            return False
        if (self.id == 11):
            return True
        if (self.id == 21 or self.id == 22):
            if game_planet[1].status == 1:
                return True
            else:
                return False
    def effect(self):
        if (self.id == 0):
            print("Hey? You!")
        if (self.id == 11):
            if self.status == 1:
                return Decimal('1')+game_energization_energyParticle**Decimal('0.5')
            else:
                return Decimal('1')
    def description(self):
        if (self.id == 0):
            return "You must be cheating..."
        if (self.id == 11):
            return "[P1-1] Effect: Your Energy Particles boost Energy Production. Cost: 10000 Energy Particles."
        if (self.id == 21):
            return "P[2-1] Effect: Unlock Light permanently. Cost: 114514 Energy Particles."
        if (self.id == 22):
            return "P[2-2] TBD"

#游戏的常量
EnergizationUpgradeCost = [0, Decimal('10.0'), Decimal('100.0'), Decimal('11200'), Decimal('1e6')]
SubtabofTab = {"main":1, "energization":2}
totalPlanets = 4
#游戏主体部分的变量
game_tabStatus = "main"
game_subtabStatus = 1
game_main_energy = Decimal('1.0')
game_main_energy_increase = Decimal()
game_main_velocity = Decimal()
game_main_acceleratorAmount = Decimal()
game_main_boosterAmount = Decimal()
game_main_chargerAmount = Decimal()
game_main_duplicatorAmount = Decimal()

#E层
game_energization_layerisUnlocked = False
game_energization_energyParticle = Decimal()
game_energization_energizerAmount = Decimal()
game_energization_frequency = Decimal('1.0')
game_energization_upgrade = [5, False, False, False, False, False]
game_planet = [Planet(0, 0, 0, Decimal('1.0')), Planet(11, 220, 120, Decimal('10000')), Planet(21, 370, 120, Decimal('114514')), Planet(22, 220, 270, Decimal('19198100'))]

#L层
game_light_layerisUnlocked = False
game_light_lightPower = Decimal('0')
#图片部分的变量

image_Tab = pygame.image.load(r'资源\Tabs.png')
image_Velocity = pygame.image.load(r'资源\Velocity.png')
image_Sound = pygame.image.load(r'资源\Layer_Sound.png')
image_Light = pygame.image.load(r'资源\Layer_Light.png')
image_Accelerator = pygame.image.load(r'资源\Accelerator.png')
image_Booster = pygame.image.load(r'资源\Booster.png')
image_Charger = pygame.image.load(r'资源\Charger.png')
image_Duplicator = pygame.image.load(r'资源\Duplicator.png')
image_EnergizeReset = pygame.image.load(r'资源\EnergizeReset.png')
image_Energizer = pygame.image.load(r'资源\Energizer.png')
image_EnergizationUpgrade = pygame.image.load(r'资源\Upgrades\EU.png')
image_EnergizationUpgradeBought = pygame.image.load(r'资源\Upgrades\EUBought.png')
image_Space = pygame.image.load(r'资源\Space.png')
image_Planets = [pygame.image.load(r"资源\Planet\0.png"), pygame.image.load(r"资源\Planet\1.png"), pygame.image.load(r"资源\Planet\2.png")]

def Tick():
    global game_energization_layerisUnlocked
    global game_main_energy
    global game_main_energy_increase
    global game_main_velocity
    global game_energization_frequency
    global game_light_layerisUnlocked
    global game_light_lightPower
    game_main_energy_increase = (getEnergyProduction()/getResist()).normalize()
    game_main_energy_increase = game_main_energy_increase * getEnergizationUpgradeEffect(1)
    game_main_energy = (game_main_energy+game_main_energy_increase/Decimal(str(dt)))
    game_main_velocity = (game_main_energy ** Decimal('0.5'))
    game_energization_frequency = game_energization_frequency + ((Decimal.__pow__(Decimal('1.5'), game_energization_energizerAmount.normalize())-Decimal('1'))/Decimal(str(dt)))
    if game_main_velocity.compare(Decimal('340')) == Decimal('1'):
        game_energization_layerisUnlocked = True
    if game_planet[2].status == 1:
        game_light_layerisUnlocked = True
    game_light_lightPower = max(game_light_lightPower, getLightPowerGain())

def Display(currentTab, currentsubTab):
    screen.blit(image_Tab,(0,0))
    screen.blit(image_Velocity,(10,10))
    if game_energization_layerisUnlocked == True:
        screen.blit(image_Sound,(10,100))
        screen.blit(pygame.font.Font(None, 40).render(str(game_energization_energyParticle), True, (255,255,255)), (95,130))
    if game_light_layerisUnlocked == True:
        screen.blit(image_Light, (10, 190))
    if currentTab == "main":
        screen.blit(pygame.font.Font(None, 50).render("Current Energy: " + str(game_main_energy) + " J ( + " + str(game_main_energy_increase) + " J/s )", True, (255,255,255)), (200,40))
        screen.blit(pygame.font.Font(None, 40).render("Translated to Velocity: " + str(game_main_velocity) + " m/s", True, (255,255,255)), (200,90))
        screen.blit(image_Accelerator, (240,190))
        screen.blit(pygame.font.Font(None, 40).render(str(game_main_acceleratorAmount) + " Accelerators, Cost: " + str(getAcceleratorCost()) + " J of Energy", True, (255,255,255)), (310,190))
        screen.blit(pygame.font.Font(None, 40).render("Effect: +" + str(getAcceleratorEffect()) + " J/s to Energy gain", True, (255,255,255)), (310,240))
        screen.blit(image_Booster, (240,320))
        screen.blit(pygame.font.Font(None, 40).render(str(game_main_boosterAmount) + " Boosters, Cost: " + str(getBoosterCost()) + " J of Energy", True, (255,255,255)), (310,320))
        screen.blit(pygame.font.Font(None, 40).render("Effect: ×" + str(getBoosterEffect()) + " to Accelerator effect", True, (255,255,255)), (310,370))
        screen.blit(image_Charger, (240,450))
        screen.blit(pygame.font.Font(None, 40).render(str(game_main_chargerAmount) + " Chargers, Cost: " + str(getChargerCost()) + " J of Energy", True, (255,255,255)), (310,450))
        screen.blit(pygame.font.Font(None, 40).render("Effect: ^" + str(getChargerEffect()) + " to Booster effect", True, (255,255,255)), (310,500))
        screen.blit(image_Duplicator, (240,580))
        screen.blit(pygame.font.Font(None, 40).render(str(game_main_duplicatorAmount) + " Duplicators, Cost: " + str(getDuplicatorCost()) + " J of Energy", True, (255,255,255)), (310,580))
        screen.blit(pygame.font.Font(None, 40).render("Effect: ×" + str(getDuplicatorEffect()) + " to Energy Production", True, (255,255,255)), (310,630))
    elif currentTab == "energization":
        if currentsubTab == 0:
            screen.blit(image_EnergizeReset,(230,40))
            screen.blit(pygame.font.Font(None, 40).render(str(getEnergyParticleGain()) + " Energy Particles on Energize", True, (63,63,255)), (310,150))
            screen.blit(image_Energizer, (240,190))
            screen.blit(pygame.font.Font(None, 40).render(str(game_energization_energizerAmount) + " Energizers, Cost: " + str(getEnergizerCost()) + " Energy Particles", True, (63,127,255)), (310,190))
            screen.blit(pygame.font.Font(None, 40).render("Effect: +" + str(((Decimal.__pow__(Decimal('1.50'), game_energization_energizerAmount.normalize()))-Decimal('1.0'))) + " Hz/s to Frequency gain", True, (63,127,255)), (310,240))
            screen.blit(pygame.font.Font(None, 40).render(str(game_energization_frequency) + " Hz of Frequency, Boosting Energy Gain by ×" + str(getFrequencyEffect()), True, (63,63,255)), (200,300))
            for i in range(1, game_energization_upgrade[0]+1):
                if game_energization_upgrade[i] == False:
                    screen.blit(image_EnergizationUpgrade, (230, 300+60*i))
                else:
                    screen.blit(image_EnergizationUpgradeBought, (230, 300+60*i))
            screen.blit(pygame.font.Font(None, 35).render('10EP', True, (63,63,255)), (246,386))
            screen.blit(pygame.font.Font(None, 60).render('You gain 3 times more Energy', True, (63,63,255)), (420,373))
            screen.blit(pygame.font.Font(None, 35).render('100EP', True, (63,63,255)), (246,446))
            screen.blit(pygame.font.Font(None, 60).render('Improve Duplicator effect', True, (63,63,255)), (420,433))
            screen.blit(pygame.font.Font(None, 25).render('11200 m/s', True, (63,63,255)), (241,511))
            screen.blit(pygame.font.Font(None, 40).render('Escape from the Earth, enter the Space', True, (63,63,255)), (435,493))
            screen.blit(pygame.font.Font(None, 35).render('1e6 EP', True, (63,63,255)), (246,566))
            screen.blit(pygame.font.Font(None, 60).render('Improve Frequency effect', True, (63,63,255)), (420,553))
        elif currentsubTab == 1:
            screen.blit(image_Space, (180, 0))
            for i in range(len(game_planet)):
                if game_planet[i].shown() == True:
                    screen.blit(image_Planets[game_planet[i].status], game_planet[i].pos)
                    if Judge_positionInArea(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], game_planet[i].pos[0], game_planet[i].pos[1], game_planet[i].pos[0]+50, game_planet[i].pos[1]+50):
                        screen.blit(pygame.font.Font(None,24).render(game_planet[i].description(), True, (191, 191, 255-game_planet[i].status*64)), (220, 40))
    elif currentTab == "light":
        if currentsubTab == 0:
            screen.blit(pygame.font.Font(None, 40).render("You have " + str(game_light_lightPower) + " Light Power, based on your highest Velocity. ", True, (63,63,255)), (220, 40))
            
def Reset(layer: str):
    global game_main_energy
    global game_main_energy_increase
    global game_main_velocity
    global game_main_acceleratorAmount
    global game_main_boosterAmount
    global game_main_chargerAmount
    global game_main_duplicatorAmount
    if (layer == "Energization" or layer == "E"):
        game_main_energy = Decimal('1.0')
        game_main_energy_increase = Decimal()
        game_main_velocity = Decimal()
        game_main_acceleratorAmount = Decimal()
        game_main_boosterAmount = Decimal()
        game_main_chargerAmount = Decimal()
        game_main_duplicatorAmount = Decimal()

#计算
def getAcceleratorCost(): 
    if (game_main_acceleratorAmount < 100): return Decimal.__pow__(Decimal('2'), game_main_acceleratorAmount)
def getBoosterCost(): 
    if (game_main_boosterAmount < 100): return (Decimal('1')+game_main_boosterAmount)*Decimal.__pow__(Decimal('3'), (game_main_boosterAmount+1))
def getChargerCost(): 
    if (game_main_chargerAmount < 50): return Decimal.__pow__(Decimal('4'), Decimal.__pow__(game_main_chargerAmount+Decimal('2.0'), Decimal('1.3')))
def getDuplicatorCost(): 
    if (game_main_duplicatorAmount < 100): return Decimal('5')**((game_main_duplicatorAmount+Decimal('2.0'))**Decimal('1.5'))
def getEnergizerCost():
    if (game_energization_energizerAmount < 5000): return Decimal.__pow__(Decimal('2'), game_energization_energizerAmount)

def getEnergyProduction():
    return getAcceleratorEffect()*getDuplicatorEffect()*getFrequencyEffect()*game_planet[1].effect()

def getAcceleratorEffect():
    return game_main_acceleratorAmount*getBoosterEffect()
def getBoosterEffect():
    return (game_main_boosterAmount+Decimal('1.0'))**getChargerEffect()
def getChargerEffect():
    return game_main_chargerAmount*Decimal('0.25')+Decimal('1.0')
def getDuplicatorEffect():
    return Decimal.__pow__(game_main_duplicatorAmount+getEnergizationUpgradeEffect(2)-Decimal('1'), Decimal('1.0')+getEnergizationUpgradeEffect(2))+Decimal('1.0')

def getFrequencyEffect():
    return (Decimal('2')+getEnergizationUpgradeEffect(4))**game_energization_frequency.log10()

def getEnergyParticleGain():
    return (((game_main_energy+3).ln().log10()**(game_main_energy+1).ln())/Decimal('2.0')).to_integral_value(ROUND_DOWN)

def getLightPowerGain():
    return Decimal(10)**(((game_main_velocity.log10())/Decimal('8.477'))-Decimal(1))
    #Yes, this is basically the Antimatter Dimensions IP Formula...

def getResist():
    totalResist = Decimal('1')
    if (game_main_velocity >= Decimal('340') and game_energization_upgrade[3] == False):
        totalResist = totalResist * Decimal('2')**game_main_energy.log10()
    if (game_main_velocity >= Decimal('300000')):
        totalResist = totalResist * Decimal('1.1')**game_main_energy.ln()
    if (game_main_velocity >= Decimal('300000000')):
        totalResist = totalResist * Decimal('0.2')
    return totalResist

def getEnergizationUpgradeEffect(id):
    if (id == 1 and game_energization_upgrade[1] == True):
        return Decimal('3')
    elif (id == 2 and game_energization_upgrade[2] == True):
        return Decimal('2')
    elif (id == 3 and game_energization_upgrade[3] == True):
        return 0
    elif (id == 4 and game_energization_upgrade[4] == True):
        return Decimal('3')
    else:
        return Decimal('1')
    

#读取存档内容
with open('saves\SaveFile.txt', 'r') as f:
    stats = f.readlines()#读取存档
    #删换行符(\n)
    print(stats)
    for i in range(len(stats)):
        stats[i] = stats[i][:(len(stats[i])-1)]
    game_main_energy = Decimal(stats[0])
    game_main_energy_increase = Decimal(stats[1])
    game_main_velocity = Decimal(stats[2])
    game_main_acceleratorAmount = Decimal(stats[3])
    game_main_boosterAmount = Decimal(stats[4])
    game_main_chargerAmount = Decimal(stats[5])
    game_main_duplicatorAmount = Decimal(stats[6])
    game_energization_layerisUnlocked = str2bool(stats[7])
    game_energization_energyParticle = Decimal(stats[8])
    game_energization_energizerAmount = Decimal(stats[9])
    game_energization_frequency = Decimal(stats[10])
    game_energization_upgrade = [int(stats[11]), str2bool(stats[12]), str2bool(stats[13]), str2bool(stats[14]), str2bool(stats[15]), str2bool(stats[16])]
    #前面的写法好傻逼啊，这里换个写法
    for i in range(1, totalPlanets):
        game_planet[i].status = int(stats[16+i])
    game_light_layerisUnlocked = str2bool(stats[20])
    game_light_lightPower = Decimal(stats[21])

while True:
    clock.tick(dt)
    screen.fill((191,191,191))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            if (event.pos[0] <= 180):
                
                if Judge_positionInArea(event.pos[0], event.pos[1],10,10,90,90):
                    game_tabStatus = "main"
                    game_subtabStatus = 0
                elif Judge_positionInArea(event.pos[0], event.pos[1],10,100,90,180) and game_energization_layerisUnlocked:
                    game_tabStatus = "energization"
                    game_subtabStatus = 0
                elif Judge_positionInArea(event.pos[0], event.pos[1],10,190,90,270) and game_light_layerisUnlocked:
                    game_tabStatus = "light"
                    game_subtabStatus = 0

            elif game_tabStatus == "main":
                if Judge_positionInArea(event.pos[0], event.pos[1],240,190,300,250) and game_main_energy >= getAcceleratorCost(): #购买Accelerator
                    game_main_energy -= getAcceleratorCost()
                    game_main_acceleratorAmount += Decimal('1')
                elif Judge_positionInArea(event.pos[0], event.pos[1],240,320,300,380) and game_main_energy >= getBoosterCost(): #购买Booster
                    game_main_energy -= getBoosterCost()
                    game_main_boosterAmount += Decimal('1')
                elif Judge_positionInArea(event.pos[0], event.pos[1],240,450,300,510) and game_main_energy >= getChargerCost(): #购买Charger
                    game_main_energy -= getChargerCost()
                    game_main_chargerAmount += Decimal('1')
                elif Judge_positionInArea(event.pos[0], event.pos[1],240,580,300,640) and game_main_energy >= getDuplicatorCost(): #购买Duplicator
                    game_main_energy -= getDuplicatorCost()
                    game_main_duplicatorAmount += Decimal('1')
            elif game_tabStatus == "energization":
                if game_subtabStatus == 0:
                    if Judge_positionInArea(event.pos[0], event.pos[1],230,40,1030,140) and getEnergyParticleGain() >= Decimal('1.0'):
                        game_energization_energyParticle += getEnergyParticleGain()
                        Reset("E")
                    if Judge_positionInArea(event.pos[0], event.pos[1],240,190,300,250) and game_energization_energyParticle >= getEnergizerCost(): #购买Energizer
                        game_energization_energyParticle -= getEnergizerCost()
                        game_energization_energizerAmount += 1
                    if Judge_positionInArea(event.pos[0], event.pos[1],230,360,1030,420) and game_energization_energyParticle >= EnergizationUpgradeCost[1] and game_energization_upgrade[1] == False:
                        game_energization_upgrade[1] = True
                        game_energization_energyParticle -= EnergizationUpgradeCost[1]
                    if Judge_positionInArea(event.pos[0], event.pos[1],230,420,1030,480) and game_energization_energyParticle >= EnergizationUpgradeCost[2] and game_energization_upgrade[2] == False:
                        game_energization_upgrade[2] = True
                        game_energization_energyParticle -= EnergizationUpgradeCost[2]
                    if Judge_positionInArea(event.pos[0], event.pos[1],230,480,1030,540) and game_main_velocity >= EnergizationUpgradeCost[3] and game_energization_upgrade[3] == False:
                        game_energization_upgrade[3] = True
                        game_main_energy -= EnergizationUpgradeCost[3]**Decimal('2')
                    if Judge_positionInArea(event.pos[0], event.pos[1],230,540,1030,600) and game_energization_energyParticle >= EnergizationUpgradeCost[4] and game_energization_upgrade[4] == False:
                        game_energization_upgrade[4] = True
                        game_energization_energyParticle -= EnergizationUpgradeCost[4]
                elif game_subtabStatus == 1:
                    for i in range(len(game_planet)):
                        if game_planet[i].shown() == True:
                            if Judge_positionInArea(event.pos[0], event.pos[1], game_planet[i].pos[0], game_planet[i].pos[1], game_planet[i].pos[0]+50, game_planet[i].pos[1]+50) and game_energization_energyParticle >= game_planet[i].cost and game_planet[i].status == 0:
                                game_planet[i].status = 1
                                game_energization_energyParticle -= game_planet[i].cost
                            
        elif event.type == pygame.KEYDOWN:
            print(event.key)
            if (event.key == pygame.K_ESCAPE):
                print("HARD RESET...")
                game_tabStatus = "main"
                game_subtabStatus = 1
                game_main_energy = Decimal('1.0')
                game_main_energy_increase = Decimal()
                game_main_velocity = Decimal()
                game_main_acceleratorAmount = Decimal()
                game_main_boosterAmount = Decimal()
                game_main_chargerAmount = Decimal()
                game_main_duplicatorAmount = Decimal()

                game_energization_layerisUnlocked = False
                game_energization_energyParticle = Decimal()
                game_energization_energizerAmount = Decimal()
                game_energization_frequency = Decimal('1.0')
                game_energization_upgrade = [5, False, False, False, False, False]
                game_planet = [Planet(0, 0, 0, Decimal('1.0')), Planet(11, 220, 120, Decimal('10000')), Planet(21, 370, 120, Decimal('114514')), Planet(22, 220, 270, Decimal('19198100'))]
                for i in range(1, totalPlanets):
                    game_planet[i].status = 0
                game_light_layerisUnlocked = False
                game_light_lightPower = Decimal('0')
            elif (event.key == pygame.K_LEFT and game_subtabStatus >= 1):
                game_subtabStatus -= 1
            elif (event.key == pygame.K_RIGHT and game_subtabStatus < SubtabofTab[game_tabStatus]-getEnergizationUpgradeEffect(3)):
                game_subtabStatus += 1
                
    Tick()
    Display(game_tabStatus, game_subtabStatus)
    #print(getLightPowerGain())
    pygame.display.update()