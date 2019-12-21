sudoku = [
    [1,0,0,0,7,0,0,3,0],
    [8,3,0,6,0,0,0,0,0],
    [0,0,2,9,0,0,6,0,8],
    [6,0,0,0,0,4,9,0,7],
    [0,9,0,0,0,0,0,5,0],
    [3,0,7,5,0,0,0,0,4],
    [2,0,3,0,0,9,1,0,0],
    [0,0,0,0,0,2,0,4,3],
    [0,4,0,0,8,0,0,0,9]
]

#function to print the sudoku board
def print_sudoku(b):
	for i in range(len(b)):
		if i%3==0 and i!=0:
			print("- - - - - - - - - - ")
		for j in range(len(b[0])):
			if(j%3==0 and j!=0):
				print("|", end = '')
			if(j==8):
				print(b[i][j])
			else:
				print((b[i][j]),end = " ")



#function to find the valid entry in sudoku
def is_valid_entry(b, number, position):
	# checking in row
	for i in range(len(b[0])):
		if  position[1] != i and b[position[0]][i] == number :
			return False

	#checking in column
	for i in range(len(b)):
		if  position[0] != i and b[i][position[1]] == number :
			return False

	#checking in small 3x3 box
	bx = position[1]//3
	by = position[0]//3
	for i in range(by*3,by*3+3):
		for j in range(bx*3,bx*3+3):
			if(b[i][j]==number and (i,j)!=position):
				return False
	return True

#function to find an empty box, denoted by 0
def find_empty_box(b):
	for i in range(len(b)):
		for j in range(len(b[0])):
			if b[i][j] == 0:
				return (i,j)
	return None


#solving sudoku using backtracking
def solve_sudoku(b):
	empty_box = find_empty_box(b)
	if not empty_box:
		return True
	else:
		r, c = empty_box 

	for i in range(1,10):
		if is_valid_entry(b, i, (r,c)):
			b[r][c] = i

			if solve_sudoku(b):
				return True
			

			b[r][c] = 0
	
	#backtrack
	return False



solve_sudoku(sudoku)
print_sudoku(sudoku)



