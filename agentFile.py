
import mesa 
import random
from mesa.time import RandomActivation  

from mesa import Agent

from SubsidieModel import calculate_belangstelling

class AdoptionAgent(Agent):
    """ Een agent met algemene eigenschappen voor innovatie adoptie."""
    def __init__(self, unique_id, model, agent_type, belangstelling , subsidie = 0):
        super().__init__(unique_id, model)
        self.agent_type = agent_type
        self.vermogen = random.normalvariate(mu = 50000, sigma=12500)         #normaalverdeling van het inkomen
        self.belangstelling = belangstelling
        self.heeft_ev_gekocht = False
        self.leeftijd_auto = random.randit(0, 30)   #waarde van leeftijd auto
        self.subsidie = subsidie 

    def proberen_EV_te_kopen(self, EV_prijs, auto_leeftijd_drempel):
        # Check of de agent al een EV heeft gekocht
        if not self.heeft_ev_gekocht:
            effectief_vermogen = self.vermogen
            # Als de agent nog geen EV heeft, voeg dan de subsidie toe aan het vermogen
            if self.subsidie > 0:
                effectief_vermogen += self.subsidie
            if self.leeftijd_auto >= auto_leeftijd_drempel and effectief_vermogen >= EV_prijs and self.belangstelling > 0.4:
                self.heeft_ev_gekocht = True   
    def step(self):
        # Voorbeeldgedrag: print hun type
        calculate_belangstelling(self)
        self.proberen_EV_te_kopen()
        print(f"Agent {self.unique_id} van type {self.agent_type} handelt.")


class Innovators(AdoptionAgent):
    def step(self):
              #toewijzing van vermogen tussen twee bepaalde intervallen
        print(f"Innovator {self.unique_id} handelt innovatief.")

class EarlyAdopters(AdoptionAgent):
    def step(self):
        
        print(f"Early Adopter {self.unique_id} adopteert vroeg.")

class EarlyMajority(AdoptionAgent):
    def step(self):
        
        print(f"Early Majority {self.unique_id} overweegt zorgvuldig.")

class LateMajority(AdoptionAgent):
    def step(self):
        
        print(f"Late Majority {self.unique_id} is sceptisch maar volgt uiteindelijk.")

class Laggards(AdoptionAgent):
    def step(self):
        
        print(f"Laggard {self.unique_id} is zeer terughoudend met verandering.")
 
