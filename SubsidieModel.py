from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
import mesa.time as time
import random
import matplotlib.pyplot as plt
import numpy as np

from enum import Enum


def percentage_evs(model):
    total_cars = 0
    total_evs = 0
    for a in model.schedule.agents:
        if a.bezit_auto == True:
            total_cars +=1 
            if a.bezit_EV == True:
                total_evs += 1
    percentage = total_evs / total_cars
    return percentage

def subsidie_liniear(model):
    subsidie = 0 
    tijdstap = model.schedule.step
    if subsidie < 4000:
        subsidie = 200* tijdstap

    return subsidie

def gemiddelde_belangstelling(model):
    total_belangstelling = sum(a.belangstelling for a in model.schedule.agents)
    mean_belangstelling = total_belangstelling / len(model.schedule.agents)
    return mean_belangstelling

def appoint_type(model, total_agents):
    max_innovator = int(total_agents * 0.025)
    max_early_adopter = int(total_agents * 0.135)
    max_early_majority = int(total_agents * 0.34)
    max_late_majority = int(total_agents * 0.34)
    max_laggard = int(total_agents * 0.16) 
    
    available_types = list(TypeAdopter)
    
    while True:
        agent_type = random.choice(available_types)
        amount_agents = count_type(model, agent_type)

        if agent_type == TypeAdopter.INNOVATOR and amount_agents <= max_innovator:
            break

        elif agent_type == TypeAdopter.EARLY_ADOPTER and amount_agents <= max_early_adopter:
            break
            
        elif agent_type == TypeAdopter.EARLY_MAJORITY and amount_agents <= max_early_majority:
            break
            
        elif agent_type == TypeAdopter.LATE_MAJORITY and amount_agents <= max_late_majority:
            break

        elif agent_type == TypeAdopter.LAGGARDS and amount_agents <= max_laggard:
            break


    return agent_type

def count_type(model, Agent_Type):

        count = 0 
        for a in model.schedule.agents:
            if a.agent_type == Agent_Type:
                count += 1

        return count

def calculate_belangstelling(model):
        for Agent in model.schedule.agents:
            if Agent.agent_type == TypeAdopter.INNOVATOR:
                Agent.belangstelling = 0.4 + (Agent.leeftijd_auto/12) * 0.05
            elif Agent.agent_type == TypeAdopter.EARLY_ADOPTER:
                Agent.belangstelling = 0.35 + (Agent.leeftijd_auto/12) * 0.05
            elif Agent.agent_type == TypeAdopter.EARLY_MAJORITY:
                Agent.belangstelling = 0.30 + (Agent.leeftijd_auto/12) * 0.05
            elif Agent.agent_type == TypeAdopter.LATE_MAJORITY:
                Agent.belangstelling = 0.25 + (Agent.leeftijd_auto/12) * 0.05
            elif Agent.agent_type == TypeAdopter.LAGGARDS:
                Agent.belangstelling = 0.20  + (Agent.leeftijd_auto/12) * 0.05


# Definieer de inkomensintervallen en bijbehorende aantallen huishoudens
inkomensintervallen = [
    ("< -6", -6, -6),
    ("-6 tot -4", -6, -4),
    ("-4 tot -2", -4, -2),
    ("-2 tot 0", -2, 0),
    ("0 tot 2", 0, 2),
    ("2 tot 4", 2, 4),
    ("4 tot 6", 4, 6),
    ("6 tot 8", 6, 8),
    ("8 tot 10", 8, 10),
    ("10 tot 12", 10, 12),
    ("12 tot 14", 12, 14),
    ("14 tot 16", 14, 16),
    ("16 tot 18", 16, 18),
    ("18 tot 20", 18, 20),
    ("20 tot 22", 20, 22),
    ("22 tot 24", 22, 24),
    ("24 tot 26", 24, 26),
    ("26 tot 28", 26, 28),
    ("28 tot 30", 28, 30),
    ("30 tot 32", 30, 32),
    ("32 tot 34", 32, 34),
    ("34 tot 36", 34, 36),
    ("36 tot 38", 36, 38),
    ("38 tot 40", 38, 40),
    ("40 tot 42", 40, 42),
    ("42 tot 44", 42, 44),
    ("44 tot 46", 44, 46),
    ("46 tot 48", 46, 48),
    ("48 tot 50", 48, 50),
    ("50 tot 52", 50, 52),
    ("52 tot 54", 52, 54),
    ("54 tot 56", 54, 56),
    ("56 tot 58", 56, 58),
    ("58 tot 60", 58, 60),
    ("60 tot 62", 60, 62),
    ("62 tot 64", 62, 64),
    ("64 tot 66", 64, 66),
    ("66 tot 68", 66, 68),
    ("68 tot 70", 68, 70),
    ("70 tot 72", 70, 72),
    ("72 tot 74", 72, 74),
    ("74 tot 76", 74, 76),
    ("76 tot 78", 76, 78),
    ("78 tot 80", 78, 80),
    ("80 tot 82", 80, 82),
    ("82 tot 84", 82, 84),
    ("84 tot 86", 84, 86),
    ("86 tot 88", 86, 88),
    ("88 tot 90", 88, 90),
    ("90 tot 92", 90, 92),
    ("92 tot 94", 92, 94),
    ("94 tot 96", 94, 96),
    ("96 tot 98", 96, 98),
    ("98 tot 100", 98, 100),
    ("> 100", 100, 100)
]

