from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
import mesa.time as time
import random
import matplotlib.pyplot as plt

import numpy as np


def get_step_number(model):
    return model.schedule.steps

def get_agents_interesse(model):
    return [round(a.interesse, 2) for a in model.schedule.agents]




class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.interesse = random.random()
        

    def step(self):
        self.interesse += 0.01
 
        

class SubsidieModel(Model):
    """A model with some numbers of agents"""

    def __init__(
        self, width = 50, height = 50 
    ):
        super().__init__()
        self.grid = SingleGrid(width, height, torus = True)
        self.schedule = time.BaseScheduler(self)

        for x in range(width):
            for y in range(height):
                agent = MoneyAgent((x, y), self)
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





