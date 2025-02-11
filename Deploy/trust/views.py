from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from . import models
from .models import Constants


class Introduction(Page):
    pass

class NowB(Page):
    pass

class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = models.Player
    form_fields = ['sent_amount']

    """def is_displayed(self):
        return self.player.id_in_group == 1"""


class SendBackWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_sent_amount()

class Group_Formation(Page):
    pass

class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = models.Player
    form_fields = ['sent_back_amount']

    """def is_displayed(self):
        return self.player.id_in_group == 2"""

    def vars_for_template(self):
        return {
                'tripled_amount': self.player.tripled_amount,
                'prompt':
                    'Quanti gettoni vuoi inviare al giocatore A (tra 0 e %s):' % self.player.tripled_amount}

#    def sent_back_amount_max(self):
#        return self.sent_amount * Constants.multiplication_factor


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

class Question1(Page):

    template_name = 'trust/Question.html'

    form_model = models.Player
    form_fields = ['question_A','question_B']

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'trust/Feedback.html'

    def vars_for_template(self):
        return {
            'num_q': 1,

        }

class Results(Page):
    """This page displays the earnings of each player"""

    def vars_for_template(self):
        return {
            'tripled_amount': self.player.sent_amount * Constants.multiplication_factor
        }


class Pre_Results(Page):
    timeout_seconds=1         
    def before_next_page(self):
        self.player.setglobals()   

class ResultsWaitPage_all(WaitPage):
    wait_for_all_groups = True
    
page_sequence = [
    Group_Formation,
    Introduction,
    ResultsWaitPage_all,
    Question1,
    Feedback1,
    ResultsWaitPage_all,
    Send,
    SendBackWaitPage,
    NowB,
    SendBack,
    ResultsWaitPage,
#    Results,
    Pre_Results,
    ResultsWaitPage_all
]
