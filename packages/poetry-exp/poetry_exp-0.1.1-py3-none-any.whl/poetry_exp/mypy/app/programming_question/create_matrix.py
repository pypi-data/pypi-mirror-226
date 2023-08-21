import random

n = 3
m = 5

matrix = [[]] * n
print matrix  # [[], [], []]

for i in range(n):
    matrix[i] = [0]*m

print matrix
"""
[
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0]
]

"""


for i in range(n):
   col = []
   for j in range(m):
       col.append(random.randint(1,100))
   matrix[i] = col

print matrix

"""
[
  [89, 66, 26, 90, 2],
  [7, 53, 43, 78, 11],
  [88, 60, 99, 48, 92]
]

"""

# Traverse Matrix- Approach1
# for row in matrix:
#     for col in row:
#         print col

# Traverse Matrix Approach2
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        print matrix[i][j]