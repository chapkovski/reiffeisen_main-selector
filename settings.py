from os import environ

SESSION_CONFIGS = [
    dict(
        name='prototype1',
        display_name="prototype1 - round slider",
        num_demo_participants=1,
        app_sequence=['backend'],
        component_number=1
    ),
    dict(
        name='prototype2',
        display_name="prototype 2 - button",
        num_demo_participants=1,
        app_sequence=['backend'],
        component_number=2
    ),
    dict(
        name='prototype3',
        display_name=" prototype3 - Slider",
        num_demo_participants=1,
        app_sequence=['backend'],
        component_number=3
    ),
    dict(
        name='prototype4',
        display_name="prototype 4 - buttons then  Slider",
        num_demo_participants=1,
        app_sequence=['backend'],
        component_number=2,
        inner_slider=True,
    ),
    dict(
        name='prototype5',
        display_name="prototype 5 - combo",
        num_demo_participants=1,
        app_sequence=['backend'],
        component_number=4,

    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)
EXTENSION_APPS = ['backend']
# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'gtk67-^&4^!8rzlcvpbs!)iv8&n#^fy*dyas9z3#(i@0xf3g$q'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