aantallen = [
    4, 1, 2, 21, 38, 46, 52, 52, 57, 62, 85, 158, 326, 443, 479, 520,
    456, 434, 434, 429, 418, 404, 384, 354, 317, 280, 246, 215, 185, 158,
    134, 113, 95, 80, 68, 57, 48, 41, 35, 30, 26, 22, 19, 17, 15, 13,
    12, 11, 10, 9, 8, 7, 6, 6, 95
]

# Genereer een lijst van waarden en gewichten
waarden = []
gewichten = []

for interval, aantal in zip(inkomensintervallen, aantallen):
    label, min_, max_ = interval
    waarden.append((min_ + max_) / 2) # Gebruik het middenpunt voor elke range
    gewichten.append(aantal)

# Gebruik de gewichten om een interval te kiezen en genereer een random waarde binnen dat interval
def genereer_random_inkomen(waarden, gewichten):
    gekozen_index = np.random.choice(len(waarden), p=gewichten/np.sum(gewichten))
    min_, max_ = inkomensintervallen[gekozen_index][1], inkomensintervallen[gekozen_index][2]
    if min_ == max_: # Voor de vaste waarden
        return min_ * 1000  # Verander de waarde naar euro's
    else:
        return np.random.uniform(min_, max_) * 1000  # Verander de waarde naar euro's en genereer binnen het interval

# Genereer een random inkomen
random_inkomen = genereer_random_inkomen(waarden, gewichten)

import numpy as np

# Definieer de vermogensintervallen en bijbehorende aantallen huishoudens
vermogensintervallen = [
    ("nulde percentiel", -np.inf, -1.5),
    ("eerste percentiel", -1.5, 2),
    ("tweede percentiel", 2, 12.4),
    ("derde percentiel", 12.4, 50.2),
    ("vierde percentiel", 50.2, 135.1),
    ("vijfde percentiel", 135.1, 218.6),
    ("zesde percentiel", 218.6, 312.0),
    ("zevende percentiel", 312.0, 434.80),
    ("achtste percentiel", 434.80, 670.5),
    ("negende percentiel", 670.5, np.inf)
]

aantallen_huishoudens = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

vermogenswaarden = []
vermogensgewichten = []

for interval in vermogensintervallen:
    label, min_, max_ = interval
    if np.isinf(min_) or np.isinf(max_):
        vermogenswaarden.append(max_ if np.isinf(min_) else min_)  # Neem de enige beschikbare waarde als een van de grenzen oneindig is
    else:
        vermogenswaarden.append((min_ + max_) / 2)  # Gebruik het middenpunt voor elke range
    vermogensgewichten.append(aantallen_huishoudens[vermogensintervallen.index(interval)])

def genereer_random_vermogen(vermogenswaarden, vermogensgewichten):
    gekozen_index = np.random.choice(len(vermogenswaarden), p=vermogensgewichten/np.sum(vermogensgewichten))
    min_, max_ = vermogensintervallen[gekozen_index][1], vermogensintervallen[gekozen_index][2]
    if np.isinf(min_) or np.isinf(max_):
        return vermogenswaarden[gekozen_index] * 1000  # Verander de waarde naar euro's
    else:
        return np.random.uniform(min_, max_) * 1000  # Verander de waarde naar euro's en genereer binnen het interval

# Genereer een random vermogen
random_vermogen = genereer_random_vermogen(vermogenswaarden, vermogensgewichten)
print(f"Random gegenereerd vermogen: €{random_vermogen:.2f}")


