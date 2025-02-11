# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Test_Tablet(Page):
	form_model = models.Player
	form_fields = ['test_q','test_radio']
	
	def before_next_page(self):
		self.group.defin_num_participants() 

class Welcome(Page):
	pass

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    pass

class ResultsWaitPage_all(WaitPage):
	wait_for_all_groups = True
	
	def body_text(self):
		return "Lo studio proseguirà quando tutti i partecipanti avranno completato la fase di benvenuto. Si prega di attendere..."
	

page_sequence = [
    Test_Tablet,
    Welcome,
    ResultsWaitPage_all
]
