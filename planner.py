import numpy as np
import csv
# Source: https://subscription.packtpub.com/book/data/9781838645359/8/ch08lvl1sec39/implementation

# Setting the parameters gamma and alpha for the Q-Learning
gamma = 0.75
alpha = 0.9


# Making a function that returns the shortest route from a starting to ending location
def route(starting_state, ending_state,R,state_to_task):
    R_new = np.copy(R)
    # R_new[ending_state, ending_state] = 1000
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
            print("Простите, я не смог найти ваш план")
            break
    return route

def main():
    selection = int(input("Ручной ввод (0) или использовать данные (1):  "))
    use_stored_matrix = selection
    state_to_task = {}
    if use_stored_matrix:
        elements = []
        with open('matrix.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for i,row in enumerate(reader):
                if i == 0:
                    for j,x in enumerate(row):
                        state_to_task[j] = x
                else:
                    elements.append([float(k) for k in row])   
        R = np.array(elements)

    if (use_stored_matrix==False):
        # Defining the states
        state_to_task = {}
        n = input("Введите число дел...\n")
        n = int(n)
        for i in range(n):
            task = input("Введите название каждой задачи...\n")
            state_to_task[i] = task
        # Defining the actions
        actions = [x for x in range(1,n+1)]
        R = np.eye(n)
        print(R)
        inp = ''
        while(1):
            for i in range(n):
                print(i,":", state_to_task[i])
            inp = input("Введите через пробел\nНачальная задача, следующая задача, наргада за переход\nПросто нажмите Enter чтобы завершить\n")
            if inp == '':
                break
            else:
                inp = inp.split()
                R[int(inp[0]),int(inp[1])] = int(inp[2])
            print(R)
        tasks = [x[1] for x in state_to_task.items()]
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
    print(R)
    print(state_to_task)
    decision = [int(x) for x in input("Введите число начальной задачи и конечно задачи через пробел\n").split()]
    # Printing the final route
    print('Результат:')
    for x in route(decision[0], decision[1],R,state_to_task):
        print(x,end='\n')

if __name__ == "__main__":
    main()