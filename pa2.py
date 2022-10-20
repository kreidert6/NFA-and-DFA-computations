# Name: pa1.py
# Author(s): Tyler Kreider and Julia Paley
# Date: 09/28/2022
# Description: A Python 3 program that simulates the computation of a DFA M on an input string s, and reports if s is accepted by M.

from re import search
import sys
from tracemalloc import start

class NFA:
	""" Simulates a DFA """

	def __init__(self, filename):
		"""
		Initializes DFA from the file whose name is
		filename
		"""
		# open and read the file
		file = open(filename, 'r')
		self.states = file.readline().rstrip()
		self.alphabet = file.readline().rstrip()+"e"
		apostrophe = "'"
		self.NFAtransition_funcs = {}
		trans_val = True
		next_line = ''
		# loop through transition function values until start state
		while trans_val:
			
			next_line = file.readline().rstrip()
			# check if the line is a transition function
			if apostrophe in next_line:
				temp = next_line.split()
				
				#replace the key value to include new state
				if (temp[0] + temp[1]) in self.NFAtransition_funcs:
					self.NFAtransition_funcs.get(temp[0]+temp[1]).append(temp[2])

				#first dictionary entry for this transition function
				else:
					temp_value_list =[]
					temp_value_list.append(temp[2])
					self.NFAtransition_funcs[temp[0]+temp[1]]= temp_value_list

			else:
				trans_val = False

		

		#blank_line = file.readline() #step 4
		self.start_state = file.readline().rstrip() #step 5

		self.DFAtransition_funcs = {}
		self.new_state_list = []
		self.total_states_to_loop = []
		self.visited_states = []
		

		self.accept_states = file.readline().rstrip().split()
		#toDFA(self)
		print(self.alphabet)
		print(self.NFAtransition_funcs)



	# def generate_new_states(self, current_state, i):
		
	# 		for x in range(current_states.length)
	# 		search_key = (self.current_state) + "'" + self.alphabet[i]

			
	# 		if search_key in self.NFAtransition_funcs:
	# 				new_state_list = self.NFAtransition_funcs.get(search_key)
	# 				#add new state to new DFA dictionary 
	# 				self.DFA_dict[search_key] = new_state_list
		
		



	def toDFA(self, dfa_filename):
		"""
		Converts the "self" NFA into an equivalent DFA
		and writes it to the file whose name is dfa_filename.
		The format of the DFA file must have the same format
		as described in the first programming assignment (pa1).
		This file must be able to be opened and simulated by your
		pa1 program.

		This function should not read in the NFA file again.  It should
		create the DFA from the internal representation of the NFA that you 
		created in __init__.
		"""

		#get start states including epsilons 
		start_states = []
		start_states.append(self.start_state)
		temp = self.start_state + "'e'" 
		if temp in self.NFAtransition_funcs:
			
			epsilon_additions = self.NFAtransition_funcs[temp]
			start_states = list(set(start_states) | set(epsilon_additions))
		self.total_states_to_loop.append(start_states)
		print(start_states)
		start_states.sort( key = int)
		
		print("NFA start state - " + self.start_state)
		print(start_states)


		self.generate_new_states()








		# #we need to initialize start state of DFA 
		# #first_state = self.start_state + dfa_filename + "'" + self.alphabet[0] 
 		
		# #make new states of new DFA
		
		# self.new_state_list = []
		# #for y in range(self.states):
		# for i in range(self.alphabet):
		# 		#new_state_list = []
		# 	current_state = 4
		# 	self.generate_new_states(current_state, i)

		
				



					
					
		
		# return 



	def generate_new_states(self):
		#destinations = []
		print(self.alphabet)
		while len(self.total_states_to_loop) > 0:
			
			current_state = self.total_states_to_loop.pop()
			if current_state not in self.visited_states:
				self.visited_states.append(current_state)
				for i in range(len(self.alphabet)):
					destinations = []
					for x in range(len(current_state)):
						print(self.alphabet[i])
						search_key = current_state[x] + "'" + self.alphabet[i] + "'"
						if search_key in self.NFAtransition_funcs:

							temp = self.NFAtransition_funcs[search_key]
							destinations += temp
							
						
					#gets rid of duplicates
					destinations = list(dict.fromkeys(destinations))
					destinations.sort( key = int ) 

					self.total_states_to_loop.append(destinations)
					
					current_state = "".join(current_state)
					destinations = "".join(destinations)


					key_entry = current_state + " '" + str(i) + "' " 
					self.DFAtransition_funcs[key_entry] = destinations

				
				
		print("CHECK THIS!!!!!!")
		print(self.DFAtransition_funcs)
			


		


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
			if next_move in self.NFAtransition_funcs:
				curr_state = self.NFAtransition_funcs[next_move]
		# if last state is an accept state, return True, else return False
		if curr_state in self.accept_states:
			return True
		else:
			return False



	
