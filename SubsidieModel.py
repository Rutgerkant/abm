from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
import mesa.time as time
import random
import matplotlib.pyplot as plt
import numpy as np

import math 
from enum import Enum

from VermogenInkomen import genereer_random_vermogen

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

def appoint_leeftijd_auto():
    # cijfers van de kans zijn gehaald van https://www.cbs.nl/nl-nl/nieuws/2016/20/personenauto-s-steeds-ouder
    # leeftijd is in maanden
    leeftijd_auto = 0
    kans = random.random()
    if kans <= 0.156:
        leeftijd_auto = random.randint(0, 36)
    elif kans > 0.156 <= 0.342:
        leeftijd_auto = random.randint(36, 72)
    elif kans > 0.342 <= 0.495:
        leeftijd_auto = random.randint(72, 108)
    elif kans > 0.495 <= 0.656:
        leeftijd_auto = random.randint(108, 144)
    elif kans > 0.656 <= 0.797:
        leeftijd_auto = random.randint(144, 225)
    elif kans > 0.797:
        leeftijd_auto = random.randint(225, 360)
    
    return leeftijd_auto

def appoint_vermogen_inkomen():
    (a, b) = genereer_random_vermogen()
    return (a,b)

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

def subsidie_log(model):
    x = model.schedule.step
    subsidie = 3966.687 * math.exp(-0.076 * (x/12))
    return subsidie

def gemiddelde_belangstelling(model):
    total_belangstelling = sum(a.belangstelling for a in model.schedule.agents)
    mean_belangstelling = total_belangstelling / len(model.schedule.agents)
    return mean_belangstelling

def count_type(model, Agent_Type):

        count = 0 
        for a in model.schedule.agents:
            if a.agent_type == Agent_Type:
                count += 1

        return count

def calculate_belangstelling(model):
        subsidie = float(subsidie_log)
        for Agent in model.schedule.agents:
            if Agent.agent_type == TypeAdopter.INNOVATOR:
                Agent.belangstelling = 0.4  + (subsidie/1000)* 3.2
            elif Agent.agent_type == TypeAdopter.EARLY_ADOPTER:
                Agent.belangstelling = 0.35  * (0.087/12) + (subsidie/1000)* 3
            elif Agent.agent_type == TypeAdopter.EARLY_MAJORITY:
                Agent.belangstelling = 0.30  + (subsidie/1000)* 2.8
            elif Agent.agent_type == TypeAdopter.LATE_MAJORITY:
                Agent.belangstelling = 0.25 + (subsidie/1000)* 2.3
            elif Agent.agent_type == TypeAdopter.LAGGARDS:
                Agent.belangstelling = 0.20 + (subsidie/1000)* 1.7

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
                    Leeftijd_auto = appoint_leeftijd_auto()
                    (vermogen, inkomen) = appoint_vermogen_inkomen()

                agent = AdoptionAgent((x,y), self, agent_type, heeft_auto, Leeftijd_auto, vermogen, inkomen)
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
    def __init__(self, pos, model, agent_type, bezit_auto, leeftijd_auto, vermogen, inkomen):
        super().__init__(pos, model)
        self.agent_type = agent_type
        self.bezit_auto = bezit_auto
        self.bezit_EV = False

        self.vermogen = vermogen
        self.inkomen = inkomen
        self.belangstelling = 0.0
        self.bezit_auto = bezit_auto
        if self.bezit_auto == True:
            self.leeftijd_auto = leeftijd_auto
        else:
            self.leeftijd_auto = 0
        



     
