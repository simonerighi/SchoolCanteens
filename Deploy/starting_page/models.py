# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
import numpy as np
import math

# </standard imports>

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'starting_page'
    players_per_group = None
    num_rounds = 1

    # define more constants here


class Subsession(BaseSubsession):
    pass
    




class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    
    def defin_num_participants(self):
        for p in self.get_players():
            p.totalnumparticipants=self.session.num_participants
            p.first_third_start=1
            p.first_third_end=math.ceil(p.totalnumparticipants/3)
            p.second_third_start=p.first_third_end+1
            p.second_third_end=p.first_third_end+math.ceil(p.totalnumparticipants/3)

    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = 0 # change to whatever the payoff should be


class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    test_q = models.PositiveIntegerField ()
    test_radio = models.CharField(widget=widgets.RadioSelect(), choices=[u'Mi trovo di fronte ad un computer', u'Mi trovo di fronte ad un tablet', u'Mi trovo di fronte ad un telefono'])

    totalnumparticipants = models.PositiveIntegerField ()
    first_third_start = models.PositiveIntegerField ()
    first_third_end = models.PositiveIntegerField ()
    second_third_start  = models.PositiveIntegerField ()
    second_third_end  = models.PositiveIntegerField ()
