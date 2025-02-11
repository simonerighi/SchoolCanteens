# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency as c, currency_range
import random
import numpy as np
import math
# </standard imports>


doc = """
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""


source_code = ""


bibliography = ()


links = {}


keywords = ()


class Constants:
    name_in_url = 'payment_info'
    players_per_group = None
    num_rounds = 1

class Subsession(otree.models.BaseSubsession):
    pass
#    def vars_for_admin_report(self):
#        payoffs = sorted([p.payoff for p in self.get_players()])
#        return {'payoffs': payoffs}
        

class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    
    def simsort(self,vct):
        return [x for x,y in sorted(enumerate(vct), key = lambda x: x[1])]
        # this should return the indexes x of sorted from the one corresponding to the smallest element of vct to the largest one (same as argsort).

    def set_total_payoff(self):
        for p in self.subsession.get_players(): 
            p.total_payoff_ego= p.participant.vars['PGGSimple_payoff_bl'] + p.participant.vars['Dictator_payoff'] + p.participant.vars['Trust_payoff']+ p.participant.vars['bomb_payoff']
            p.participant.vars['total_payoff_ego']=p.total_payoff_ego
        listadipartecipanti=self.subsession.get_players()
        sorted_players=sorted(listadipartecipanti, key=lambda totalPayoffEgo: totalPayoffEgo.participant.vars['total_payoff_ego'], reverse=True)  
        i=0
        for p in sorted_players:
           p.rankpos=i+1
           i=i+1
        
        totalnumparticipants=self.session.num_participants
        first_third_start=1
        first_third_end=math.ceil(totalnumparticipants/3)
        second_third_start=first_third_end+1
        second_third_end=first_third_end+math.ceil(totalnumparticipants/3)
        for p in self.subsession.get_players():
            if p.rankpos <= first_third_end:
                p.payoffnum=2;
                p.payoff=2
                p.participant.payoff=2
                p.participant.note=2
            elif second_third_start<= p.rankpos <= second_third_end:
                p.payoffnum=1;
                p.payoff=1
                p.participant.payoff=1
                p.participant.note=1
            else:
                p.payoffnum=0;
                p.payoff=0
                p.participant.payoff=0
                p.participant.note=0
            p.numpart=self.session.num_participants

class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    
    total_pay=models.DecimalField(max_digits=4, decimal_places=2) #CurrencyField() #
    
    total_payoff_ego=models.CurrencyField()
    
    rankpos=models.PositiveIntegerField()
    
    numpart=models.PositiveIntegerField()
    
    payoffnum=models.PositiveIntegerField()
    #def set_totalpay(self):
    #    self.total_pay = self.participant.money_to_pay().to_real_world_currency(self.session)

#class stuffs:
#    def argsort(self):
#        return [x for x,y in sorted(enumerate(self), key = lambda x: x[1])]


#vect=np.array([],dtype=int)
#        for p in self.subsession.get_players():
#            print(p.participant.vars['total_payoff_ego'])
#            np.append(vect, np.int(p.participant.vars['total_payoff_ego']))
#            print(np.array(vect))
#        print(np.array(vect))
#        sorted_players=np.argsort(vect, axis=1, kind='quicksort', order=None)



""" WORKS BADLY
    def set_total_payoff(self):
        for p in self.subsession.get_players(): 
            p.total_payoff_ego= p.participant.vars['PGGSimple_payoff_bl'] + p.participant.vars['Dictator_payoff'] + p.participant.vars['Trust_payoff']
            p.participant.vars['total_payoff_ego']=p.total_payoff_ego
        vect = []
        for p in self.subsession.get_players():
            vect.append(int(-p.participant.vars['total_payoff_ego']))
        vect2=np.array(vect)
        vect2=vect2.astype(int)
        sorted_players= np.argsort(vect2, kind='quicksort', order=None) #axis=1,
        print(sorted_players)
        print(vect2)
        i=0
        for p in self.subsession.get_players():
            p.rankpos=sorted_players[i]+1
            i=i+1 """
        