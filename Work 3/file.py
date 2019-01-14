import copy
import numpy as np
import math
def input(fr):
	size=int(fr.readline())	
	ncars=int(fr.readline())
	nobst=int(fr.readline())
	obst, cstart, cend = ([] for i in range(3))
	for _ in range(nobst):
		line = fr.readline().strip().split(',')
		obst.append([line[1],line[0]])
	for i in range(ncars+ncars):
		line = fr.readline().strip().split(',')
		if i<ncars:
			cstart.append([line[1],line[0]])
		else:
			cend.append([line[1],line[0]])
	return size, ncars, nobst, obst, cstart, cend


def leftturn(arrow):
	if arrow == '^':
		return '<'
	if arrow == '<':
		return 'v'
	if arrow == 'v':
		return '>'
	return '^'


def rightturn(arrow):
	if arrow == '^':
		return '>'
	if arrow == '<':
		return '^'
	if arrow == 'v':
		return '<'
	return 'v'


def simulate(grid, d_list, start, end):
	total = 0
	for j in range(10):
		point = 0
		curr_x, curr_y = int(start[0]), int(start[1])
		end_x, end_y = int(end[0]), int(end[1])
		np.random.seed(j)
		swerve = np.random.random_sample(1000000)
		k = 0
		flag = True
		while flag:
			move = d_list[curr_x][curr_y]
			if swerve[k] > 0.7:
				if swerve[k] > 0.8:
					if swerve[k] > 0.9:
						move = leftturn(leftturn(move))
					else:
						move = rightturn(move)
				else:
					move = leftturn(move)
			k += 1
			if move == '^':
				curr_x = curr_x-1 if curr_x>0 else curr_x
			elif move == '>':
				curr_y = curr_y+1 if curr_y<size-1 else curr_y
			elif move == '<':
				curr_y = curr_y-1 if curr_y>0 else curr_y
			else:
				curr_x = curr_x+1 if curr_x<size-1 else curr_x
			if end_y == curr_y and end_x == curr_x:
				flag = False
			point += grid[curr_x][curr_y]	
		total += point

	total = math.floor(total/10)
	# print int(total)
	return int(total)


def policy(grid, size, obst, cend, utils):
	gamma, eps = 0.9, 0.1
	dx1 = ['^', 'v', '>', '<']
	d_list = [['']*size for q in range(size)]
	for j in range(nobst):
		utils[int(obst[j][0])][int(obst[j][1])] = -101
	d_list[int(cend[0])][int(cend[1])] = 'X'
	while True:
		delta = 0
		udash = copy.deepcopy(utils)
		temp = copy.deepcopy(d_list)
		for x in range(size):
			for y in range(size):
				if x == int(cend[0]) and y == int(cend[1]):
					continue
				else:
					values = []
					up = udash[x-1 if x>0 else x][y]
					left = udash[x][y-1 if y>0 else y]
					right = udash[x][y+1 if y<size-1 else y]
					down = udash[x+1 if x<size-1 else x][y]
					values.append(np.float64((0.7*up)+0.1*(left+right+down)))
					values.append(np.float64((0.7*down)+0.1*(up+left+right)))
					values.append(np.float64((0.7*right)+0.1*(up+down+left)))
					values.append(np.float64((0.7*left)+0.1*(up+right+down)))
					mx = max(values)
					idx = values.index(mx)
					d_list[x][y] = dx1[idx]		# POLICY MATRIX
					utils[x][y] = grid[x][y] + np.float64(gamma*mx)
					delta = max(delta, abs(udash[x][y]-utils[x][y]))
		if delta < eps * (1-gamma)/gamma:
			break
	return temp

fr=open('input.txt','r')
fw=open('output.txt','w')
size, ncars, nobst, obst, cstart, cend= input(fr)
grid, ans = [[-1.0]*size for p in range(size)], []
for j in range(nobst):
		grid[int(obst[j][0])][int(obst[j][1])] = -101

for i in range(ncars):		# For all cars
	if cstart[i] == cend[i]:
		# print 100
		ans.append(100)
	else:
		utils = [[-1.0]*size for p in range(size)]
		grid[int(cend[i][0])][int(cend[i][1])] = 99
		utils[int(cend[i][0])][int(cend[i][1])] = 99
		d_list = policy(grid, size, obst, cend[i], utils)
		ans.append(simulate(grid, d_list, cstart[i], cend[i]))
		grid[int(cend[i][0])][int(cend[i][1])] = -1

for i,x in enumerate(ans):
	fw.write(str(x))
	if i < len(ans)-1:
		fw.write("\n")
