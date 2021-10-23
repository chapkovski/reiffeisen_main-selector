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
    def is_displayed(self):
        return self.subsession.round_number == 1

class Decision(Page):
    form_model = 'player'
    form_fields = ['volatility', ]
    live_method = 'register_event'
    def vars_for_template(self):
        vol = [0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
        dt = [dict(volatility=i, data=self.player.chart_generator(i)) for i in vol]
        return dict(data=dt)

    def before_next_page(self):
        self.player.generate_data()





class Trade(Page):
    live_method = 'register_event'
    form_fields = ['exit_price']
    form_model = 'player'

    def before_next_page(self):
        if self.round_number == Constants.num_rounds:
            self.player.set_payoff()




class Results(Page):
    def vars_for_template(self):
        ratofret = round((self.player.exit_price - Constants.S)/Constants.S, 4)
        return dict(ratofret=ratofret)




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
