# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Contribute_bl(Page):

    form_model = models.Player
    form_fields = ['contribution_bl']


class ResultsWaitPage_bl(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs_bl()


class Results_bl(Page):
    pass

class Introduction_bl(Page):
    pass
    
class Instruction_bl(Page):
    pass

class Introduction_opt(Page):
    pass


class Choose_opt(Page):

    form_model = models.Player
    form_fields = ['participation']

    
class Contribute_opt(Page):

    form_model = models.Player
    form_fields = ['contribution_opt']

    def is_displayed(self):
        return self.player.participation == 'Si'


class ResultsWaitPage_opt(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs_opt()
        
class ResultsWaitPage_final(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()
        
class Pre_Results(Page):
    timeout_seconds=1         
    def before_next_page(self):
        self.player.setglobals()   

class Results_opt(Page):
    pass
    
class Results(Page):
    pass

class Introduction_all(Page):
	pass
	

class Introduction_group(Page):
	pass	

class Introduction_2d(Page):
	pass	
		
class ResultsWaitPage_all(WaitPage):
	wait_for_all_groups = True


class Question1(Page):

    template_name = 'PGG_Simple/Question.html'

    form_model = models.Player
    form_fields = ['value_project_test','individual_part_test', 'individual_gain']

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'PGG_Simple/Feedback.html'

    def vars_for_template(self):
        return {
            'num_q': 1,

        }

class Group_Formation(Page):
	pass
	
class Empty_write(Page):
	pass
	

page_sequence = [Group_Formation,
	Introduction_group,
	ResultsWaitPage_all,
	Question1,
	Feedback1,
    ResultsWaitPage_all,
    Contribute_bl,
    ResultsWaitPage_bl,
    ResultsWaitPage_final, 
    ResultsWaitPage_all,
    Pre_Results
]
