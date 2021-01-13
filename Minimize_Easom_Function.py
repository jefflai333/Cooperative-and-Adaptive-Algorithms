import math
from math import cos, exp, pi, sin
from random import uniform, random


def distance(point1):
    return math.sqrt(pow(point1[0] - pi, 2) + pow(point1[1] - pi, 2))


def easom(x):
    return -cos(math.radians(x[0])) * cos(math.radians(x[1])) * exp(-pow((x[0] - pi), 2) - pow((x[1] - pi), 2))


def temperature_reduction(annealing_schedule, alpha, temperature):
    if annealing_schedule == "lin":
        return temperature - alpha
    elif annealing_schedule == "exp":
        return pow(temperature, alpha)
    elif annealing_schedule == "slow":
        return temperature / (1 + alpha * temperature)
    else:
        # default annealing schedule is linear
        return temperature - alpha


def cost_function(cost, curr_temp):
    return exp(-cost / (curr_temp * 0.001))


def neighbouring_function(curr_solution, curr_temp):
    # make sure that the neighbouring solution is within the bounds
    # randomize the direction that the neighbouring solution will go towards
    magnify_curr_temp = 0.1
    exponent_curr_temp = 0.05
    equation = magnify_curr_temp * exp(curr_temp * exponent_curr_temp)
    while True:
        random_radians = uniform(0, 2 * pi)
        if -100 < curr_solution[0] + equation * sin(
                random_radians) < 100 and -100 < curr_solution[1] + equation * cos(random_radians) < 100:
            break
    return [curr_solution[0] + equation * sin(random_radians), curr_solution[1] + equation * cos(random_radians)]


def simulated_annealing(init_temp, init_solution, alpha, iterations, annealing_schedule):
    curr_solution = init_solution
    curr_temp = init_temp
    count = 0
    max_attempts = 10000
    if annealing_schedule == "lin":
        min_temp = 0
    elif annealing_schedule == "exp":
        min_temp = 1.1
    elif annealing_schedule == "slow":
        min_temp = 0.01
        # set iterations to 1 for slow annealing schedule
        iterations = 1
    else:
        min_temp = 1.1
    while curr_temp > min_temp:
        for j in range(iterations):
            neighbouring_solution = neighbouring_function(curr_solution, curr_temp)
            cost_neighbouring_solution = easom(neighbouring_solution)
            cost_curr_solution = easom(curr_solution)
            cost = cost_neighbouring_solution - cost_curr_solution
            if cost < 0:
                curr_solution = neighbouring_solution
                count = 0
            else:
                x = random()
                if x < cost_function(cost, curr_temp):
                    curr_solution = neighbouring_solution
                    count = 0
                else:
                    count += 1
            # if no progress has been made after x attempts, then return the solution
            if count > max_attempts:
                return curr_solution
        curr_temp = temperature_reduction(annealing_schedule, alpha, curr_temp)
    return curr_solution


if __name__ == '__main__':
    random_init = []
    random_temp = []
    annealing_schedules = [[1, "lin"], [2, "lin"], [4, "lin"], [0.95, "exp"], [0.85, "exp"], [0.75, "exp"], [0.05, "slow"], [0.15, "slow"], [0.25, "slow"]]
    answers = []
    for i in range(10):
        # add a random point in between -100 and 100 for x and y and do it 10 times
        random_init.append([uniform(-100, 100), uniform(-100, 100)])
        random_temp.append(uniform(80, 100))
    num_iterations = 1
    for i in range(10):
        for j in range(10):
            for k in range(len(annealing_schedules)):
                print("Simulated Annealing Round " + str(num_iterations))
                curr_sol = simulated_annealing(random_temp[i], random_init[j], annealing_schedules[k][0], 1000, annealing_schedules[k][1])
                # calculate distance from optimal solution
                min_distance = distance(curr_sol)
                answers.append([random_temp[i], random_init[j], annealing_schedules[k], curr_sol, min_distance])
                num_iterations += 1
    answers = sorted(answers, key=lambda x: x[4], reverse=True)
    # print all answers, the answer at the end of the array will be the best solution
    for i in range(len(answers)):
        print(answers[i])
    print(random_temp)
    print(random_init)
