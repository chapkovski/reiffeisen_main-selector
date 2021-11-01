from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class invest(Page):
    form_model = 'player'
    form_fields = ['fb1_clarity',
                   'fb2_strategy',
                   'fb3_dropdown',
                   ]

class finprodnow(Page):
    form_model = 'player'
    form_fields = [
                   'debcard1',
                   'credcard1',
                   'conscred1',
                   'mortgcred1',
                   'bankacc1',
                   'bankdepo1',
                   'bankinv1',
                   'invest1',
        ]

class finprodfut(Page):
        form_model = 'player'
        form_fields = [
                   'debcard2',
                   'credcard2',
                   'conscred2',
                   'mortgcred2',
                   'bankacc2',
                   'bankdepo2',
                   'bankinv2',
                   'invest2',
            ]

class prefs(Page):
    form_model = 'player'
    form_fields = [
                   'invgoals',
                   'invgoals_other',
                   'inv_horiz',
                   'norm7_know',
                   'norm8_risk',
                   'norm9_debt',
                   'norm10_saving',
                   'norm11_invlott',
                   'norm11down_invlott',
                   'norm11up_invlott',
                   'riskat',
                   'management',
                   ]


class MyPage(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'field',
        'field_other',
        'family',
        'famember',
        'income',
        'budget',
        'budget_other',
        'satis',
        'expect',
        'trust',
        'freedom',
        ]

    def before_next_page(self):
        self.player.set_payoff()

class Results_Toloka(Page):
    pass

page_sequence = [
    invest, finprodnow, finprodfut, prefs, MyPage, Results_Toloka, #, Yourself #, polit, City,
]
