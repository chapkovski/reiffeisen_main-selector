# Raif project

This project consists of two modules (`backend` and `frontend`) plus a small survey (`reif_survey_0`) unrelated to a mai
part.

Backend is built using [oTree](https://otree.readthedocs.io/en/latest/), which is just a Django add-on for building 
behavioral experiments and surveys. So at its core it uses Django ORM, and [Django Channels](https://channels.readthedocs.io/en/stable/) for interacting 
with a user in real time via websockets.

The description of the frontend is available in the `README` file located in the `front` folder.

On the backend the `pages.py` defines the series of screens that a person gets through: Introduction, more detailed 
Instructions, choosing the volatility level (page `Decision`), and a trading session (page `Trade`). When a
trading session is over the results are shown (page `Results`). This process is repeated for several rounds (the number
of rounds is defined in `main.models.Constants.num_rounds`). Finally final results (Page `FinalResults`) are shown where
we inform a user which round was randomly selected for payment.

The page 'Decision' is rendered using frontend app `Selector` from frontend. 
The page 'Trade' is rendered using frontend app 'Main' from frontend. See details in `front->readme`.

The data for price updates is generated in `main.player.merton_jump_paths` method.

The module that registers all events that occur in 'Decision' and 'Trade' pages is located in `main.player.register_event` 
method. This method takes the data and stores it as an `Event` db instance, together with player id, and timestamp.

The export moodule that converts the Event instances to the excel file is located in `main.views.PandasExport`. It
simply converts the database queryset of the Event data table to the excel file and returns it to the experimenter through 
the admin interface of oTree (in 'Data' menu -> Third-party exports).





