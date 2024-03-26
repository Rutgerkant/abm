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

def available_types(model, width, height):
    total_agents = width * height
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

def get_step_number(model):
    return model.schedule.steps

def calculate_belangstelling(model):
    for a in model.schedule.agents:
        if a.agent_type == TypeAdopter.INNOVATOR:
            a.belangstelling = 0.5 + a.leeftijd_auto * 0.05

        elif a.agent_type == TypeAdopter.EARLY_ADOPTER:
            a.belangstelling = 0.45 + a.leeftijd_auto * 0.5

        elif a.agent_type == TypeAdopter.EARLY_MAJORITY:
            a.belangstelling = 0.40 + a.leeftijd_auto * 0.5

        elif a.agent_type == TypeAdopter.LATE_MAJORITY:
           a.belangstelling = 0.35 + a.leeftijd_auto * 0.5

        elif a.agent_type == TypeAdopter.LAGGARDS:
            a.belangstelling = 0.30  + a.leeftijd_auto * 0.5





class TypeAdopter(Enum):
    INNOVATOR = 0
    EARLY_ADOPTER = 1
    EARLY_MAJORITY = 2
    LATE_MAJORITY = 3
    LAGGARDS = 4

class SubsidieModel(Model):
    """A model with some numbers of agents"""

    def __init__(
        self, width = 50, height = 50 
    ):
        super().__init__()
        self.grid = SingleGrid(width, height, torus = True)
        self.schedule = BaseScheduler(self)
        total_agents = width * height
        no_car_count = int(total_agents * 0.25)  # 25% have no car

        

        for agent in range(total_agents):
            x = random.randrange(width)
            y = random.randrange(height)
            agent_type = random.choice(available_types)  
            agent = MoneyAgent((x, y), self, agent_type)
            self.grid.move_to_empty(agent)
            self.schedule.add(agent)
        
        for _ in range(no_car_count):
            x = random.randrange(width)
            y = random.randrange(height)
            agent = MoneyAgent((x, y), self, TypeAdopter.NO_CAR)
            self.grid.move_to_empty(agent)  
            self.schedule.add(agent)

        model_metrics = {
                "step":get_step_number,
                "agent_interesse":calculate_belangstelling,
            }
        
        agent_metrics = {
            "interesse": "interesse"
            }

        self.datacollector = DataCollector(model_reporters=model_metrics,agent_reporters=agent_metrics)
        
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        calculate_belangstelling(self)
        self.datacollector.collect(self)

    def run(self, n):
        """Run the model for n steps."""
        for _ in range(n):
            self.step()





class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, pos, model, agent_type):
        super().__init__(pos, model)
        self.interesse = random.random()
        self.bezit_EV = False 
        self.leeftijd_auto = random.randint(0, 10)
        self.vermogen = random.randint(0, 80)
        self.agent_type = agent_type

    

        
        


