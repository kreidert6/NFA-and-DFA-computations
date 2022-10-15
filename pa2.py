# Name: pa1.py
# Author(s): Tyler Kreider and Julia Paley
# Date: 09/28/2022
# Description: A Python 3 program that simulates the computation of a DFA M on an input string s, and reports if s is accepted by M.

import sys

class DFA:
	""" Simulates a DFA """

	def __init__(self, filename):
		"""
		Initializes DFA from the file whose name is
		filename
		"""
		# open and read the file
		file = open(filename, 'r')
		self.states = file.readline().rstrip()
		self.alphabet = file.readline().rstrip()
		apostrophe = "'"
		self.transition_funcs = {}
		trans_val = True
		next_line = ''
		# loop through transition function values until start state
		while trans_val:
			next_line = file.readline().rstrip()
			# check if the line is a transition function
			if apostrophe in next_line:
				temp = next_line.split()
				self.transition_funcs[temp[0]+temp[1]]=temp[2]
			else:
				trans_val = False
		self.start_state = next_line
		self.accept_states = file.readline().rstrip().split()

	def simulate(self, str):
		""" 
		Simulates the DFA on input str.  Returns
		True if str is in the language of the DFA,
		and False if not.
		"""
		curr_state = self.start_state
		# loop through values in input string
		for i in range (len(str)):
			next_move = curr_state + "\'" + str[i]+ "\'"
			# confirm if next move is in the transition function
			if next_move in self.transition_funcs:
				curr_state = self.transition_funcs[next_move]
		# if last state is an accept state, return True, else return False
		if curr_state in self.accept_states:
			return True
		else:
			return False



	
