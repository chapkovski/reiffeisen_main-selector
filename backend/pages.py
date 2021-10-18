from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import json
from pprint import pprint


class Intro(Page):
#    @staticmethod
    def is_displayed(self):
        return self.subsession.round_number == 1


class Instructions(Page):
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



class Trade(Page):
    live_method = 'register_event'

class Results(Page):
    pass
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

page_sequence = [
    Intro,
    Instructions,
#    Instructions1,
#    Instructions2,
    Decision,
    Trade,
    Results,
]
