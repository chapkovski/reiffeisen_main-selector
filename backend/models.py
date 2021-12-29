from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from django.utils.dateformat import format
from django.utils import timezone
from django.db import models as djmodels
import numpy as np
from scipy.stats import norm
import random
import json
from pprint import pprint

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'backend'
    players_per_group = None
    num_rounds = 10
    trading_day_min = 3
    freq = 6
    length = int(trading_day_min * 240 / 6)
    hetto = 1
    dt = 1

    S = 100  # current stock price
    T = 1  # time to maturity
    lam = 2  # intensity of jump i.e. number of jumps per annum
    steps = 250  # time steps
    steps1 = 75
    Npaths = 1  # number of paths to simulate
    sigma = .48  # annual standard deviation , for wiener process
    m = -0.02  # mean of jump size
    r = 0.06  # risk free rate
    v = 0.03  # sigma / 10  # standard deviation of jump


class Subsession(BaseSubsession):
    paying_round = models.IntegerField()

    def creating_session(self):
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    income = models.FloatField(min=3, max=25)
    volatility = models.FloatField(min=0.01, max=0.50)
    drawdown = models.FloatField(min=2, max=4, initial=3)
    data = models.LongStringField()
    current_position = models.IntegerField(initial=1)
    exit_price = models.FloatField()
    final_payoff = models.FloatField()
    paying_round = models.IntegerField()

    def chart_generator(self, vol):
        sizesam = (Constants.steps1, 50)
        dift = Constants.T / Constants.steps1
        poi_rv = np.multiply(np.random.poisson(Constants.lam * dift, size=sizesam),
                             np.random.normal(-vol * 3, Constants.v, size=sizesam)).cumsum(axis=0)

        geo = np.cumsum(((Constants.r - (vol) ** 2 / 2
                          - Constants.lam * (-vol * 2 + Constants.v ** 2 * 0.5)) * dift
                         + vol * np.sqrt(dift) * np.random.normal(size=sizesam)), axis=0)
        _dt = np.round_(np.exp(geo + poi_rv) * Constants.S, 3)
        data = np.transpose(_dt).tolist()
        return data

    def merton_jump_paths(self):
        size = (Constants.steps, Constants.Npaths)
        dift = Constants.T / Constants.steps
        poi_rv = np.multiply(np.random.poisson(Constants.lam * dift, size=size),
                             np.random.normal(-self.volatility * 3, Constants.v, size=size)).cumsum(axis=0)
        geo = np.cumsum(((Constants.r - (self.volatility) ** 2 / 2
                          - Constants.lam * (-(self.volatility) * 2 + Constants.v ** 2 * 0.5)) * dift
                         + self.volatility * np.sqrt(dift) * np.random.normal(size=size)), axis=0)

        return np.round_(np.exp(geo + poi_rv) * Constants.S, 3).tolist()

    def generate_data(self):
        data = [j for i in self.merton_jump_paths() for j in i]

        self.data = json.dumps(data)

    def get_data(self):
        return json.loads(self.data)

    def get_drawdown(self):
        return Constants.S * (1 - self.drawdown / 10)

    def register_event(self, data):
        timestamp = timezone.now()

        self.events.create(
            owner=self,
            timestamp=timestamp,
            unix_timestamp=format(timestamp, 'U'),
            name=data.pop('name', ''),
            body=json.dumps(data),
            current_price=data.get('currentPrice'),
            price_index=data.get('priceIndex'),
            slider_value=data.get('sliderValue'),
            secs_since_round_starts=data.get('secs_since_round_starts'),
            clicked_volatility=data.get('volatility')
        )

        return {
            self.id_in_group: dict(timestamp=timestamp.strftime('%m_%d_%Y_%H_%M_%S'), action='getServerConfirmation')}

    def set_payoff(self):
        self.paying_round = self.session.vars['paying_round']
        self.final_payoff = self.in_round(self.paying_round).exit_price
        self.payoff = self.final_payoff


class Event(djmodels.Model):
    class Meta:
        ordering = ['timestamp']
        get_latest_by = 'timestamp'

    owner = djmodels.ForeignKey(to=Player, on_delete=djmodels.CASCADE, related_name='events')
    name = models.StringField()
    timestamp = djmodels.DateTimeField(null=True, blank=True)
    unix_timestamp = models.IntegerField()
    body = models.StringField()
    current_price = models.FloatField()
    price_index = models.IntegerField()
    slider_value = models.IntegerField()
    secs_since_round_starts = models.IntegerField()
    clicked_volatility = models.FloatField()
