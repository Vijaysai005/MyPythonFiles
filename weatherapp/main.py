
__author__ = 'Vijayasai S'

import json
import kivy
import random
kivy.require("1.10.0")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton
from kivy.factory import Factory
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore


def locations_args_converter(index, data_item):
    city, country = data_item.split("(")
    return {'location': (city, country[0:-1])}


class LocationButton(ListItemButton):
    location = ListProperty()


class CoverPage(BoxLayout):
    pass


class Conditions(BoxLayout):
    conditions = StringProperty()


class WeatherRoot(BoxLayout):

    current_weather = ObjectProperty()
    locations = ObjectProperty()

    def __init__(self, **kwargs):
        super(WeatherRoot, self).__init__(**kwargs)
        self.store = JsonStore("weather_store.json")
        if self.store.exists("locations"):
            current_location = self.store.get("locations")["current_location"]
            self.show_current_weather(current_location)

    def show_current_weather(self, location=None):
        self.clear_widgets()

        if self.current_weather is None:
            self.current_weather = CurrentWeather()

        if self.locations is None:
            self.locations = Factory.Locations()
            if self.store.exists("locations"):
                locations = self.store.get("locations")["locations"]
                self.locations.locations_list.adapter.data.extend(locations)

        if location is not None:
            self.current_weather.location = location
            if location not in self.locations.locations_list.adapter.data:
                self.locations.locations_list.adapter.data.append(location)
                self.locations.locations_list._trigger_reset_populate()
                self.store.put("locations", locations=list(
                    self.locations.locations_list.adapter.data), current_location=location)

        self.current_weather.update_weather()
        self.add_widget(self.current_weather)

    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(AddLocationForm())

    def show_locations(self):
        self.clear_widgets()
        self.add_widget(self.locations)

    def show_cover_page(self):
        self.clear_widgets()
        self.add_widget(CoverPage())


class AddLocationForm(BoxLayout):

    search_input = ObjectProperty()

    def __init__(self, *args):
        super(AddLocationForm, self).__init__(*args)
        self.args = args

    def search_location(self):
        # print "The user searched for '{}'".format(self.search_input.text)
        search_template = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=82f2c23dee62adf6047f8b083a4ddfff"
        search_url = search_template.format(self.search_input.text)
        request = UrlRequest(search_url, self.found_location)

    def found_location(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        cities = ["{} ({})".format(data["name"], data["sys"]["country"])]
        self.search_results.item_strings = cities
        self.search_results.adapter.data.clear()
        self.search_results.adapter.data.extend(cities)
        self.search_results._trigger_reset_populate()


class SnowConditions(Conditions):
    FLAKE_SIZE = 5
    NUM_FLAKES = 60
    FLAKE_AREA = FLAKE_SIZE * NUM_FLAKES
    FLAKE_INTERVAL = 1.0 / 30.0

    def __init__(self, **kwargs):
        super(SnowConditions, self).__init__(**kwargs)
        self.flakes = [[x * self.FLAKE_SIZE, 0] for x in range(self.NUM_FLAKES)]
        Clock.schedule_interval(self.update_flakes, self.FLAKE_INTERVAL)

    def update_flakes(self, time):
        for flake in self.flakes:
            flake[0] += random.choice([-1, 1])
            flake[1] -= random.randint(0, self.FLAKE_SIZE)
            if flake[1] <= 0:
                flake[1] = random.randint(0, int(self.height))

        self.canvas.before.clear()
        with self.canvas.before:
            widget_x = self.center_x - self.FLAKE_AREA / 2
            widget_y = self.pos[1]
            for x_flake, y_flake in self.flakes:
                x = widget_x + x_flake
                y = widget_y + y_flake
                Color(0.9, 0.9, 1.0)
                Ellipse(pos=(x, y), size=(self.FLAKE_SIZE, self.FLAKE_SIZE))


class CurrentWeather(BoxLayout):
    symbol = '\u00b0C'
    location = ListProperty(["Chennai", "IN"])
    conditions = StringProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()
    conditions_image = StringProperty()

    def update_weather(self):
        config = WeatherApp.get_running_app().config
        temp_type = config.getdefault("General", "temp_type", "metric").lower()
        if temp_type == "Imperial".lower():
            self.symbol = '\u00b0F'
        # print "The user searched for '{}'".format(self.search_input.text)
        weather_template = "http://api.openweathermap.org/data/2.5/weather?q={},{}&units={}&APPID=82f2c23dee62adf6047f8b083a4ddfff"
        self.location = ["".join(self.location[0:-4]),
                         "".join(self.location[-3:-1]), temp_type]
        weather_url = weather_template.format(*self.location)
        request = UrlRequest(weather_url, self.weather_retrieved)

    def weather_retrieved(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        # self.render_conditions(data['weather'][0]['description'])
        self.conditions = data['weather'][0]['description']
        self.temp = data['main']['temp']
        self.temp_min = data['main']['temp_min']
        self.temp_max = data['main']['temp_max']
        self.conditions_image = "http://openweathermap.org/img/w/{}.png".format(
            data['weather'][0]['icon'])

    # def render_conditions(self, conditions_description):
    #     if "clear" in conditions_description.lower():
    #         conditions_widget = Factory.ClearConditions()
    #     elif "snow" in conditions_description.lower():
    #         conditions_widget = SnowConditions()
    #     else:
    #         conditions_widget = SnowConditions()
    #     conditions_widget.conditions = conditions_description
    #     # self.conditions.clear_widgets()
    #     # self.conditions.add_widget(conditions_widget)


class WeatherApp(App):
    """docstring for WeatherApp"""

    def __init__(self, *args):
        super(WeatherApp, self).__init__(*args)
        self.args = args

    def build_config(self, config):
        config.setdefaults('General', {'temp_type': 'Metric'})

    def build_settings(self, settings):
        settings.add_json_panel("Weather Settings", self.config, data="""
            [
                {
                    "type": "options",
                    "title": "Temperature System",
                    "section": "General",
                    "key" : "temp_type",
                    "options": ["Metric", "Imperial"]
                }
            ]""")

    def on_config_change(self, config, section, key, value):
        if config is self.config and key == "temp_type":
            try:
                self.root.children[0].update_weather()
            except AttributeError:
                pass


if __name__ == "__main__":
    WeatherApp().run()
