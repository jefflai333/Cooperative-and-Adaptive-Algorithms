import csv
import random
from itertools import combinations


def read_flow_and_distance_files():
    flow = []
    distance = []
    with open('flow.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            flow.append(row)
    with open('distance.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            distance.append(row)
    flow = [[int(i) for i in row] for row in flow]
    distance = [[int(i) for i in row] for row in distance]
    return flow, distance


def neighbourhood_function(solution, flow, distance):
    sum_of_products = 0
    for i in range(len(solution)):
        for j in range(len(solution)):
            flow_1 = solution[i] - 1
            flow_2 = solution[j] - 1
            sum_of_products = sum_of_products + flow[flow_1][flow_2] * distance[i][j]
    return sum_of_products


def one_swap_away(solution, smaller_neighbourhood):
    next_possible_solutions = []
    indexes = combinations([x for x in range(20)], 2)
    indexes = [list(index) for index in indexes]
    if smaller_neighbourhood:
        indexes = indexes[95:]
    for index in indexes:
        copied_solution = solution.copy()
        next_possible_solutions.append([swap_positions(copied_solution, index[0], index[1]), list(index)])
    return next_possible_solutions


def swap_positions(solution, index1, index2):
    solution[index1], solution[index2] = solution[index2], solution[index1]
    return solution


def subtract_one_from_tenure(tabu_list):
    for i in range(len(tabu_list)):
        for j in range(len(tabu_list[i])):
            if i < j and tabu_list[i][j] > 0:
                tabu_list[i][j] -= 1
    return tabu_list


def tabu(initial_solution, flow, distance, tabu_tenure_length=4, tabu_tenure_length_variable=False, best_solution_so_far=False, best_solution_in_neighbourhood=False, smaller_neighbourhood=False, frequency_list=False):
    max_num_iter_with_no_improvement = 100
    num_improved_iterations = 0
    # set tabu list to be a 20x20 array of 0s
    tabu_list = [[0 for x in range(20)] for y in range(20)]
    current_solution = initial_solution
    best_solution = initial_solution
    best_solution_value = neighbourhood_function(initial_solution, flow, distance)
    print("Initial Solution: " + str(initial_solution))
    print("Initial Solution Value: " + str(best_solution_value))
    tabu_tenure_counter = 0
    if tabu_tenure_length_variable:
        tabu_tenure_length = random.randint(3, 13)
    while num_improved_iterations < max_num_iter_with_no_improvement:
        # change tabu tenure length between a range of 3 and 13
        if tabu_tenure_length_variable and tabu_tenure_counter == 25:
            tabu_tenure_length = random.randint(3, 13)
            tabu_tenure_counter = 0
        # make a list of all the next possible solutions with one swap only
        candidate_list = one_swap_away(current_solution, smaller_neighbourhood)
        current_solution_value = neighbourhood_function(current_solution, flow, distance)
        # subtract the current solution value with each value in the one_swap_away candidates
        candidate_list = [[neighbourhood_function(candidate[0], flow, distance) - current_solution_value, candidate[1]] for candidate in candidate_list]
        candidate_list = sorted(candidate_list, key=lambda x: x[0])
        if frequency_list:
            candidate_list = [
                [candidate[0], candidate[1], tabu_list[candidate[1][1]][candidate[1][0]]] for
                candidate in candidate_list]
        # finds indexes where the tabu tenure is greater than 0
        current_tabu_list = [[i, j] for i, x in enumerate(tabu_list) for j, y in enumerate(x) if y > 0]
        aspiration_list = []
        if best_solution_so_far:
            aspiration_list = [candidate[1] for candidate in candidate_list if candidate[0] + current_solution_value < best_solution_value]
        if best_solution_in_neighbourhood:
            aspiration_list = [candidate_list[0][1]]
        # remove all candidates from candidate_list that are in current_tabu_list and not in aspiration_list
        candidate_list = [x for x in candidate_list if x[1] not in current_tabu_list or x[1] in aspiration_list]
        tabu_list = subtract_one_from_tenure(tabu_list)
        best_move = candidate_list[0]
        best_move_value = best_move[0]
        best_move_indexes = best_move[1]
        current_solution = swap_positions(current_solution, best_move_indexes[0], best_move_indexes[1])
        # set the recency tabu list to be the tabu_tenure_length
        tabu_list[best_move_indexes[0]][best_move_indexes[1]] = tabu_tenure_length
        # increase the frequency tabu list by 1 for this swap
        tabu_list[best_move_indexes[1]][best_move_indexes[0]] += 1
        # checks if this move is the best ever solution
        if current_solution_value + best_move_value < best_solution_value:
            best_solution = current_solution
            best_solution_value = current_solution_value + best_move_value
            num_improved_iterations = 0
        else:
            num_improved_iterations += 1
        tabu_tenure_counter += 1
    return best_solution, best_solution_value


if __name__ == "__main__":
    flow, distance = read_flow_and_distance_files()
    # randomly generate a solution to compare all other solutions to
    first_solution = [12, 11, 16, 18, 4, 10, 7, 5, 20, 17, 3, 2, 1, 8, 6, 19, 13, 14, 9, 15]
    # try 10 different initial solutions
    initial_solutions = [first_solution]
    # randomly generates 10 solutions and adds to the solutions list
    for i in range(10):
        initial_solution = [x+1 for x in range(20)]
        random.shuffle(initial_solution)
        initial_solutions.append(initial_solution)
    # runs tabu search through each one and prints the final solution and its value
    for i in range(11):
        sol, val = tabu(initial_solutions[i], flow, distance)
        print("Final Solution: " + str(sol))
        print("Final Solution Value: " + str(val))
    # try with different tabu list lengths
    # try with a tabu_tenure_length of 3 and then 13
    tabu_tenure_lengths = [3, 8]
    for i in range(len(tabu_tenure_lengths)):
        first_solution = [12, 11, 16, 18, 4, 10, 7, 5, 20, 17, 3, 2, 1, 8, 6, 19, 13, 14, 9, 15]
        tabu_tenure_length = tabu_tenure_lengths[i]
        print("Tabu Tenure Length: " + str(tabu_tenure_length))
        sol, val = tabu(first_solution, flow, distance, tabu_tenure_length)
        print("Final Solution: " + str(sol))
        print("Final Solution Value: " + str(val))
    # tabu list size varying
    first_solution = [12, 11, 16, 18, 4, 10, 7, 5, 20, 17, 3, 2, 1, 8, 6, 19, 13, 14, 9, 15]
    print("Tabu Tenure Length: Varying between 3 and 8")
    sol, val = tabu(first_solution, flow, distance, tabu_tenure_length_variable=True)
    print("Final Solution: " + str(sol))
    print("Final Solution Value: " + str(val))
    # aspiration of best solution so far
    print("Aspiration List: Best Solution So Far")
    sol, val = tabu(first_solution, flow, distance, best_solution_so_far=True)
    print("Final Solution: " + str(sol))
    print("Final Solution Value: " + str(val))
    print("Aspiration List: Best Solution In Neighbourhood")
    sol, val = tabu(first_solution, flow, distance, best_solution_in_neighbourhood=True)
    print("Final Solution: " + str(sol))
    print("Final Solution Value: " + str(val))
    print("Aspiration List: Best Solution In Neighbourhood")
    sol, val = tabu(first_solution, flow, distance, best_solution_in_neighbourhood=True)
    print("Final Solution: " + str(sol))
    print("Final Solution Value: " + str(val))
    print("Smaller Neighbourhood: ")
    sol, val = tabu(first_solution, flow, distance, smaller_neighbourhood=True)
    print("Final Solution: " + str(sol))
    print("Final Solution Value: " + str(val))
    print("Frequency List: ")
    sol, val = tabu(first_solution, flow, distance, frequency_list=True)
    print("Final Solution: " + str(sol))
    print("Final Solution Value: " + str(val))