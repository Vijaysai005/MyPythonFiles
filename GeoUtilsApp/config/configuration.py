# !usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:44:30 2018

@author: vijayasai
"""

""" Configuration Module."""
class Configuration(object):

    def __init__(self):
        """ Mongo."""
        # Databases
        self.MONGO_TBT_DB="tbt_data"
        self.MONGO_PERSONALIZATION_DB="personalization"
        
        # Collections in databases
        self.MONGO_ROUTE_COLLECTION="google_routes"
        self.MONGO_HOST="localhost"
        self.MONGO_PORT=27017

        """" Google."""
        # Api key
        self.API_KEY="AIzaSyCMhFUOGH9jLY44y1edzxBLKlmoBOlp_GY"
