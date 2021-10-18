from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import json
from pprint import pprint


class Instructions(Page):
    def is_displayed(self):
        return self.round_number==1


class Instructions2(Page):
    def is_displayed(self):
        return self.round_number == 1



class Decision(Page):
    form_model = 'player'
    form_fields = ['volatility', ]

    def vars_for_template(self):
        vol = [0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
        dt = [dict(volatility=i, data=self.player.chart_generator(i)) for i in vol]
        return dict(data=dt)

    def before_next_page(self):
        self.player.generate_data()


class Trade(Page):
    live_method = 'register_event'
    form_model = 'player'
    form_fields = ['exit_price']

page_sequence = [
    Instructions,
    Instructions2,
    Decision,
    Trade
]
