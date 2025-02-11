# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

# </standard imports>

author = 'Your name here'

doc = """
Your app description
"""

class Constants:
    name_in_url = 'PGG_Simple'
    players_per_group = 4
    num_rounds = 1

    # define more constants here
    endowement = c(40)
    efficiency_factor=2
    
    # test questions constants
    value_project_test_correct='B: 0+20+30+10=60x2=120'
    individual_part_test_correct='B: 120:4=30'
    individual_gain_correct='B: 120:4=30 + tuoi gettoni nel portafoglio pari a 30 (= 40 iniziali - 10 messi da te nel progetto comune). Totale 60.'

class Subsession(otree.models.BaseSubsession):
    def creating_session(self):
        self.group_randomly()

"""    def before_session_starts(self):
    	list_of_lists = []
    	players = self.get_players()
    	num_players=len(self.get_players())
    	vct_players=range(0,num_players)
    	#random.shuffle(vct_players)
    	random.shuffle(players)
    	startat=0
    	endat=Constants.players_per_group-1
    	for iii in self.get_groups():
        	#pos_group=vct_players[startat:endat] #group_players=[] #for iii in len(pos_group): group_players.append(pos_group[iii])
        	group_players=players[startat:endat+1]
        	startat=startat+Constants.players_per_group
        	endat=endat+Constants.players_per_group #fill_in=play(vct_players[startat:endat]) #group.set_players(fill_in)
        	list_of_lists.append(group_players)	
    	self.set_groups(list_of_lists) """


class Group(otree.models.BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_contribution_bl = models.CurrencyField()
    individual_share_bl = models.CurrencyField()
    total_contribution_opt = models.CurrencyField()
    individual_share_opt = models.CurrencyField()
    number_participants_opt=models.CurrencyField()

    def set_payoffs_bl(self):  
    	for p in self.get_players(): 
    		for case in switch(p.contribution_bl): 
    			if case('0 gettoni'): 
    				p.contrib_bl = 0
    				break
    			if case('10 gettoni'): 
    				p.contrib_bl = 10
    				break
    			if case('20 gettoni'): 
    				p.contrib_bl = 20
    				break
    			if case('30 gettoni'): 
    				p.contrib_bl = 30
    				break
    			if case('40 gettoni'): 
    				p.contrib_bl = 40
    				break
    
    	self.total_contribution_bl = sum([p.contrib_bl for p in self.get_players()])
    	self.individual_share_bl = ( self.total_contribution_bl * Constants.efficiency_factor / Constants.players_per_group )
    	for p in self.get_players():
    		p.payoff_bl = ( Constants.endowement - p.contrib_bl + self.individual_share_bl )


    def set_payoffs(self):
        for p in self.get_players():
        	p.chosen_payoff=random.choice(['bl','bl'])
        	if p.chosen_payoff=='bl': p.payoff=p.payoff_bl
        	else: p.payoff=p.payoff_opt

    def set_payoffs_opt(self):
        self.total_contribution_opt = 0
        yesparticipants=[]
        nonparticipants=[]
        
        for p in self.get_players():
            if p.participation == 'Si':
            	for case in switch(p.contribution_opt):
            		if case('0 gettoni'): 
            			p.contrib_opt = 0
            			break
            		if case('10 gettoni'): 
            			p.contrib_opt = 10
            			break
            		if case('20 gettoni'): 
            			p.contrib_opt = 20
            			break
            		if case('30 gettoni'): 
            			p.contrib_opt = 30
            			break
            		if case('40 gettoni'): 
            			p.contrib_opt = 40
            			break
            		
            	self.total_contribution_opt = self.total_contribution_opt + p.contrib_opt
            	yesparticipants=yesparticipants + [p]
            else:
            	nonparticipants=nonparticipants + [p]
        
        number_participants_opt=len(yesparticipants) # THIS DOESNT WORK FOR THE TIME BEING.
        
        if len(yesparticipants)>0:
            self.individual_share_opt = ( self.total_contribution_opt * Constants.efficiency_factor / len(yesparticipants) )

        for p in yesparticipants:
            p.payoff_opt = ( Constants.endowement - p.contrib_opt + self.individual_share_opt )
            
        for p in nonparticipants: #p.contribution = 0
            p.payoff_opt = Constants.endowement





class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    payoff_opt = models.CurrencyField ()
    payoff_bl = models.CurrencyField ()
    chosen_payoff=models.CharField()
    contrib_opt = models.CurrencyField ()
    contrib_bl = models.CurrencyField ()
    #contribution_bl = models.CurrencyField (choices=currency_range(0, Constants.endowement,c(10)))
    contribution_bl = models.CharField(widget=widgets.RadioSelect(), choices=[u'0 gettoni', u'10 gettoni', u'20 gettoni', u'30 gettoni', u'40 gettoni'])
    contribution_opt = models.CharField(widget=widgets.RadioSelect(),choices=[u'0 gettoni', u'10 gettoni', u'20 gettoni', u'30 gettoni', u'40 gettoni'])
    participation = models.CharField(initial=None,
                                     choices=['Si', 'No'],
                                     verbose_name='Vuoi Partecipare?',
                                     widget=widgets.RadioSelect())

    value_project_test = models.CharField(widget=widgets.RadioSelect(), choices=[u'A: 0+20+30+10=60', u'B: 0+20+30+10=60x2=120'])
    individual_part_test = models.CharField(widget=widgets.RadioSelect(), choices=[u'A: 60:4=15',u'B: 120:4=30'])
    individual_gain = models.CharField(widget=widgets.RadioSelect(), choices=[u'A: 120:4=30',u'B: 120:4=30 + tuoi gettoni nel portafoglio pari a 30 (= 40 iniziali - 10 messi da te nel progetto comune). Totale 60.'])

    def setglobals(self):
        self.participant.vars['PGGSimple_participation']=self.participation
        self.participant.vars['PGGSimple_endowement']=Constants.endowement
        self.participant.vars['PGGSimple_contribution_opt']=self.contribution_opt
        self.participant.vars['PGGSimple_total_contribution_opt']=self.group.total_contribution_opt
        self.participant.vars['PGGSimple_individual_share_opt']=self.group.individual_share_opt
        self.participant.vars['PGGSimple_payoff_opt']=self.payoff_opt
        self.participant.vars['PGGSimple_contribution_bl']=self.contribution_bl
        self.participant.vars['PGGSimple_total_contribution_bl']=self.group.total_contribution_bl
        self.participant.vars['PGGSimple_individual_share_bl']=self.group.individual_share_bl
        self.participant.vars['PGGSimple_payoff_bl']=self.payoff_bl
        self.participant.vars['PGGSimple_chosen_payoff']=self.chosen_payoff
        return(self.participant.vars)


    def is_value_project_test_correct(self):
        return (self.value_project_test == Constants.value_project_test_correct)

    def is_individual_part_test_correct(self):
            return (self.individual_part_test ==
                    Constants.individual_part_test_correct)
    
    def is_individual_gain_correct(self):
            return (self.individual_gain ==
                    Constants.individual_gain_correct)

    def role(self):
        if self.participation == 'Si': return 'part'
        else: return 'nopart'



# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False