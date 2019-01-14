import numpy as np
import timeit
import signal


def safe(matrix, row, col):
    for field in matrix[row]:
        if field: return False
    for i in range(len(matrix[0])):
        if matrix[i][col]: return False
    i, j = row, col
    l = len(matrix)
    while i < l and j < l:
        if matrix[i][j]: return False
        i, j = i + 1, j + 1
    i, j = row, col
    while i < l and j >= 0:
        if matrix[i][j]: return False
        i, j = i + 1, j - 1
    i, j = row, col
    while i >= 0 and j < l:
        if matrix[i][j]: return False
        i, j = i - 1, j + 1
    i, j = row, col
    while i >= 0 and j >= 0:
        if matrix[i][j]: return False
        i, j = i - 1, j - 1
    return True


def score(matrix):
    sum_1 = sum_t = sum_up = sum_lr = 0
    for i,j in [(i,j) for i in range(N) for j in range(N)]:
        if matrix[i][j] == 1:
            sum_1 += cost[i][j]
            sum_t += cost[j][i]
            sum_up += cost[i][N-j-1]
            sum_lr += cost[N-i-1][j]
    return max(sum_1, sum_t, sum_up, sum_lr)


def officer_place(count, row):
    global sumMax
    if count == p:
        ans = score(matrix)
        if ans > sumMax:
            sumMax = ans
        return
    if p - count <= N - row:
        # SORTED INDICES
        path_row = cost[row]
        sorted_indices = sorted(range(len(path_row)), key = path_row.__getitem__, reverse=True)
        for i in sorted_indices:
        # for i in range(N):
            if safe(matrix, row, i):
                matrix[row][i] = 1
                if count == p:
                    pass
                else:
                    officer_place(count+1, row+1)
                    matrix[row][i] = 0
        officer_place(count, row+1)


def handler(signum, frame):
    with open('output.txt', "w") as fw:
        fw.write(str(sumMax))
    exit()

fr = open('input3.txt', 'r')
N = int(fr.readline())
p = int(fr.readline())
s = int(fr.readline())
cost = np.zeros((N, N), dtype=np.int)
for inp in fr.readlines():
    x_y = inp.split(",")
    x_cord = int(x_y[0])
    y_cord = int(x_y[1])
    cost[x_cord][y_cord] += 1
fw = open('output.txt', 'w')
sumMax = 0
matrix = np.zeros((N, N), dtype=np.int)
signal.signal(signal.SIGALRM, handler)
signal.alarm(178)
officer_place(0, 0)
fw.write(str(sumMax))
fw.close()
