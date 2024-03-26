from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
import mesa.time as time
import random
import matplotlib.pyplot as plt

import numpy as np

from enum import Enum


def step(self):
        self.interesse += 0.01

def get_step_number(model):
    return model.schedule.steps

def get_agents_interesse(model):
    return [round(a.interesse, 2) for a in model.schedule.agents]



class SubsidieModel(Model):
    """A model with some numbers of agents"""

    def __init__(
        self, width = 50, height = 50 
    ):
        super().__init__()
        self.grid = SingleGrid(width, height, torus = True)
        self.schedule = BaseScheduler(self)

        innovator_percentage = 0.026
        early_adopter_percentage = 0.166
        early_majority_percentage = 0.34
        late_majority_percentage = 0.34
        laggard_percentage = 0.168

        total_agents = width * height
        innovator_count = int(total_agents * innovator_percentage)
        early_adopter_count = int(total_agents * early_adopter_percentage)
        early_majority_count = int(total_agents * early_majority_percentage)
        late_majority_count = int(total_agents * late_majority_percentage)
        laggard_count = int(total_agents * laggard_percentage)
        no_car_count = int(total_agents * 0.25)  # 25% have no car

        agent_counts = [innovator_count, early_adopter_count, early_majority_count,
                        late_majority_count, laggard_count]

        agent_type = 0
        for count in agent_counts:
            for _ in range(count):
                x = random.randrange(width)
                y = random.randrange(height)
                agent = MoneyAgent((x, y), self, TypeAdopter(agent_type))
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)
            agent_type += 1

        # Add agents with no car
        for _ in range(no_car_count):
            x = random.randrange(width)
            y = random.randrange(height)
            agent = MoneyAgent((x, y), self, TypeAdopter.NO_CAR)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)


        model_metrics = {
                "step":get_step_number,
                "agent_interesse":get_agents_interesse,
            }
        
        agent_metrics = {
            "interesse": "interesse"
            }

        self.datacollector = DataCollector(model_reporters=model_metrics,agent_reporters=agent_metrics)
        
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def run(self, n):
        """Run the model for n steps."""
        for _ in range(n):
            self.step()



class TypeAdopter(Enum):
    INNOVATOR = 0
    EARLY_ADOPTER = 1
    EARLY_MAJORITY = 2
    LATE_MAJORITY = 3
    LAGGARDS = 4

class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.interesse = random.random()
        self.bezit_EV = False 
        self.leeftijd_auto = random.randint(10)
        self.vermogen = random.randint(80)
        
        


