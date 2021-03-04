#Sodoku calculator
#done with unique row gona work on unique box now
import math
import numpy as np

def mat_correct(raw):
	mat = list(raw)
	out_mat = []
	for i in range(len(mat)):
		print(mat[i], end=" ")
		if mat[i] == ".":
			mat[i] = 0

		out_mat.append(int(mat[i]))

		if ((i+1)%9) == 0:
			print(' ')
	print(' ')

	return out_mat

def mat_print(in_mat):
	for i in range(len(in_mat)):
		print(in_mat[i], end=" ")
		if ((i+1)%9) == 0:
			print(' ')
	print(' ')


def row_print(in_mat, num):
	for i in range(len(in_mat)):
		if ((num-1)*9 <= i) and (i < (num)*9):
			print(in_mat[i], end=" ")
	print(' ')
	print(' ')


#0, 9, 18, 27...
def col_print(in_mat, num):
	for i in range(len(in_mat)):
		if (i % 9) == num-1:
			print(in_mat[i].value)
	print(' ')


def box_print(in_mat, num):
	step = 0
	wrap = 0
	#given the boxnum, find the root number
	root = int((num - 1) / 3) * 27

	for boxnum in range(9):
		print(in_mat[root + step +  wrap + ((num - 1) % 3)*3 ], end = ' ')
		step += 1
		if(step == 3):
			print(' ')
			wrap += 9
			step = 0

	print(' ')

def row_grab(in_mat, num):
	out_mat = []
	for i in range(len(in_mat)):
		if ((num-1)*9 <= i) and (i < (num)*9):
			out_mat.append(in_mat[i])

	return out_mat

#0, 9, 18, 27...
def col_grab(in_mat, num):
	out_mat = []
	for i in range(len(in_mat)):
		if (i % 9) == num-1:
			out_mat.append(in_mat[i])
	return out_mat

def box_grab(in_mat, num):
	out_mat = []
	step = 0
	wrap = 0
	#given the boxnum, find the root number
	root = int((num - 1) / 3) * 27
	for boxnum in range(9):
		out_mat.append(in_mat[root + step +  wrap + ((num - 1) % 3)*3 ])
		step += 1
		if(step == 3):
			wrap += 9
			step = 0
	return out_mat

def missing(in_mat):
	temp_mat = []
	for i in range(1,10): #from i: 1 - 9
		signal = 0
		for j in range(len(in_mat)):
			if in_mat[j] == i:
				signal += 1
		if signal == 0:
			temp_mat.append(i)
	return temp_mat

class Unit:
	def __init__(self, value, list):
		self.value = value
		self.suslist = list