def wil_auto_kopen(model):
    drempel_leeftijd_auto = 60
    for a in model.schedule.agents:
        if a.bezit_EV == False:
            if a.bezit_auto == False:
                if random.random() < 0.2:
                    koopt_auto(model, a)        
            else:
                if a.leeftijd_auto > drempel_leeftijd_auto:
                    if random.random() < 0.80:
                        koopt_auto(model, a)
                
                elif a.agent_type == TypeAdopter.INNOVATOR:
                    if random.random() < 0.25 and a.vermogen > model.prijs_EV:
                        koopt_EV(model, a)                    

def koopt_auto(model, a):
    if a.vermogen > model.prijs_EV or (a.vermogen + model.subsidie > model.prijs_EV):
        if a.belangstelling > 0.7:
            if random.random() > 0.2: 
                koopt_EV(model, a)
        
        elif a.belangstelling > 0.6 and a.belangstelling <= 0.7:
            if random.random() > 0.4: 
                koopt_EV(model, a)
            
        if a.belangstelling > 0.5 and a.belangstelling <= 0.6:
            if random.random() > 0.6: 
                koopt_EV(model, a)
        
    elif a.vermogen > model.prijs_FBA:
            a.bezit_auto = True
            a.leeftijd_auto = 0
            model.gekochte_fba += 1
        
def koopt_EV(model, agent):
        agent.bezit_auto = True
        agent.bezit_EV = True
        model.gekochte_evs += 1

def aantal_evs(model):
    count = 0
    for a in model.schedule.agents:
        if a.bezit_EV == True:
            count +=1

    return count

def huishoudens_bezit_auto(model):
    heeft_wel = 0
    for a in model.schedule.agents:
        if a.bezit_auto == True:
            heeft_wel += 1

    percentage_bezit_auto = heeft_wel/model.total_agents
    return percentage_bezit_auto

class TypeAdopter(Enum):
    INNOVATOR = 0
    EARLY_ADOPTER = 1
    EARLY_MAJORITY = 2
    LATE_MAJORITY = 3
    LAGGARDS = 4

class SubsidieModel(Model):
    def __init__(self, width = 50, height =50 ):
        super().__init__()
        self.width = width
        self.height = height

        
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=False)

        self.total_agents = self.width * self.height
        self.prijs_EV = 40000
        self.prijs_FBA = 33000
        self.subsidie = 0

        self.gekochte_evs = 0
        self.gekochte_fba = 0

        for x in range(self.width):
            for y in range(self.height):
                agent_type = appoint_type(self, self.total_agents)
                heeft_auto = False
                if random.random() > 0.26:
                    heeft_auto = True

                agent = AdoptionAgent((x,y), self, agent_type, heeft_auto)
                self.grid.place_agent(agent, (x, y))

                self.schedule.add(agent)


        model_metrics = {
             "Gemiddelde belangstelling": gemiddelde_belangstelling,
             "Aantal gekochte EV": lambda model: model.gekochte_evs,
             "Aantal gekochte FBA": lambda model: model.gekochte_fba,
             "Percentage huishoudens in bezit auto": huishoudens_bezit_auto,
             "Percerntage EV's van Auto's": percentage_evs
         }
        
        agent_metrics = {
            "Type Agent": lambda agent: agent.agent_type.name,
            "Belangstelling": lambda agent: agent.belangstelling,
            "leeftijd auto": lambda agent: agent.leeftijd_auto
        }

        self.datacollector = DataCollector(model_reporters=model_metrics,agent_reporters=agent_metrics)
        
        self.running = True
        

    def step(self):
        self.schedule.step()
        for agent in self.schedule.agents:
            agent.leeftijd_auto += 1

        calculate_belangstelling(self)
        wil_auto_kopen(self)


        huishoudens_bezit_auto(self)
        percentage_evs(self)
        self.datacollector.collect(self)


class AdoptionAgent(Agent):
    def __init__(self, pos, model, agent_type, bezit_auto):
        super().__init__(pos, model)
        self.agent_type = agent_type
        self.bezit_auto = bezit_auto
        self.bezit_EV = False

        self.vermogen = random.normalvariate(mu=50000, sigma=12500)
        self.belangstelling = 0.0
        if self.bezit_auto == True:
            self.leeftijd_auto = random.randint(0, 120)
        else:
            self.leeftijd_auto = 0
        



     
