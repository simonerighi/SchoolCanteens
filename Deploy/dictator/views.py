from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass

class Group_Formation(Page):
    pass

class Offer(Page):
    form_model = models.Player
    form_fields = ['sent']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
   pass
   
class Question1(Page):

    template_name = 'dictator/Question.html'

    form_model = models.Player
    form_fields = ['question_A','question_B']

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'dictator/Feedback.html'

    def vars_for_template(self):
        return {
            'num_q': 1,

        }

class ResultsWaitPage_all(WaitPage):
    wait_for_all_groups = True

class Pre_Results(Page):
    timeout_seconds=1         
    def before_next_page(self):
        self.player.setglobals()   

page_sequence = [
    Group_Formation,
    Introduction,
    ResultsWaitPage_all,
    Question1,
    Feedback1,
    ResultsWaitPage_all,
    Offer,
    ResultsWaitPage,
#    Results,
    Pre_Results,
    ResultsWaitPage_all
]
