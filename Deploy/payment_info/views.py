# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


class PaymentInfo(Page):
    def before_next_page(self):
        self.group.set_total_payoff() 
    
    def vars_for_template(self):
        participant = self.player.participant
        return {
            'participant': participant,
            'PGGSimple_participation' : participant.vars['PGGSimple_participation'],
            'PGGSimple_endowement': participant.vars['PGGSimple_endowement'],
            'PGGSimple_contribution_opt': participant.vars['PGGSimple_contribution_opt'],
            'PGGSimple_total_contribution_opt': participant.vars['PGGSimple_total_contribution_opt'],
            'PGGSimple_individual_share_opt': participant.vars['PGGSimple_individual_share_opt'],
            'PGGSimple_payoff_opt': participant.vars['PGGSimple_payoff_opt'],
            'PGGSimple_contribution_bl': participant.vars['PGGSimple_contribution_bl'],
            'PGGSimple_total_contribution_bl': participant.vars['PGGSimple_total_contribution_bl'],
            'PGGSimple_individual_share_bl': participant.vars['PGGSimple_individual_share_bl'],
            'PGGSimple_payoff_bl': participant.vars['PGGSimple_payoff_bl'],
            'PGGSimple_chosen_payoff': participant.vars['PGGSimple_chosen_payoff'],
            'Trust_sent_amount': participant.vars['Trust_sent_amount'],
            'Trust_sent_back_amount': participant.vars['Trust_sent_back_amount'],
            'Trust_tripled_amount': participant.vars['Trust_tripled_amount'],
            'Trust_sentbyother': participant.vars['Trust_sentbyother'],
            'Trust_sentbackbyother': participant.vars['Trust_sentbackbyother'],
            'Trust_payoff_if_A': participant.vars['Trust_payoff_if_A'],
            'Trust_payoff_if_B': participant.vars['Trust_payoff_if_B'],
            'Trust_payoff': participant.vars['Trust_payoff'],
            'Trust_is_dictator': participant.vars['Trust_is_dictator'],
            'Dictator_sent': participant.vars['Dictator_sent'],
            'Dictator_sentbyother': participant.vars['Dictator_sentbyother'],
            'Dictator_payoff_if_A': participant.vars['Dictator_payoff_if_A'],
            'Dictator_payoff_if_B': participant.vars['Dictator_payoff_if_B'],
            'Dictator_payoff': participant.vars['Dictator_payoff'],
            'Dictator_is_dictator': participant.vars['Dictator_is_dictator'],
            'Dictator_question_A': participant.vars['Dictator_question_A'],
            'Dictator_question_B': participant.vars['Dictator_question_B'],
            'bomb_payoff': participant.vars['bomb_payoff'],
            'total_payoff' : participant.vars['PGGSimple_payoff_bl'] + participant.vars['Dictator_payoff']  + participant.vars['Trust_payoff']  + participant.vars['bomb_payoff']
			}

'''class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True
    
#    def vars_for_template(self):
#        participant = self.player.participant
#        return {
#            'participant': participant,
#            'PGGSimple_payoff_bl': participant.vars['PGGSimple_payoff_bl'],
#            'Trust_payoff': participant.vars['Trust_payoff'],
#            'Dictator_payoff': participant.vars['Dictator_payoff'],
#            } '''

'''    def after_all_players_arrive(self):
        # sort players by 'score'
        # see python docs on sorted() function
        sorted_players = sorted(
            self.subsession.get_players(),
            key=lambda player: total_payoff)

        # chunk players into groups
        group_matrix = []
        ppg = Constants.players_per_group
        for i in range(0, len(sorted_players), ppg):
            group_matrix.append(sorted_players[i:i+ppg])

        # set new groups
        self.subsession.set_group_matrix(group_matrix)'''#ShuffleWaitPage,
	
class PaymentInfo2(Page):
    pass


page_sequence = [PaymentInfo,PaymentInfo2]
