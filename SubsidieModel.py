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
        self.interesse += 0.05
 
        

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


model1 = SubsidieModel(1)




# Druk de model metrics af
for i in range(10):
    model1.step()

model_data = model1.datacollector.get_model_vars_dataframe()

print(model_data)


import holoviews as hv
from collections import defaultdict


def value(cell):
    if cell.interesse  < 0.5: return 15   # if the tree is fine, another color
    elif cell.interesse > 0.5 and cell.interesse < 0.8: return 20    # if the tree is on fire, another color
    elif cell.interesse > 0.8 : return 5   # if the cell is burned out, another color

hmap = hv.HoloMap()  # draws the holoviews grid

for i in range(100):   
    model1.step()   # This will run the model for one step. Because of the for loop, the model will run for 100 steps in total!!!!!
    # Note: It is not a big problem if you don't completely understand the next few lines since these concern the holoviews library
    grid_dict = defaultdict(list)
    for content, row_index, col_index in model1.grid.coord_iter():
        grid_dict[row_index] += [content]  
    data = np.array([[value(c) for c in row] for row in grid_dict.values()])
    data = np.transpose(data)
    data = np.flip(data, axis=0)
    bounds=(0,0,5,5)   # Coordinate system: (left, bottom, right, top)
    hmap[i] = hv.Image(data, vdims=[hv.Dimension('a', range=(0,21))],bounds=bounds).relabel('Grid').opts(cmap='Viridis',xticks=[0],yticks=[0])
    # holoviews comes with different colormaps (cmap). In this case, we are using the colormap Viridis, which has a color scheme between blue and yellow.
hmap