class Grid:
    # Node Initializer. Sets first node to carry data and sets pointer to next node
	def __init__(self, data):
		self.data = data

	def package(self):
		out_mat = []
		for i in range(len(self.data)):
			out_mat.append(self.data[i].value)
		return out_mat

	def g_sum(self):
		sum = 0
		for i in range(len(self.data)):
			sum += self.data[i].value
		return sum

	def in_list(self, array, num):
		for i in range(len(array)):
			if array[i] == num:
				return 1
		return 0

	def token2parent(self, total_array, tokens, unique):
		parent = 1
		for e in range(len(total_array)):#assign token to be parent tracker
			if total_array[e] == 0:
				parent += 1
			if self.in_list(unique, total_array[e]):
				tokens[total_array[e] - 1] = parent
		parent_token = []
		for f in range(9):
			parent_token.append(0)
		for g in range(len(parent_token)):
			for h in range(len(tokens)):
				if tokens[h] == g + 1:
					parent_token[g] += 1
		return parent_token

	def suspectlist(self):
		#populate the the squares again with correct friend lists
		print("We in suspect now...")
		row_temp = []
		curr_row = 0
		time_saver = 0
		for i in range(len(self.data)):
			row_ID = int(i/9) + 1
			row_reg = []
			box_ID = int(i/27)*3 + (int(i/3)%3)+1
			box_reg = []
			curr_box = 0
			col_temp = []
			col_reg = []
			neighbor = []

			if time_saver:
				if self.data[i].value == 0:
					#Grab the Row
					if curr_row == row_ID:#if same row as earlier
						for j in range(len(row_temp)):#fill neighbor with same row sus
							neighbor.append(row_temp[j])
					else: #new row, so update current_row, and find row_sus
						curr_row = row_ID
						row_reg = row_grab(self.package(), row_ID)
						row_temp = []
						for k in range(len(row_reg)):
							if row_reg[k] > 0:
								row_temp.append(row_reg[k])
								neighbor.append(row_reg[k])

					#Grab the Box
					if curr_box == box_ID:#if same row as earlier
						for l in range(len(box_temp)):#fill neighbor with same row sus
							neighbor.append(box_temp[l])
					else: #new box, so update current_row, and find row_sus
						curr_box = box_ID
						box_reg = box_grab(self.package(), box_ID)
						box_temp = []
						for m in range(len(box_reg)):
							if box_reg[m] > 0:
								box_temp.append(box_reg[m])
								neighbor.append(box_reg[m])

					#Grab the columns
					col_temp = col_grab(self.package(), i%9 + 1 )
					for n in range(len(col_temp)):
						if col_temp[n] > 0:
							neighbor.append(col_temp[n])
							
			else: #no TIME SAVER
				if self.data[i].value == 0: #if 0, then look for all 3 contracts
					row_reg = row_grab(self.package(), row_ID)
					for k in range(len(row_reg)):
						if row_reg[k] > 0:
							neighbor.append(row_reg[k])
					box_reg = box_grab(self.package(), box_ID)
					for m in range(len(box_reg)):
						if box_reg[m] > 0:
							neighbor.append(box_reg[m])
					col_reg = col_grab(self.package(), i%9 + 1 )
					for n in range(len(col_reg)):
						if col_reg[n] > 0:
							neighbor.append(col_reg[n])
				else:
					self.data[i].suslist = [] #has value, so suslist = nothing

			real_sus = missing(neighbor)

			if len(real_sus) == 1 and self.data[i].value == 0: #if only one sus, then fill in val, remove suslist
				self.data[i].value = real_sus[0]
				self.data[i].suslist = []
			else:
				self.data[i].suslist  = real_sus

	def row_unique(self):
		total_row_sus = []
		curr_row = 0
		print_debug = 1

		for i in range(len(self.data)):
			row_ID = int(i/9) + 1
			if curr_row == row_ID:#if theyre the same, then add on!
				if self.data[i].value == 0:
					for j in range(len(self.data[i].suslist)):
						total_row_sus.append(self.data[i].suslist[j])
				total_row_sus.append(0)

				#ONCE the end is reached, tally up!:
				if (i+1)%9 == 0:
					if print_debug == 1:
						print("Row ", int(i/9)+1 ," finished, total sus: ")
						for l in range(len(total_row_sus)):
							print(total_row_sus[l], end = " ")
						print(" ")

					sus = missing(missing(total_row_sus))
					row_token = []
					for a in range(9):
						row_token.append(0)

					for b in range(len(sus)):
						for c in range(len(total_row_sus)):
							if sus[b] == total_row_sus[c]:
								row_token[sus[b] - 1] += 1

					if print_debug:
						print("Parent Tracker:")
						for p in range(len(row_token)):
							print(row_token[p], end = " ")
						print(" ")

					unique = []
					for d in range(9):
						if row_token[d] != 1:
							row_token[d] = 0
						else:
							unique.append(d + 1)

					#now we have the final parent token
					parent_token =  self.token2parent(total_row_sus, row_token, unique)

					if print_debug:
						print("Parent token:")
						for par in range(len(parent_token)):
							print(parent_token[par], end = " ")
						print(" ")

					#go through parent token and find all ones
					for c in range(len(parent_token)):
						if parent_token[c] == 1:
							#C+1 = PARENT HOUSE
							for d in range(len(row_token)):
								#D+1 = VALUE
								if (row_token[d] == c + 1) and (self.data[i- (8 - c)].value == 0):
									if print_debug == 1:
										print("currently in i = : ", i)
										print("we're changing the values...", i- (8 - c), " is now: ", d+1)
									self.data[i- (8 - c)].value = d + 1
									self.data[i- (8 - c)].suslist = []
			else: #if new row, recreate the list
				curr_row = row_ID
				total_row_sus = []
				#print("For index: ", i, " the list:")
				if self.data[i].value == 0:
					for k in range(len(self.data[i].suslist)):
						total_row_sus.append(self.data[i].suslist[k])
				total_row_sus.append(0)



	def box_unique(self):
		total_box_sus = []
		box_1 = [0, 1, 2, 9, 10, 11, 18, 19, 20] #box 1 addy = correct format
		print_debug = 1

		for box in range(9):
			curr_address = []
			seed = int(box/3)*27 + (box % 3)*3

			for a in range(9):
				curr_address.append(seed + box_1[a])

			for b in range(9):
				if self.data[curr_address[b]].value == 0:
					for sus in range(len(self.data[curr_address[b]].suslist)):
						total_box_sus.append(self.data[curr_address[b]].suslist[sus])
						if box + 1 == 7:
							print("adding @: ", self.data[curr_address[b]].suslist[sus], curr_address[b], self.data[curr_address[b]].value)

				total_box_sus.append(0)

			if print_debug:
				print("Total Box SUS of", box + 1)
				for g in range(len(total_box_sus)):
					print(total_box_sus[g], end = " ")
				print(" ")

			box_sus = missing(missing(total_box_sus))
			box_token = []
			for c in range(9):
				box_token.append(0)

			for d in range(len(box_sus)):
				for e in range(len(total_box_sus)):
					if box_sus[d] == total_box_sus[e]:
						box_token[box_sus[d] - 1] += 1

			if print_debug:
				print("Box Token is: ")
				for g in range(len(box_token)):
					print(box_token[g], end = " ")
				print(" ")


			box_unique = [] #grab the unique array
			for f in range(9):
				if box_token[f] != 1:
					box_token[f] = 0
				else:
					box_unique.append(f + 1)

			if print_debug:
				print("Parent Token is: ")
				for g2 in range(len(box_token)):
					print(box_token[g2], end = " ")
				print(" ")

			parent_tracker =  self.token2parent(total_box_sus, box_token, box_unique)
			if print_debug == 1:
				print("Parent Tracker:")
				for g in range(len(parent_tracker)):
					print(parent_tracker[g], end = " ")
				print(" ")

			for h in range(len(parent_tracker)):
				if parent_tracker[h] == 1:

					for i in range(len(box_token)):
						#D+1 = VALUE
						print("BoxHouse h+1: ", h+1, "", "The val that belongs: ", i+1)

						if (box_token[i] == h + 1) and (self.data[curr_address[h]].value == 0):
							self.data[curr_address[h]].value = i+1
							print(box_token[i], h+1, "Value ", i+1, " has been put into: ", curr_address[h])
							self.data[curr_address[h]].suslist = []

			#WHY ARE WE ADDING 8 WHEN 8 IS a friend?
			total_box_sus = []


