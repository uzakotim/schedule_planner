import numpy as np
# Source: https://subscription.packtpub.com/book/data/9781838645359/8/ch08lvl1sec39/implementation

# Setting the parameters gamma and alpha for the Q-Learning
gamma = 0.75
alpha = 0.9

# PART 1 - BUILDING THE ENVIRONMENT

# Defining the states
state_to_task = {}
n = input("Введите число дел...\n")
n = int(n)
for i in range(1,n+1):
    task = input("Введите название каждой задачи...\n")
    state_to_task[i] = task
# Defining the actions
actions = [x for x in range(1,n+1)]
print(actions)
# Defining the rewards
R = np.eye(n)
inp = ''
while(1):
    for i in range(1,n+1):
        print(i,":", state_to_task[i])
    inp = input("Введите через пробел\nНачальная задача, следующая задача, наргада за переход\nПросто нажмите Enter чтобы завершить\n")
    if inp == '':
        break
    else:
        inp = inp.split()
        R[int(inp[0])-1,int(inp[1])-1] = int(inp[2])
    print(R)

# Making a mapping from the states to the locations
# state_to_location = {state: location for location, state in location_to_state.items()}

# Making a function that returns the shortest route from a starting to ending location
def route(starting_state, ending_state):
    R_new = np.copy(R)
    R_new[ending_state, ending_state] = 1000
    Q = np.array(np.zeros([R_new.shape[0], R_new.shape[1]]))
    for i in range(1000):
        current_state = np.random.randint(0, R_new.shape[0])
        playable_actions = []
        for j in range(R_new.shape[1]):
            if R_new[current_state, j] > 0:
                playable_actions.append(j)
        next_state = np.random.choice(playable_actions)
        TD = R_new[current_state, next_state] + gamma * Q[next_state, np.argmax(Q[next_state,])] - Q[current_state, next_state]
        Q[current_state, next_state] = Q[current_state, next_state] + alpha * TD
    route = [state_to_task[starting_state+1]]
    next_state = starting_state
    while (next_state != ending_state):
        starting_state = next_state
        next_state = np.argmax(Q[starting_state,])
        next_task = state_to_task[next_state+1]
        route.append(next_task)
    return route

# # Making the final function that returns the optimal route
# def best_route(starting_location, intermediary_location, ending_location):
#     return route(starting_location, intermediary_location) + route(intermediary_location, ending_location)[1:]

decision = [int(x) for x in input("Введите число начальной задачи и конечно задачи через пробел\n").split()]
# Printing the final route
print('Путь:')
for x in route(decision[0]-1, decision[1]-1):
    print(x,end='\n')
