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

from BaseModel import BaseModelSub, get_lst_agents, TypeAdopter

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
    x = model.schedule.steps // 12
    subsidie = 3966.687 * math.exp(-0.076 * (x))
    return subsidie

def gemiddelde_belangstelling(model):
    total_belangstelling = sum(a.belangstelling for a in model.schedule.agents)
    mean_belangstelling = total_belangstelling / len(model.schedule.agents)
    return mean_belangstelling

def gemiddelde_leeftijd_auto(model):
    som = 0
    aantal = 0
    for a in model.schedule.agents:
        if a.bezit_auto == True:
            som += a.leeftijd_auto
            aantal += 1

    gem = som /aantal
    return gem 

def late_majority_ev(model):
    count_late_majority = 0
    late_majority_met_EV = 0
    for a in model.schedule.agents:
        if a.agent_type == TypeAdopter.LATE_MAJORITY:
            if a.bezit_auto == True:
                count_late_majority += 1
                if a.bezit_EV == True:
                    late_majority_met_EV += 1
    percentage = late_majority_met_EV / count_late_majority
    return percentage

def laggards_ev(model):
    count_laggards = 0
    laggards_met_EV = 0
    for a in model.schedule.agents:
        if a.agent_type == TypeAdopter.LAGGARDS:
            if a.bezit_auto == True:
                count_laggards += 1
                if a.bezit_EV == True:
                    aggards_met_EV += 1
    percentage = laggards_met_EV / count_laggards
    return percentage

def count_type(model, Agent_Type):

        count = 0 
        for a in model.schedule.agents:
            if a.agent_type == Agent_Type:
                count += 1

        return count

def calculate_belangstelling(model):
        subsidie = subsidie_log(model)
        subsidie = float(subsidie)
        for Agent in model.schedule.agents:
            if Agent.agent_type == TypeAdopter.INNOVATOR:
                Agent.belangstelling = 0.75  + (subsidie/1000)* 0.032
            elif Agent.agent_type == TypeAdopter.EARLY_ADOPTER:
                Agent.belangstelling = 0.716  + (subsidie/1000)* 0.03
            elif Agent.agent_type == TypeAdopter.EARLY_MAJORITY:
                Agent.belangstelling = 0.524  + (subsidie/1000)* 0.028
            elif Agent.agent_type == TypeAdopter.LATE_MAJORITY:
                Agent.belangstelling = 0.406 + (subsidie/1000)* 0.023
            elif Agent.agent_type == TypeAdopter.LAGGARDS:
                Agent.belangstelling = 0.374 + (subsidie/1000)* 0.017

def wil_auto_kopen(model):
    count = 0
    count_auto = 0
    
    for a in model.schedule.agents:
        count += 1
        if a.bezit_EV == False:
            if a.bezit_auto == True and a.leeftijd_auto > model.drempelwaarde:
                kans = a.leeftijd_auto // 12 * 0.087
                if random.random() < kans:
                    count_auto += 1
                    koopt_auto(model, a) 

def koopt_auto(model, a):
    if a.vermogen > model.prijs_EV:
        interesse = a.belangstelling
        kans = random.random()
        if kans < interesse:
                
                koopt_EV(model, a)

    elif a.vermogen > model.prijs_FBA:
            a.bezit_auto = True
            a.leeftijd_auto = 0
            model.gekochte_fba += 1

    elif (a.vermogen + model.subsidie) > model.prijs_EV:
         koopt_EV(model, a) 
        
def koopt_EV(model, agent):
        agent.bezit_auto = True
        agent.bezit_EV = True
        model.gekochte_evs += 1
        model.hoeveelheid_subsidie += model.subsidie

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


class SubsidieModel(BaseModelSub):
    def __init__(self, a, b, width = 28, height = 28):
        super().__init__(width, height)
        self.prijs_EV = a
        self.prijs_FBA = b

        model_metrics = {
             "Gemiddelde belangstelling": gemiddelde_belangstelling,
             "Aantal gekochte EV": lambda model: model.gekochte_evs,
             "Aantal gekochte FBA": lambda model: model.gekochte_fba,
             "Percentage huishoudens in bezit auto": huishoudens_bezit_auto,
             "Percerntage EV's van Auto's": percentage_evs,
             "Hoeveelheid totale Subsidie": lambda model: model.hoeveelheid_subsidie,
             "Hoeveelheid Subsidie": lambda model: model.subsidie,
             "Percentage late majority met EV": late_majority_ev,
             "Percentage laggards met EV": laggards_ev
         }
        
        agent_metrics = {
            "Type Agent": lambda agent: agent.agent_type.name,
            "Belangstelling": lambda agent: agent.belangstelling,
            "leeftijd auto": lambda agent: agent.leeftijd_auto,
            "Vermogen Agent": lambda agent:agent.vermogen,
            "agent heeft ev": lambda agent:agent.bezit_EV
        }

        self.datacollector = DataCollector(model_reporters=model_metrics,agent_reporters=agent_metrics)

        self.running = True
        
    def step(self):
        self.schedule.step()
        self.subsidie = subsidie_log(self)
        for agent in self.schedule.agents:
            agent.leeftijd_auto += 1
            agent.vermogen += agent.inkomen

        
        calculate_belangstelling(self)
        wil_auto_kopen(self)

        huishoudens_bezit_auto(self)
        percentage_evs(self)
        late_majority_ev(self)
        laggards_ev(self)
        
        self.datacollector.collect(self)
        
        