###########TESTING############
toggle_input = 0

if toggle_input:
	raw = "85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4."
	mat = mat_correct(raw)
else:
	mat = [0, 0, 4, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 1, 9, 2, 0, 6, 8, 0, 0, 0, 6, 0, 0, 7, 8, 0, 5, 9, 5, 0, 0, 0, 3, 0, 0, 0, 2, 1, 3, 0, 5, 9, 0, 0, 8, 0, 0, 0, 5, 7, 0, 1, 6, 4, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 5, 0, 0]

unitList = []
for i in range(len(mat)):
	u = Unit(mat[i], [])
	unitList.append(u)

g = Grid(unitList)
mat_print(g.package())
count = 0
g.suspectlist()

while(g.g_sum() < 404 and count < 3):
	count+=1
	g.row_unique()
	g.suspectlist()
	print("current count is: ", count, ", " , int((g.g_sum() / 405) * 100 ), "%")
	mat_print(g.package())



#WHY IS THE TOTAL SUS LIST GRABBING WRONG VALUES?














'''
Hard
[0, 0, 4, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 1, 9, 2, 0, 6, 8, 0, 0, 0, 6, 0, 0, 7, 8, 0, 5, 9, 5, 0, 0, 0, 3, 0, 0, 0, 2, 1, 3, 0, 5, 9, 0, 0, 8, 0, 0, 0, 5, 7, 0, 1, 6, 4, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 5, 0, 0]

85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.
..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..
12..4......5.69.1...9...5.........7.7...52.9..3......2.9.6...5.4..9..8.1..3...9.4
...57..3.1......2.7...234......8...4..7..4...49....6.5.42...3.....7..9....18.....
7..1523........92....3.....1....47.8.......6............9...5.6.4.9.7...8....6.1.

1....7.9..3..2...8..96..5....53..9...1..8...26....4...3......1..4......7..7...3..
1...34.8....8..5....4.6..21.18......3..1.2..6......81.52..7.9....6..9....9.64...2
...92......68.3...19..7...623..4.1....1...7....8.3..297...8..91...5.72......64...
.6.5.4.3.1...9...8.........9...5...6.4.6.2.7.7...4...5.........4...8...1.5.2.3.4.
7.....4...2..7..8...3..8.799..5..3...6..2..9...1.97..6...3..9...3..4..6...9..1.35

....7..2.8.......6.1.2.5...9.54....8.........3....85.1...3.2.8.4.......9.7..6....




Medium
4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
52...6.........7.13...........4..8..6......5...........418.........3..2...87.....
6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....
48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....
....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8...
......52..8.4......3...9...5.1...6..2..7........3.....6...1..........7.4.......3.
6.2.5.........3.4..........43...8....1....2........7..5..27...........81...6.....
.524.........7.1..............8.2...3.....6...9.5.....1.6.3...........897........
6.2.5.........4.3..........43...8....1....2........7..5..27...........81...6.....
.923.........8.1...........1.7.4...........658.........6.5.2...4.....7.....9.....
6..3.2....5.....1..........7.26............543.........8.15........4.2........7..
.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...
..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..
3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....
1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......
6..3.2....4.....1..........7.26............543.........8.15........4.2........7..
....3..9....2....1.5.9..............1.2.8.4.6.8.5...2..75......4.1..6..3.....4.6.
45.....3....8.1....9...........5..9.2..7.....8.........1..4..........7.2...6..8..
.237....68...6.59.9.....7......4.97.3.7.96..2.........5..47.........2....8.......
..84...3....3.....9....157479...8........7..514.....2...9.6...2.5....4......9..56
.98.1....2......6.............3.2.5..84.........6.........4.8.93..5...........1..
..247..58..............1.4.....2...9528.9.4....9...1.........3.3....75..685..2...
4.....8.5.3..........7......2.....6.....5.4......1.......6.3.7.5..2.....1.9......
.2.3......63.....58.......15....9.3....7........1....8.879..26......6.7...6..7..4
1.....7.9.4...72..8.........7..1..6.3.......5.6..4..2.........8..53...7.7.2....46
4.....3.....8.2......7........1...8734.......6........5...6........1.4...82......
.......71.2.8........4.3...7...6..5....2..3..9........6...7.....8....4......5....
6..3.2....4.....8..........7.26............543.........8.15........8.2........7..
.47.8...1............6..7..6....357......5....1..6....28..4.....9.1...4.....2.69.
......8.17..2........5.6......7...5..1....3...8.......5......2..4..8....6...3....
38.6.......9.......2..3.51......5....3..1..6....4......17.5..8.......9.......7.32
...5...........5.697.....2...48.2...25.1...3..8..3.........4.7..13.5..9..2...31..
.2.......3.5.62..9.68...3...5..........64.8.2..47..9....3.....1.....6...17.43....
.8..4....3......1........2...5...4.69..1..8..2...........3.9....6....5.....2.....
..8.9.1...6.5...2......6....3.1.7.5.........9..4...3...5....2...7...3.8.2..7....4
4.....5.8.3..........7......2.....6.....5.8......1.......6.3.7.5..2.....1.8......
1.....3.8.6.4..............2.3.1...........958.........5.6...7.....8.2...4.......
1....6.8..64..........4...7....9.6...7.4..5..5...7.1...5....32.3....8...4........
249.6...3.3....2..8.......5.....6......2......1..4.82..9.5..7....4.....1.7...3...
...8....9.873...4.6..7.......85..97...........43..75.......3....3...145.4....2..1
...5.1....9....8...6.......4.1..........7..9........3.8.....1.5...2..4.....36....
......8.16..2........7.5......6...2..1....3...8.......2......7..3..8....5...4....
.476...5.8.3.....2.....9......8.5..6...1.....6.24......78...51...6....4..9...4..7
.....7.95.....1...86..2.....2..73..85......6...3..49..3.5...41724................
.4.5.....8...9..3..76.2.....146..........9..7.....36....1..4.5..6......3..71..2..
.834.........7..5...........4.1.8..........27...3.....2.6.5....5.....8........1..
..9.....3.....9...7.....5.6..65..4.....3......28......3..75.6..6...........12.3.8
.26.39......6....19.....7.......4..9.5....2....85.....3..2..9..4....762.........4
2.3.8....8..7...........1...6.5.7...4......3....1............82.5....6...1.......
6..3.2....1.....5..........7.26............843.........8.15........8.2........7..
1.....9...64..1.7..7..4.......3.....3.89..5....7....2.....6.7.9.....4.1....129.3.
.........9......84.623...5....6...453...1...6...9...7....1.....4.5..2....3.8....9
.2....5938..5..46.94..6...8..2.3.....6..8.73.7..2.........4.38..7....6..........5
9.4..5...25.6..1..31......8.7...9...4..26......147....7.......2...3..8.6.4.....9.
...52.....9...3..4......7...1.....4..8..453..6...1...87.2........8....32.4..8..1.
53..2.9...24.3..5...9..........1.827...7.........981.............64....91.2.5.43.
1....786...7..8.1.8..2....9........24...1......9..5...6.8..........5.9.......93.4
....5...11......7..6.....8......4.....9.1.3.....596.2..8..62..7..7......3.5.7.2..
.47.2....8....1....3....9.2.....5...6..81..5.....4.....7....3.4...9...1.4..27.8..
......94.....9...53....5.7..8.4..1..463...........7.8.8..7.....7......28.5.26....
.2......6....41.....78....1......7....37.....6..412....1..74..5..8.5..7......39..
1.....3.8.6.4..............2.3.1...........758.........7.5...6.....8.2...4.......
2....1.9..1..3.7..9..8...2.......85..6.4.........7...3.2.3...6....5.....1.9...2.5
..7..8.....6.2.3...3......9.1..5..6.....1.....7.9....2........4.83..4...26....51.
...36....85.......9.4..8........68.........17..9..45...1.5...6.4....9..2.....3...
34.6.......7.......2..8.57......5....7..1..2....4......36.2..1.......9.......7.82
......4.18..2........6.7......8...6..4....3...1.......6......2..5..1....7...3....
.4..5..67...1...4....2.....1..8..3........2...6...........4..5.3.....8..2........
.......4...2..4..1.7..5..9...3..7....4..6....6..1..8...2....1..85.9...6.....8...3
8..7....4.5....6............3.97...8....43..5....2.9....6......2...6...7.71..83.2
.8...4.5....7..3............1..85...6.....2......4....3.26............417........
....7..8...6...5...2...3.61.1...7..2..8..534.2..9.......2......58...6.3.4...1....
......8.16..2........7.5......6...2..1....3...8.......2......7..4..8....5...3....
.2..........6....3.74.8.........3..2.8..4..1.6..5.........1.78.5....9..........4.
.52..68.......7.2.......6....48..9..2..41......1.....8..61..38.....9...63..6..1.9
....1.78.5....9..........4..2..........6....3.74.8.........3..2.8..4..1.6..5.....
1.......3.6.3..7...7...5..121.7...9...7........8.1..2....8.64....9.2..6....4.....
4...7.1....19.46.5.....1......7....2..2.3....847..6....14...8.6.2....3..6...9....
......8.17..2........5.6......7...5..1....3...8.......5......2..3..8....6...4....
963......1....8......2.5....4.8......1....7......3..257......3...9.2.4.7......9..
15.3......7..4.2....4.72.....8.........9..1.8.1..8.79......38...........6....7423
..........5724...98....947...9..3...5..9..12...3.1.9...6....25....56.....7......6
....75....1..2.....4...3...5.....3.2...8...1.......6.....1..48.2........7........
6.....7.3.4.8.................5.4.8.7..2.....1.3.......2.....5.....7.9......1....
....6...4..6.3....1..4..5.77.....8.5...8.....6.8....9...2.9....4....32....97..1..
.32.....58..3.....9.428...1...4...39...6...5.....1.....2...67.8.....4....95....6.
...5.3.......6.7..5.8....1636..2.......4.1.......3...567....2.8..4.7.......2..5..
.5.3.7.4.1.........3.......5.8.3.61....8..5.9.6..1........4...6...6927....2...9..
..5..8..18......9.......78....4.....64....9......53..2.6.........138..5....9.714.
..........72.6.1....51...82.8...13..4.........37.9..1.....238..5.4..9.........79.
...658.....4......12............96.7...3..5....2.8...3..19..8..3.6.....4....473..
.2.3.......6..8.9.83.5........2...8.7.9..5........6..4.......1...1...4.22..7..8.9
.5..9....1.....6.....3.8.....8.4...9514.......3....2..........4.8...6..77..15..6.
.....2.......7...17..3...9.8..7......2.89.6...13..6....9..5.824.....891..........
3...8.......7....51..............36...2..4....7...........6.13..452...........8..
