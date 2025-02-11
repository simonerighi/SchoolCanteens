from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets
tripled. The trust game was first proposed by
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
"""


class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'trust/Instructions.html'

    # Initial amount allocated to each player
    endowment = c(100)
    multiplication_factor = 3

    # test questions constants
    QuestionA_test_correct='A: 90 gettoni'
    QuestionB_test_correct='B: 110 gettoni'


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

    def set_sent_amount(self):
    	for p in self.get_players():
    		if p==self.get_player_by_id(1):
    			other=self.get_player_by_id(2)
    		else:
    			other=self.get_player_by_id(1)
    		p.sentbyother=other.sent_amount
    		p.tripled_amount = other.sent_amount * Constants.multiplication_factor


    def set_payoffs(self):
    	possible_choices = self.get_players()
    	dictator_agent=random.choice(possible_choices)
    	dictator_agent.is_dictator=True
    	for p in self.get_players():
    		if p.sent_back_amount>p.tripled_amount:
    			p.sent_back_amount=p.tripled_amount
    	for p in self.get_players():
    		if p==self.get_player_by_id(1):
    			other=self.get_player_by_id(2)
    		else:
    			other=self.get_player_by_id(1)
    		p.payoff_if_A = Constants.endowment - p.sent_amount + other.sent_back_amount
    		p.payoff_if_B = other.sent_amount * Constants.multiplication_factor - p.sent_back_amount
    		p.sentbackbyother=other.sent_back_amount
    		if p.is_dictator==True:
    			p.payoff=p.payoff_if_A
    		else:
    			p.payoff=p.payoff_if_B

class Player(BasePlayer):
    
    sent_amount = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""Amount sent by P1""",
    )

    sentbyother= models.CurrencyField()

    tripled_amount= models.CurrencyField()

    sent_back_amount = models.CurrencyField(
        doc="""Amount sent back by P2""",
        min=c(0)#, max=tripled_amount
    )

    
    sentbackbyother= models.CurrencyField()
    
    payoff_if_A=models.CurrencyField()
    payoff_if_B=models.CurrencyField()
    is_dictator= models.BooleanField(initial=False)

    question_A = models.CharField(widget=widgets.RadioSelect(), choices=[u'A: 90 gettoni', u'B: 120 gettoni', u'C: 50 gettoni'])
    question_B = models.CharField(widget=widgets.RadioSelect(), choices=[u'A: 60 gettoni',u'B: 110 gettoni', u'C: 40 gettoni'])
    
    total_points=models.CurrencyField()
    def setglobals(self):
        self.participant.vars['Trust_sent_amount']=self.sent_amount
        self.participant.vars['Trust_sent_back_amount']=self.sent_back_amount
        self.participant.vars['Trust_tripled_amount']=self.tripled_amount
        self.participant.vars['Trust_sentbyother']=self.sentbyother
        self.participant.vars['Trust_sentbackbyother']=self.sentbackbyother
        self.participant.vars['Trust_payoff_if_A']=self.payoff_if_A
        self.participant.vars['Trust_payoff_if_B']=self.payoff_if_B
        self.participant.vars['Trust_payoff']=self.payoff
        self.participant.vars['Trust_is_dictator']=self.is_dictator
        return(self.participant.vars)


    def question_A_correct(self):
        return (self.question_A == Constants.QuestionA_test_correct)

    def question_B_correct(self):
            return (self.question_B ==
                    Constants.QuestionB_test_correct)
    
  
    
    """def role(self):
        return {1: 'A', 2: 'B'}[self.id_in_group]"""
