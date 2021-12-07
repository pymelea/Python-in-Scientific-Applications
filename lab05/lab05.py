# Call this script: bokeh serve ./lab05.py --show

from bokeh.io import curdoc
from bokeh.plotting import figure, row
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider
from collections import Counter
import pandas as pd
import numpy as np


# Function to load and draw bokeh histogram about age responders
def age_histogram():

    # load data about responders age
    data_age = pd.read_csv("data-07.csv")
    ages = data_age["Age"]
    hist, edges = np.histogram(ages, density=False, bins=50)

    hist_plot = figure(background_fill_color="#fafafa")
    hist_plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
                   fill_color="navy", line_color="white", alpha=0.5)

    hist_plot.title.text = 'Age of responders according to Stackoverflow in 2019'
    hist_plot.title.align = 'center'
    hist_plot.title.text_color = 'black'
    hist_plot.title.text_font_size = '15px'
    hist_plot.xaxis.axis_label = 'Responder Age'
    hist_plot.yaxis.axis_label = 'Counts'
    hist_plot.y_range.start = 0

    return hist_plot


# Function to load data about responders languages from csv
def load_lang_data():

    # load data about languages from csv
    data_lang = pd.read_csv("data-03.csv")
    lang_responses = data_lang["LanguagesWorkedWith"]
    language_counter = Counter()

    # count responses
    for response in lang_responses:
        language_counter.update(response.split(";"))

    return language_counter


# Function to process data
def process_data(slider_value: int, language_counter: Counter):

    # counter.most_common returns list of tuples so we unzip it
    language, popularity = zip(*language_counter.most_common(slider_value))
    # and reverse because we want the most popular at the top
    language = tuple(reversed(language))
    popularity = tuple(reversed(popularity))
    # create source to bokeh
    source = ColumnDataSource(dict(x=popularity, y=language))

    return source


# Fuction to reload data on dashboard
def update_data(attr, old, new):

    new_source = process_data(new, language_counter)
    source.data = dict(new_source.data)
    plot.y_range.factors = new_source.data['y']


# ---------------------------------------------------------------------------
# Initial slider value
slider_value = 10
language_counter = load_lang_data()
source = process_data(slider_value, language_counter)

# Slider
offset = Slider(title='Top Languages', value=10, start=10,
                end=20, step=1)
offset.on_change('value', update_data)

# Plot
plot = figure(y_range=source.data['y'], background_fill_color="#fafafa")
plot.hbar(right='x', y='y', source=source,
          height=0.4, color='blue', fill_alpha=0.5)
plot.title.text = 'Most popular languages according to Stackoverflow in 2019'
plot.title.align = 'center'
plot.title.text_color = 'black'
plot.title.text_font_size = '15px'
plot.xaxis.axis_label = 'Number of people using this'
# ---------------------------------------------------------------------------
# Histogram
hist_plot = age_histogram()
# ---------------------------------------------------------------------------

# Curdoc
curdoc().add_root(row(hist_plot, plot, offset, width=900))
curdoc().title = 'Stackoverflow Poll'
