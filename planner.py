import numpy as np
import csv
# Source: https://subscription.packtpub.com/book/data/9781838645359/8/ch08lvl1sec39/implementation
# Setting the parameters gamma and alpha for the Q-Learning
gamma = 0.75
alpha = 0.9

def printMatrix(a):
   # source: https://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python
    print("Reward matrix ["+("%d" %a.shape[0])+"]["+("%d" %a.shape[1])+"]")
    rows = a.shape[0]
    cols = a.shape[1]
    for i in range(0,rows):
        for j in range(0,cols):
            print(("%6.f" %a[i,j]),end=" ")
        print()
    print()
def printDict(a):
    for i in a:
        print(i,": ",a[i],end='\n')

# Making a function that returns the shortest route from a starting to ending location
def route(starting_state, ending_state,R_new,state_to_task):
    global gamma,alpha
    # -----------------------------------------
    # Function to find the best route from 
    # starting to ending location
    # -----------------------------------------
    # Optional : set goal reward high
    R_new[ending_state, ending_state] = 1000
    # -----------------------------------------
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
    route = [state_to_task[starting_state]]
    next_state = starting_state
    counter = 0
    while (next_state != ending_state):
        starting_state = next_state
        next_state = np.argmax(Q[starting_state,])
        next_task = state_to_task[next_state]
        route.append(next_task)
        counter += 1
        if counter > len(state_to_task):
            print("Sorry, I could not find a plan")
            print("Add more connections between events")
            break
    return route
def read_stored_matrix(state_to_task):
    # -----------------------------------------
    # Function to read the graph from csv file
    # -----------------------------------------
    elements = []
    with open('matrix.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i,row in enumerate(reader):
            if i == 0:
                for j,x in enumerate(row):
                    state_to_task[j] = x
            else:
                elements.append([float(k) for k in row])   
    R = np.array(elements, dtype=int)
    return R,state_to_task


def manual_input_matrix(state_to_task):
    # -----------------------------------------
    # Function to write the graph from 
    # user input
    # -----------------------------------------
    # Defining the states
    i = 0
    while(1):
        task = input("Type-in a name for each of your tasks...\nSimply press Enter to finish\n")
        if task == '':
            break
        else:
            state_to_task[i] = task
        i+=1
    n = len(state_to_task)
    # Defining the rewards
    R = np.eye(n,dtype=int)
    printMatrix(R)
    inp = ''
    while(1):
        for i in range(n):
            print(i,":", state_to_task[i])
        inp = input("Type-in separately by space\nStarting task, next task, reward for transition\nSimply press Enter to finish\n")
        if inp == '':
            break
        else:
            inp = inp.split()
            R[int(inp[0]),int(inp[1])] = int(inp[2])
        printMatrix(R)
    tasks = [x[1] for x in state_to_task.items()]
    # Save the matrix into csv file
    with open('matrix.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(tasks)
        row_list = []
        for i in range(n):
            for j in range(n):
                row_list.append(str(int(R[i,j])))
            writer.writerow(row_list)
            row_list = []
    return R,state_to_task
def main():
    string_inp1 = "Manual input (0) or use data (1)\n"
    print("*"*len(string_inp1))
    selection = int(input(string_inp1))
    use_stored_matrix = selection
    state_to_task = {}
    if use_stored_matrix:
        R,state_to_task = read_stored_matrix(state_to_task)
    if (use_stored_matrix==False):
        R,state_to_task = manual_input_matrix(state_to_task)
    
    printMatrix(R)
    print("*"*len(string_inp1))
    printDict(state_to_task)
    print("*"*len(string_inp1))
    decision = [int(x) for x in input("Type in the index of the first task and\nthe last task separated by space\n").split()]
    # Printing the final route
    sourceFile = open('plan.txt', 'w')
    print("*"*len(string_inp1))
    print('Result:',file = sourceFile)
    print('Result:')
    for i,x in enumerate(route(decision[0], decision[1],R,state_to_task)):
        print(i+1,":",x,file= sourceFile,end='\n')
        print(i+1,":",x,end='\n')
    sourceFile.close()

if __name__ == "__main__":
    main()