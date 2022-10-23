# Name: pa2.py
# Author(s): Tyler Kreider and Julia Paley
# Date Written: 10/15/2022 
# Description: Reads an NFA specification from another file, converts the NFA to an equivalent DFA, and writes the DFA to a file.


class NFA:
	""" Simulates an NFA """

	def __init__(self, filename):
		"""
		Initializes NFA from the file whose name is
		filename
		"""
		# open and read the file
		file = open(filename, 'r')
		self.total_nfa_states = int(file.readline().rstrip())
		self.alphabet = file.readline().rstrip()
		apostrophe = "'"
		self.nfa_trans_funcs = {}
		trans_val = True
		next_line = ''

		# loop through transition function values until start state
		while trans_val:
			next_line = file.readline().rstrip()
			# check if the line is a transition function
			if apostrophe in next_line:
				trans_vals = next_line.split()
				#replace the key value to include new state
				if (trans_vals[0] + trans_vals[1]) in self.nfa_trans_funcs:
					self.nfa_trans_funcs.get(trans_vals[0]+trans_vals[1]).append(trans_vals[2])
				#first dictionary entry for this transition function
				else:
					temp_value_list = [trans_vals[2]]
					self.nfa_trans_funcs[trans_vals[0]+trans_vals[1]]= temp_value_list
			else:
				trans_val = False

		self.start_state = file.readline().rstrip()
		self.accept_states = file.readline().rstrip().split()
		# initialize needed variables
		self.dfa_trans_funcs = {}
		self.dfa_accept_sts = []
		self.dfa_start_st = 0
		self.total_states = 0

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
		dfa_start_states = [self.start_state]
		dfa_start_states = self.epsilon(dfa_start_states)
		dfa_start_states = list(dict.fromkeys(dfa_start_states))
		dfa_start_states.sort( key = int)
		final_dfa_start = ",".join(dfa_start_states)
		self.dfa_start_st = final_dfa_start
		states_to_loop = [final_dfa_start]
		
		# add nfa states to loop through for transition function
		for single_state in range(1, self.total_nfa_states + 1):
			states_to_loop.append(str(single_state))

		# add start state to accept states if it is an accept state
		for start_var in dfa_start_states:
			if start_var in self.accept_states:
				self.dfa_accept_sts.append(final_dfa_start)
				break	
		
		self.create_transitions(states_to_loop)
		self.dfa_trans_funcs = self.format_to_file()
		self.WriteToFile(dfa_filename)
		

	def create_transitions(self, total_states_to_loop):
		"""
		Loops through total_states_to_loop until every state the DFA visits
		is in the DFA transition function. Updates the DFA's accept state(s).
		"""
		while len(total_states_to_loop) > 0:
			current_state = total_states_to_loop.pop()
			current_state = current_state.split(',')
			# loop through alphabet and get next state transition
			for i in range(len(self.alphabet)):
				destinations = []
				# loop states in current_state and add nfa state to dfa destination state
				for x in range(len(current_state)): 
					search_key = current_state[x] + "'" + self.alphabet[i] + "'"
					if search_key in self.nfa_trans_funcs:
						destinations.extend(self.nfa_trans_funcs[search_key])
						destinations = self.epsilon(destinations)
				#get rid of duplicates
				if len(destinations) > 1:
					destinations = list(dict.fromkeys(destinations))
					destinations.sort( key = int ) 
				# add state to dfa accept states if the state has an accepting NFA state
				for potential_accept in destinations:
					if potential_accept in self.accept_states:
						self.dfa_accept_sts.append(",".join(destinations))
						self.dfa_accept_sts = list(dict.fromkeys(self.dfa_accept_sts))
						break
				key_entry = ",".join(current_state) + " '" + self.alphabet[i] + "' " 

				# if destination is a reject state
				if len(destinations) == 0:
					destinations = '0'
				else:
					destinations = ",".join(destinations)
				# add destination to list of unhandled states 
				if destinations not in self.dfa_trans_funcs.values():
					total_states_to_loop.append(destinations) 
					total_states_to_loop = list(dict.fromkeys(total_states_to_loop))
				# add new transition function entry
				self.dfa_trans_funcs[key_entry] = destinations	
		
		

	def format_to_file(self):
		"""
		Creates the correct format for the DFA transition function, start state,
		and accept state(s). Returns the DFA function in the correct format.
		"""
		new_mappings = {}
		new_trans_func = {}
		state_number = self.total_nfa_states + 1

		# create new mappings for DFA states that are 1 NFA state
		for i in range(1, state_number):
			new_mappings[str(i)] = str(i)

		# create mappings for all other DFA states
		for trans_key in self.dfa_trans_funcs:
			# DFA transition state is 2+ states or a rejecting state
			if trans_key[:-5] not in new_mappings:
				new_mappings[trans_key[:-5]] = str(state_number)
				state_number += 1

		# loop through DFA transition function keys and fix format in transition function
		for trans_key in self.dfa_trans_funcs:
			new_value = new_mappings[trans_key[:-5]] + " " + trans_key[-4:-1] + " "
			new_trans_func[new_value] = new_mappings[self.dfa_trans_funcs[trans_key]]
		
		# fix format for start state
		self.dfa_start_st = new_mappings[self.dfa_start_st]

		# fix format for accept states
		for i in range(len(self.dfa_accept_sts)):
			self.dfa_accept_sts[i] = new_mappings[self.dfa_accept_sts[i]]

		# get total number of states
		max_state_val = [eval(state) for state in list(new_mappings.values())]
		self.total_states = int(max(max_state_val))

		return new_trans_func
	
	def epsilon(self, states_list):
		"""
		Adds all epsilon transition states to the destination or start state.
		Returns list of all states epsilon leads to.
		"""
		for i in range(len(states_list)):
			epsilon_trans =  states_list[i] + "'e'"
			if epsilon_trans in self.nfa_trans_funcs:
				states_list.extend(self.nfa_trans_funcs[epsilon_trans])
				# recursion for unlimited epsilons
				states_list.extend(self.epsilon(self.nfa_trans_funcs[epsilon_trans]))
		return states_list


	def WriteToFile(self, dfa_filename):
		"""
		Writes the created DFA spcifications to the file dfa_filename in the format from pa1.
		"""
		new_file = open(dfa_filename, 'w')
		new_file.write(str(self.total_states) + '\n')
		new_file.write(self.alphabet + '\n')

		for trans_func in self.dfa_trans_funcs:
			new_file.write(trans_func + " " + str(self.dfa_trans_funcs[trans_func]) + '\n')

		new_file.write(self.dfa_start_st + '\n')
		new_file.write(	" ".join(self.dfa_accept_sts))