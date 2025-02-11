from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
One player decides how to divide a certain amount between himself and the other
player.

See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.

"""


class Constants(BaseConstants):
    name_in_url = 'dictator'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'dictator/Instructions.html'

    # Initial amount allocated to the dictator
    endowment = c(100)

    # test questions constants
    QuestionA_test_correct='C: 30 gettoni'
    QuestionB_test_correct='B: 70 gettoni'



class Subsession(BaseSubsession):
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
    	self.set_groups(list_of_lists)"""



class Group(BaseGroup):

    def set_payoffs(self):
        possible_choices = self.get_players()
        dictator_agent=random.choice(possible_choices)
        dictator_agent.is_dictator=True
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff_if_A = Constants.endowment - p1.sent
        p1.payoff_if_B = p2.sent
        p2.payoff_if_A = Constants.endowment - p2.sent
        p2.payoff_if_B = p1.sent
        p1.sentbyother=p2.sent
        p2.sentbyother= p1.sent
        if p1.is_dictator==True:
        	p1.payoff=p1.payoff_if_A
        	p2.payoff=p2.payoff_if_B
        else:
        	p2.payoff=p2.payoff_if_A
        	p1.payoff=p1.payoff_if_B
#            if p.id_in_group==1:#p==self.get_player_by_id(1):
#                other=self.get_player_by_id(2)
#            else:
#                other=self.get_player_by_id(1)
#            p.payoff_if_A = p.kept
#            p.payoff_if_B = Constants.endowment - other.kept
#            p.obtained= Constants.endowment - other.kept


class Player(BasePlayer):
	
    sent=models.CurrencyField(min=0, max=Constants.endowment)
    payoff_if_A=models.CurrencyField()
    payoff_if_B=models.CurrencyField()
    is_dictator= models.BooleanField(initial=False)
    question_A = models.CharField(widget=widgets.RadioSelect(), choices=[u'A: 20 gettoni', u'B: 70 gettoni', u'C: 30 gettoni'])
    question_B = models.CharField(widget=widgets.RadioSelect(), choices=[u'A: 30 gettoni',u'B: 70 gettoni', u'C: 10 gettoni'])
    sentbyother = models.CurrencyField()
    
    def setglobals(self):
        self.participant.vars['Dictator_sent']=self.sent
        self.participant.vars['Dictator_payoff_if_A']=self.payoff_if_A
        self.participant.vars['Dictator_payoff_if_B']=self.payoff_if_B
        self.participant.vars['Dictator_payoff']=self.payoff
        self.participant.vars['Dictator_is_dictator']=self.is_dictator
        self.participant.vars['Dictator_question_A']=self.question_A
        self.participant.vars['Dictator_question_B']=self.question_B
        self.participant.vars['Dictator_sentbyother']=self.sentbyother
        return(self.participant.vars)

    def question_A_correct(self):
        return (self.question_A == Constants.QuestionA_test_correct)

    def question_B_correct(self):
            return (self.question_B ==
                    Constants.QuestionB_test_correct)
    