from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import json
from pprint import pprint

class Instructions(Page):
    pass

class Instructions2(Page):
    pass
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



class Trade(Page):
    live_method = 'register_event'


page_sequence = [
    Instructions,
    Instructions2,
    Decision,
    Trade
]
