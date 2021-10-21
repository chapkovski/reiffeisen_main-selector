from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import json
from pprint import pprint


class Intro(Page):
#    @staticmethod
    def is_displayed(self):
        return self.subsession.round_number == 1


class Instructions_slider(Page):
#    @staticmethod
    def is_displayed(self):
        return self.subsession.round_number == 1

#class Instructions1(Page):
#    @staticmethod
#    def is_displayed(self):
#        return self.subsession.round_number == 1

#class Instructions2(Page):
#    @staticmethod
#    def is_displayed(self):
#        return self.subsession.round_number == 1
    # def vars_for_template(self):
    #     return dict(<img src="{{ static 'reif_main-selector/img2high.jpg' }}"/>,  <img src="{{ static 'reif_main-selector/img1low.jpg' }}"/>)

class Decision(Page):
    form_model = 'player'
    form_fields = ['volatility', ]
    def vars_for_template(self):
        vol = [0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
        dt = [dict(volatility=i, data=self.player.chart_generator(i)) for i in vol]
        return dict(data=dt)

    def before_next_page(self):
        self.player.generate_data()

#    @staticmethod
#    def before_next_page(self):



class Trade(Page):
    live_method = 'register_event'
    form_fields = ['exit_price']
    form_model = 'player'

    def before_next_page(self):
        if self.round_number == Constants.num_rounds:
            self.player.set_payoff()
    # def before_next_page(self):
    #     import random
    #
    #     participant = self.player.participant
    #     if self.player.round_number == Constants.num_rounds:
    #         random_round = random.randint(1, Constants.num_rounds)
    #         self.participant.selected_round = random_round
    #         player_in_selected_round = self.player.in_round(random_round)
    #         self.player.payoff = player_in_selected_round.player.exit_price

            # participant.selected_round = random_round
            # player_in_selected_round = player.in_round(random_round)
            # player.payoff = Constants.endowment - player_in_selected_round.give_amount

#     def creating_session(self):
#         import random
# #        participant = self.player.participant
#         if self.round_number == 1:
#             self.player.random_round = random.randint(1, Constants.num_rounds)
#             self.player.selected_round = self.player.random_round
#             self.player.player_in_selected_round = self.player.in_round(self.player.random_round)
#             self.player.payoff = self.player.exit_price
#             self.session.vars['paying_round'] = self.player.random_round



class Results(Page):
    def vars_for_template(self):
        player = self.player
        ratofret = round((self.player.exit_price - Constants.S)/Constants.S, 4)
        return dict(ratofret=ratofret)

    # def live_method(player, data):
    #     t = data['type']
    #     if t == 'offer':
    #         other_player = data['to']
    #         response = {
    #             'type': 'offer',
    #             'from': player.id_in_group,
    #             'value': data['value']
    #             }
    #         return {other_player: response}


class NextPage(Page):
    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds


class FinalResults(Page):
#    @staticmethod

    def is_displayed(self):
        return self.player.round_number == Constants.num_rounds

#    @property
    def vars_for_template(self):
        paying_round = self.subsession.session.vars['paying_round']
        final_payoff = self.player.final_payoff #in_round(self.player.paying_round).exit_price
        return dict(pay_round=paying_round, final_payoff=final_payoff)




page_sequence = [
    # Intro,
    # Instructions_slider,
#    Instructions1,
#    Instructions2,
    Decision,
    Trade,
    Results,
    NextPage,
    FinalResults,
]
