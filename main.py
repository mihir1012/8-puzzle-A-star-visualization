from queue import PriorityQueue as pq
from queue import LifoQueue as stk
import math

source = [[4,0,8],[6,1,5],[7,3,2]]
target = [[1,2,3],[4,5,6],[7,8,0]]



state_map = {1:source}
def get_state_number(state):
    #print("get_state_number",state,end=" ")
    for key,val in state_map.items():
        if val == state:
            #print("key found", key)
            return key
    state_map[len(state_map) + 1] = state
    #print("key added",len(state_map) +1,state_map)
    return len(state_map)

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i,j

def get_possible_states(curr):
    possible_states = {}
    row,col = find_zero(curr)

    if row < 2 and col > 0 :

        new_state = [[curr[x][y] for y in range(3)] for x in range(3)]
        new_state[row][col] = new_state[row][col-1]
        new_state[row][col-1] = 0
        possible_states[get_state_number(new_state)]="LEFT"
        new_state = [[curr[x][y] for y in range(3)] for x in range(3)]
        new_state[row][col] = new_state[row+1][col]
        new_state[row+1][col] = 0
        possible_states[get_state_number(new_state)] = "DOWN"

    if row < 2 and col < 2 :
        
        new_state = [[curr[x][y] for y in range(3)] for x in range(3)]
        new_state[row][col] = new_state[row][col+1]
        new_state[row][col+1] = 0
        possible_states[get_state_number(new_state)] = "RIGHT"
        new_state = [[curr[x][y] for y in range(3)] for x in range(3)]
        new_state[row][col] = new_state[row+1][col]
        new_state[row+1][col] = 0
        possible_states[get_state_number(new_state)] = "DOWN"

    if row > 0 and col > 0 :
        new_state = [[curr[x][y] for y in range(3)] for x in range(3)]
        new_state[row][col] = new_state[row][col-1]
        new_state[row][col-1] = 0
        possible_states[get_state_number(new_state)] = "LEFT"
        new_state = [[curr[x][y] for y in range(3)] for x in range(3)]
        new_state[row][col] = new_state[row-1][col]
        new_state[row-1][col] = 0
        possible_states[get_state_number(new_state)] = "UP"
        
    if row > 0 and col < 2 :
        new_state = [[curr[x][y] for y in range(3)] for x in range(3)]
        new_state[row][col] = new_state[row][col+1]
        new_state[row][col+1] = 0
        possible_states[get_state_number(new_state)] = "RIGHT"
        new_state = [[curr[x][y] for y in range(3)] for x in range(3)]
        new_state[row][col] = new_state[row-1][col]
        new_state[row-1][col] = 0
        possible_states[get_state_number(new_state)] = "UP"
        
    return possible_states


def reconstruct_path(parents,directions,current):
    print("State and Direction of move of the empty cell:\n")
    stack = stk()
    while current in parents:
        stack.put((current,directions[current]))
        current = parents[current]

    for row in state_map[current]:
          print(row)
    print("")
    
    while not stack.empty():
      state,direction = stack.get()  
      current_state = state_map[ state ]
      print("---",direction,"---","\n")
      for row in current_state:
          print(row)
      print("")

def get_diff(ele):
    for i in range(3):
        for j in range(3):
            if ele == target[i][j]:
                return i,j
# Hueristic is number of misplaced tiles
def h(curr):
    val = 0
    for i in range(3):
        for j in range(3):
            if curr[i][j] != target[i][j]:
                p,q=get_diff(curr[i][j])
                val += abs(i-p) + abs(j-q)
    return val

found = False
open_set = pq()
open_set.put((0,source))
parents ={}
parent_direction={}
g_score = {1: 0}
f_score = {1: h(source)}

open_set_hash = {get_state_number(source)}

while not open_set.empty():
    current =  open_set.get()[1] 
    open_set_hash.remove(get_state_number(current))

    #print("current:",current)

    if current == target:
        reconstruct_path(parents,parent_direction,get_state_number(target))
        found = True
        break

    possible_states = get_possible_states(current)
    #print(possible_states,state_map)
    for possible_state in possible_states:
        #print("possible state", possible_state)
        temp_g_score = g_score[get_state_number(current)] + 1
        if possible_state not in g_score or temp_g_score < g_score[possible_state]:
            parents[possible_state] = get_state_number(current)
            parent_direction[possible_state] = possible_states[possible_state]
            g_score[possible_state] = temp_g_score
            f_score[possible_state] = temp_g_score + h(state_map[possible_state])

            if possible_state not in open_set_hash:
                open_set.put((f_score[possible_state],state_map[possible_state]))
                open_set_hash.add(possible_state)
 
print("path not available") if not found else print("Done")
#print(state_map)
