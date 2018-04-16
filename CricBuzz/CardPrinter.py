#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:09:24 IST 2018
@author: Vijayasais
"""

import sys

class CardPrinter(object):

	def __init__(self):
		pass

	def scorecard_printer(self, scorecard):
		batteam = scorecard.get("batteam")
		runs = scorecard.get("runs")
		wickets = scorecard.get("wickets")
		overs = scorecard.get("overs")
		sys.stdout.write("{} Innings  {}-{}({})\n".format(batteam, runs, wickets, overs))
		sys.stdout.write("*****************************************\n")

		string = "{:<25} {:<40} {:<6} {:<6} {:<6} {:<6}\n".format(
			"Batsman", " ", "Runs", "Balls", "Fours", "Sixes")
		sys.stdout.write(string)
		batcard = scorecard.get("batcard")
		for batsmen in batcard:
			name = batsmen.get("name")
			dismissal = batsmen.get("dismissal")
			if dismissal == "not out":
				dismissal = "batting"
			runs = batsmen.get("runs")
			balls = batsmen.get("balls")
			fours = batsmen.get("fours")
			sixes = batsmen.get("six")
			string = "{:<25} {:<40} {:<6} {:<6} {:<6} {:<6}\n".format(
				name, dismissal, runs, balls, fours, sixes)
			sys.stdout.write(string)
		string = "{:<25} {:<20} {:<6} {:<8} {:<6} {:<6}\n".format(
			"Bowler", " ", "Overs", "Maidens", "Runs", "Wickets")
		sys.stdout.write("*****************************************\n")
		sys.stdout.write(string)
		bowlcard = scorecard.get("bowlcard")
		for bowler in bowlcard:
			name = bowler.get("name")
			wickets = bowler.get("wickets")
			overs = bowler.get("overs")
			maidens = bowler.get("maidens")
			runs = bowler.get("runs")
			string = "{:<25} {:<20} {:<6} {:<8} {:<6} {:<6}\n".format(
				name, " ", overs, maidens, runs, wickets)
			sys.stdout.write(string)

	def commentary_printer(self, commentary):
		for comm in commentary:
			sys.stdout.write("{}\n\n".format(comm))
		pass



if __name__ == "__main__":
	pass
