#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 11:25:08 IST 2018
@author: Vijayasais
"""

import sys
import time
from subprocess import call
from CricBuzzFeatures import CricBuzzFeatures

class CricBuzzMain(object):

	def get_current_scorecard(self):
		mycricbuzz = CricBuzzFeatures()
		mycricbuzz.get_current_scorecards()
	
	def get_current_commentary(self):
		mycricbuzz = CricBuzzFeatures()
		mycricbuzz.get_current_commentary()

	def main(self):
		while True:
			try:
				self.get_current_scorecard()
				time.sleep(20)
				call("clear")
				self.get_current_commentary()
				time.sleep(20)
				call("clear")
			except Exception:
				time.sleep(1)	
	

if __name__ == "__main__":
	instance = CricBuzzMain()
	instance.main()
