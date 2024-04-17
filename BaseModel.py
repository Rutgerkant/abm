from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
import mesa.time as time
import random
import matplotlib.pyplot as plt
import numpy as np
from aantalSubs import reset_subsidiepot, Tracking_Subs
import math 
from enum import Enum

from VermogenInkomen import genereer_random_vermogen

lst_agents = []

def get_lst_agents():
    return lst_agents

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

def count_type(model, Agent_Type):

        count = 0 
        for a in model.schedule.agents:
            if a.agent_type == Agent_Type:
                count += 1

        return count


class TypeAdopter(Enum):
    INNOVATOR = 0
    EARLY_ADOPTER = 1
    EARLY_MAJORITY = 2
    LATE_MAJORITY = 3
    LAGGARDS = 4

class BaseModelSub(Model):
    def __init__(self, width = 89, height = 89):
        super().__init__()
        self.width = width
        self.height = height
        

        
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=False)

        self.total_agents = self.width * self.height
        self.prijs_EV = 40000
        self.prijs_FBA = 33000
        self.subsidie = 0
        self.hoeveelheid_subsidie = 0

        self.gekochte_evs = 0
        self.gekochte_fba = 0
        

        for x in range(self.width):
            for y in range(self.height):
                agent_type = appoint_type(self, self.total_agents)
                heeft_auto = False
                Leeftijd_auto = 0
                if random.random() > 0.26:
                    heeft_auto = True
                    Leeftijd_auto = appoint_leeftijd_auto()
                
                
                (vermogen, inkomen) = appoint_vermogen_inkomen()

                agent = AdoptionAgent((x,y), self, agent_type, heeft_auto, Leeftijd_auto, vermogen, inkomen)
                lst_agents.append(agent)
                self.grid.place_agent(agent, (x, y))

                self.schedule.add(agent)
    
    def step(self):
        self.schedule.step()
        
        

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


    