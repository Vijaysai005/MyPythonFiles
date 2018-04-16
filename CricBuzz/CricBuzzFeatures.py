#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:07:23 IST 2018
@author: Vijayasais
"""

import sys
from pycricbuzz import Cricbuzz
from CardPrinter import CardPrinter

class CricBuzzFeatures(object):

	def __init__(self):
		self.card_printer = CardPrinter()
		self.cricket = Cricbuzz()
		self.matches = self.cricket.matches()

	def get_scorecard(self, match_id):
		scorecard = self.cricket.scorecard(match_id)
		return scorecard

	def get_commentary(self, match_id):
		commentary = self.cricket.commentary(match_id)
		return commentary

	def get_all_match_ids(self):
		match_ids = []
		for matches in self.matches:
			match_ids.append(matches["id"])
		return match_ids

	def get_all_inprogress_match_ids(self):
		inprogress_match_ids = []
		for matches in self.matches:
			if matches["mchstate"] == "inprogress":
				inprogress_match_ids.append(matches["id"])
		return inprogress_match_ids

	def ger_all_complete_and_inprogress_match_ids(self):
		inprogress_and_complete_match_ids = []
		for matches in self.matches:
			if matches["mchstate"] == "inprogress" or matches["mchstate"] == "complete":
				inprogress_and_complete_match_ids.append(matches["id"])
		return inprogress_and_complete_match_ids

	def get_all_inprogress_match_ids(self):
		inprogress_match_ids = []
		for matches in self.matches:
			if matches["mchstate"] == "inprogress":
				inprogress_match_ids.append(matches["id"])
		return inprogress_match_ids

	def get_all_scorecards(self):
		for match_id in self.ger_all_complete_and_inprogress_match_ids():
			self.card_printer.scorecard_printer(self.get_scorecard(match_id))

	def get_current_scorecards(self):
		for match_id in self.get_all_inprogress_match_ids():
			complete_scorecard = self.get_scorecard(match_id)
			matchinfo = complete_scorecard.get("matchinfo", {})
			match_between = matchinfo.get("mchdesc")
			match_status = matchinfo.get("status")
			source = matchinfo.get("srs")
			match_num = matchinfo.get("mnum")
			sys.stdout.write("{} - {}     Status: {}\n".format(source, match_num, match_status))
			sys.stdout.write("************** {} **************\n".format(match_between))
			
			scorecard = complete_scorecard.get("scorecard")
			len_scorecard = len(scorecard)
			if len_scorecard == 2:
				first_innings = scorecard[1]
				second_innings = scorecard[0]
				self.card_printer.scorecard_printer(second_innings)
				sys.stdout.write("\n")
				self.card_printer.scorecard_printer(first_innings)
			elif len_scorecard == 1:
				first_innings = scorecard[0]
				self.card_printer.scorecard_printer(first_innings)

	def get_current_commentary(self):
		for match_id in self.get_all_inprogress_match_ids():
			commentary = self.get_commentary(match_id)
			only_commentary = commentary.get("commentary")
			self.card_printer.commentary_printer(only_commentary)


if __name__ == "__main__":
	pass
