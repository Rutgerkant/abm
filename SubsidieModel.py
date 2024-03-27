from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
import mesa.time as time
import random
import matplotlib.pyplot as plt

import numpy as np

from enum import Enum


def count_innovators(model):
    amount_innovators = sum(1 for a in model.schedule.agents if a.agent_type == TypeAdopter.INNOVATOR)
    return amount_innovators

def count_early_adopters(model):
    amount_early_adopters = sum(1 for a in model.schedule.agents if a.agent_type == TypeAdopter.EARLY_ADOPTER)
    return amount_early_adopters

def count_early_majority(model):
    amount_early_majority = sum(1 for a in model.schedule.agents if a.agent_type == TypeAdopter.EARLY_MAJORITY)
    return amount_early_majority

def count_late_majority(model):
    amount_late_majority = sum(1 for a in model.schedule.agents if a.agent_type == TypeAdopter.LATE_MAJORITY)
    return amount_late_majority

def count_laggards(model):
    amount_laggards = sum(1 for a in model.schedule.agents if a.agent_type == TypeAdopter.LAGGARDS)
    return amount_laggards

def appoint_type(model, total_agents):
    max_innovator = int(total_agents * 0.026)
    max_early_adopter = int(total_agents * 0.166)
    max_early_majority = int(total_agents * 0.34)
    max_late_majority = int(total_agents * 0.34)
    max_laggard = int(total_agents * 0.168) 
    available_types = []
    if count_innovators(model) <= max_innovator:
            available_types.append(TypeAdopter.INNOVATOR)

    if count_early_adopters(model) <= max_early_adopter:
        available_types.append(TypeAdopter.EARLY_ADOPTER)
    
    if count_early_majority(model) <= max_early_majority:
        available_types.append(TypeAdopter.EARLY_MAJORITY)

    if count_late_majority(model) <= max_late_majority:
        available_types.append(TypeAdopter.LATE_MAJORITY)
    
    if count_laggards(model) <= max_laggard:
        available_types.append(TypeAdopter.LAGGARDS)

    agent_type = random.choice(available_types)
    return agent_type

def get_step_number(model):
    return model.schedule.steps

def calculate_belangstelling(self):
        if self.agent_type == TypeAdopter.INNOVATOR:
            self.belangstelling = 0.5 + self.leeftijd_auto * 0.05
        elif self.agent_type == TypeAdopter.EARLY_ADOPTER:
            self.belangstelling = 0.45 + self.leeftijd_auto * 0.5
        elif self.agent_type == TypeAdopter.EARLY_MAJORITY:
            self.belangstelling = 0.40 + self.leeftijd_auto * 0.5
        elif self.agent_type == TypeAdopter.LATE_MAJORITY:
            self.belangstelling = 0.35 + self.leeftijd_auto * 0.5
        elif self.agent_type == TypeAdopter.LAGGARDS:
            self.belangstelling = 0.30  + self.leeftijd_auto * 0.5

def gemiddelde_belangstelling(model):
    total_belangstelling = sum(a.belangstelling for a in model.schedule.agents)
    mean_belangstelling = total_belangstelling / len(model.schedule.agents)
    return mean_belangstelling



class TypeAdopter(Enum):
    INNOVATOR = 0
    EARLY_ADOPTER = 1
    EARLY_MAJORITY = 2
    LATE_MAJORITY = 3
    LAGGARDS = 4

class SubsidieModel(Model):
    """A model with some numbers of agents"""

    def __init__(
        self, width = 50, height = 50, subsidie_start = 5000, subsidie_verandering_per_stap = 20 
    ):
        super().__init__()
        self.grid = SingleGrid(width, height, torus = True)
        self.schedule = BaseScheduler(self)
        total_agents = width * height
        kans_bezit_auto = 0.75

        self.width = width
        self.height = height
        self.subsidie = subsidie_start
        self.subsidie_verandering_per_stap = subsidie_verandering_per_stap

        for x in range(self.width):
            for y in range(self.height):
                agent_type = appoint_type(self, total_agents)
                if agent_type is not None:
                    pos = (x, y)
                    print({x,y}, {agent_type})
                    agent = AdoptionAgent(self, pos, agent_type)
                    self.grid.place_agent(agent, pos)
                    self.schedule.add(agent)
   

    

        model_metrics = {
                "step":get_step_number,
                "Aantal_Innovators": count_innovators,
                "gemiddelde_belangstelling": gemiddelde_belangstelling,
            }
        
        agent_metrics = {
            "belangstelling": "belangstelling"
            }

        self.datacollector = DataCollector(model_reporters=model_metrics,agent_reporters=agent_metrics)
        
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.subsidie = max(self.subsidie + self.subsidie_verandering_per_stap, 0)  # Update de subsidie
        self.schedule.step()
        for agent in self.schedule.agents:
            agent.step()  # Roep de step methode van elke agent aan
        self.datacollector.collect(self)


    def run(self, n):
        """Run the model for n steps."""
        for _ in range(n):
            self.step()


class AdoptionAgent(Agent):
    """ Een agent met algemene eigenschappen voor innovatie adoptie."""
    def __init__(self, unique_id, model, pos, agent_type, belangstelling=0, subsidie=0):
        super().__init__(unique_id, model)  # Hier wordt de __init__-methode van Agent correct aangeroepen
        self.pos = pos
        self.agent_type = agent_type
        self.subsidie = subsidie 
        self.vermogen = random.normalvariate(mu=50000, sigma=12500)
        self.belangstelling = belangstelling
        self.heeft_ev_gekocht = False
        self.leeftijd_auto = random.randint(0, 30)

        print(self.unique_id, self.pos, self.agent_type)

    def proberen_EV_te_kopen(self, EV_prijs=20000, auto_leeftijd_drempel=5):
        if not self.heeft_ev_gekocht:
            effectief_vermogen = self.vermogen
            if self.subsidie > 0:
                effectief_vermogen += self.subsidie
            if self.leeftijd_auto >= auto_leeftijd_drempel and effectief_vermogen >= EV_prijs and self.belangstelling > 0.4:
                self.heeft_ev_gekocht = True

    def step(self):
        calculate_belangstelling(self)
        self.proberen_EV_te_kopen()
