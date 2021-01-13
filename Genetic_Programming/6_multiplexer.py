import copy
import random
import matplotlib.pyplot as plt

function_set = {"AND", "OR", "NOT", "IF"}
terminal_set = {"a0", "a1", "d0", "d1", "d2", "d3"}
mutation_probability = 0.05
crossover_probability = 0.7
population_size = 2500
max_number_no_improved_best_fitness = 15


def and_function(x, y):
    return x and y


def or_function(x, y):
    return x or y


def not_function(x):
    return not x


def if_function(x, y, z):
    if x:
        return y
    else:
        return z


def convert(value, input_set):
    if value == "a0":
        return input_set[0]
    elif value == "a1":
        return input_set[1]
    elif value == "d0":
        return input_set[2]
    elif value == "d1":
        return input_set[3]
    elif value == "d2":
        return input_set[4]
    else:
        return input_set[5]


def calculate_set(input_set):
    a0 = input_set[0]
    a1 = input_set[1]
    d0 = input_set[2]
    d1 = input_set[3]
    d2 = input_set[4]
    d3 = input_set[5]
    if a0 == 0 and a1 == 0:
        return d0
    elif a0 == 0 and a1 == 1:
        return d1
    elif a0 == 1 and a1 == 0:
        return d2
    else:
        return d3


def calculate_fitness(tree, total_input_set):
    count = 0
    for input_set in total_input_set:
        if calculate_set(input_set) == tree.calculate_tree(input_set):
            count += 1
    return count/len(total_input_set)


def crossover(tree1, tree2):
    # declare random node to be the point of crossover for each tree
    tree1_node = random.randint(1, tree1.size())
    tree2_node = random.randint(1, tree2.size())
    # find subtrees based on the random node
    tree1_subtree = tree1.sub_tree(tree1_node)
    tree2_subtree = tree2.sub_tree(tree2_node)
    tree1_size = tree1.size()
    tree2_size = tree2.size()
    tree1_subtree_size = tree1_subtree.size()
    tree2_subtree_size = tree2_subtree.size()
    # if the tree and subtree are same size, root case, set the tree to be the other tree's subtree
    if tree1_size == tree1_subtree_size:
        tree1 = tree2_subtree
    # otherwise add this subtree to the other tree
    else:
        tree1.add_sub_tree(tree1_node, tree2_subtree)
    # if the tree and subtree are same size, root case, set the tree to be the other tree's subtree
    if tree2_size == tree2_subtree_size:
        tree2 = tree1_subtree
    # otherwise add this subtree to the other tree
    else:
        tree2.add_sub_tree(tree2_node, tree1_subtree)
    # reset pointers for parents and counters
    tree1.set_parents()
    tree_count = tree1.size()
    tree1.set_counters([tree_count])
    tree2.set_parents()
    tree_count2 = tree2.size()
    tree2.set_counters([tree_count2])
    return tree1, tree2


class Tree:
    # default constructor to create a node
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.middle = None
        self.right = None
        self.parent = None
        self.counter = None
        self.position = None

    def set_parents(self):
        if self.left:
            self.left.parent = self
            self.left.position = "left"
            self.left.set_parents()
        if self.middle:
            self.middle.parent = self
            self.middle.position = "middle"
            self.middle.set_parents()
        if self.right:
            self.right.parent = self
            self.right.position = "right"
            self.right.set_parents()

    def set_counters(self, num_nodes):
        self.counter = num_nodes[0]
        num_nodes[0] -= 1
        if self.left:
            self.left.set_counters(num_nodes)
        if self.middle:
            self.middle.set_counters(num_nodes)
        if self.right:
            self.right.set_counters(num_nodes)

    def print_tree(self, depth=0, position="root"):
        if self.parent:
            print(self.value + ", " + str(depth) + ", " + position + ", " + self.parent.value + ", " + str(self.counter))
        else:
            print(self.value + ", " + str(depth) + ", " + position + ", " + str(self.counter))
        if self.left:
            self.left.print_tree(depth=depth + 1, position="left")
        if self.middle:
            self.middle.print_tree(depth=depth + 1, position="middle")
        if self.right:
            self.right.print_tree(depth=depth + 1, position="right")

    def calculate_tree(self, input_set):
        if self.value in function_set:
            if self.value == "AND":
                return and_function(self.left.calculate_tree(input_set), self.right.calculate_tree(input_set))
            elif self.value == "OR":
                return or_function(self.left.calculate_tree(input_set), self.right.calculate_tree(input_set))
            elif self.value == "NOT":
                return not_function(self.middle.calculate_tree(input_set))
            elif self.value == "IF":
                left_tree = self.left.calculate_tree(input_set)
                middle_tree = self.middle.calculate_tree(input_set)
                right_tree = self.right.calculate_tree(input_set)
                return if_function(left_tree, middle_tree, right_tree)
        elif self.value in terminal_set:
            return convert(self.value, input_set)
        else:
            return self.value

    def generate_random_tree(self, max_depth, depth=0):
        if depth < max_depth:
            random_num = random.random()
            # 50% chance for it to create a terminal node compared to function node
            if random_num < 0.5:
                self.value = random.sample(terminal_set, 1)[0]
            else:
                self.value = random.sample(function_set, 1)[0]
                # since a function set is generated, more nodes must be generated to create an acceptable tree
                if self.value == "AND" or self.value == "OR":
                    self.left = Tree()
                    self.left.generate_random_tree(max_depth, depth=depth + 1)
                    self.right = Tree()
                    self.right.generate_random_tree(max_depth, depth=depth + 1)
                elif self.value == "NOT":
                    self.middle = Tree()
                    self.middle.generate_random_tree(max_depth, depth=depth + 1)
                else:
                    self.left = Tree()
                    self.left.generate_random_tree(max_depth, depth=depth + 1)
                    self.right = Tree()
                    self.right.generate_random_tree(max_depth, depth=depth + 1)
                    self.middle = Tree()
                    self.middle.generate_random_tree(max_depth, depth=depth + 1)
        else:
            self.value = random.sample(terminal_set, 1)[0]

    def size(self):
        if self.value in terminal_set:
            return 1
        if self.left:
            left = self.left.size()
        else:
            left = 0
        if self.middle:
            middle = self.middle.size()
        else:
            middle = 0
        if self.right:
            right = self.right.size()
        else:
            right = 0
        # the 1 is to compensate for the current node
        return 1 + left + middle + right

    def sub_tree(self, node_number):
        if node_number == self.counter:
            return copy.deepcopy(self)
        else:
            ans = None
            if self.left and not ans:
                ans = self.left.sub_tree(node_number)
            if self.middle and not ans:
                ans = self.middle.sub_tree(node_number)
            if self.right and not ans:
                ans = self.right.sub_tree(node_number)
            return ans
        return None

    def add_sub_tree(self, node_number, sub_tree):
        if node_number == self.counter:
            if self.position == "left":
                self.parent.left = sub_tree
            elif self.position == "middle":
                self.parent.middle = sub_tree
            elif self.position == "right":
                self.parent.right = sub_tree
        else:
            if self.left:
                self.left.add_sub_tree(node_number, sub_tree)
            if self.middle:
                self.middle.add_sub_tree(node_number, sub_tree)
            if self.right:
                self.right.add_sub_tree(node_number, sub_tree)


if __name__ == "__main__":
    # create the input sets
    input_sets = [x for x in range(64)]
    # convert to binary
    input_sets = [list('{0:06b}'.format(x)) for x in input_sets]
    for i in range(len(input_sets)):
        for j in range(len(input_sets[0])):
            input_sets[i][j] = int(input_sets[i][j])
    init_generation = []
    best_fitness = []
    tree_size = []
    maximum_depth = 4
    for i in range(population_size):
        new_tree = Tree()
        new_tree.generate_random_tree(maximum_depth)
        tree_size.append(new_tree.size())
        new_tree.set_counters([new_tree.size()])
        new_tree.set_parents()
        init_generation.append([new_tree])
    updated_generation = init_generation
    best_tree = Tree()
    best_fitness_score = 0
    total_generations = 1
    number_no_improved_best_fitness = 0
    # keep iterating until either an optimal solution is reached or the solution has not improved in x amount of iterations
    while number_no_improved_best_fitness < max_number_no_improved_best_fitness:
        curr_generation = updated_generation
        # select best parents
        for j in range(population_size):
            fitness = calculate_fitness(curr_generation[j][0], input_sets)
            curr_generation[j] = [curr_generation[j][0], fitness]
        # sort generation to figure out best candidates
        curr_generation = sorted(curr_generation, key=lambda x: x[1], reverse=True)
        curr_best_fitness = curr_generation[0][1]
        # update best tree and best fitness score if the best ever fitness score has been improved
        if curr_best_fitness > best_fitness_score:
            best_tree = copy.deepcopy(curr_generation[0][0])
            print(curr_best_fitness)
            best_fitness_score = curr_best_fitness
            number_no_improved_best_fitness = 0
        else:
            number_no_improved_best_fitness += 1
        # exit code if fitness is 1, since that means an optimal solution has been found
        if curr_best_fitness == 1:
            break
        # add current best fitness to best fitness list to plot
        best_fitness.append(curr_best_fitness)
        updated_generation = []
        # pick parents by using tournament selection
        for j in range(population_size):
            # pick a random amount of individuals to participate in the tournament
            num_in_tourney = random.randint(1, population_size)
            # select these amount of individuals randomly from the generation
            candidates_in_tourney = random.sample(curr_generation, num_in_tourney)
            # find the best performing candidate
            candidates_in_tourney = sorted(candidates_in_tourney, key=lambda x: x[1], reverse=True)
            # add the best performing candidate into the updated generation
            best_candidate = copy.deepcopy(candidates_in_tourney[0])
            updated_generation.append(best_candidate)
        # shuffle updated_generation
        random.shuffle(updated_generation)
        j = 0
        while j < population_size - 2:
            # have a random number to determine whether or not mutation or crossover is performed
            random_num = random.random()
            curr_tree = copy.deepcopy(updated_generation[j][0])
            if random_num < mutation_probability:
                size_tree = curr_tree.size()
                random_tree = Tree()
                random_tree.generate_random_tree(maximum_depth)
                random_node = random.randint(1, size_tree)
                # find a random subtree based on a random integer
                random_subtree = curr_tree.sub_tree(random_node)
                # if the subtree is the size of the tree, root case, set the current tree to be the random tree
                if random_subtree.size() == curr_tree.size():
                    curr_tree = random_tree
                else:
                    curr_tree.add_sub_tree(random_node, random_tree)
                curr_tree.set_parents()
                curr_tree.set_counters([curr_tree.size()])
                updated_generation[j][0] = copy.deepcopy(curr_tree)
                j += 1
            # if random_num is within crossover probability and having two parents won't exceed the population size
            elif random_num < crossover_probability and j+1 < population_size:
                curr_tree2 = updated_generation[j+1][0]
                swapped_tree1, swapped_tree2 = crossover(curr_tree, curr_tree2)
                updated_generation[j][0] = copy.deepcopy(swapped_tree1)
                updated_generation[j+1][0] = copy.deepcopy(swapped_tree2)
                j += 2
            # do nothing
            else:
                j += 1
        # apply elitism so that previous two best solutions are kept
        updated_generation.append(copy.deepcopy(curr_generation[0]))
        updated_generation.append(copy.deepcopy(curr_generation[1]))
        print("Number of Generations Done: " + str(total_generations))
        total_generations += 1
    best_tree.print_tree()
    print("Best Fitness Score: " + str(best_fitness_score))
    fig, ax = plt.subplots()
    generations = [x for x in range(len(best_fitness))]
    ax.plot(generations, best_fitness)
    ax.set_xticks(range(0, len(best_fitness), 1))
    ax.set(xlabel='Number of Generations', ylabel='Fitness', title='Fitness vs Number of Generations')
    fig.savefig("Fitness.png")
    new_tree = Tree("IF")
    new_tree.left = Tree("a0")
    new_tree.middle = Tree("IF")
    new_tree.middle.right = Tree("d2")
    new_tree.middle.middle = Tree("d3")
    new_tree.middle.left = Tree("a1")
    new_tree.right = Tree("IF")
    new_tree.right.left = Tree("a1")
    new_tree.right.middle = Tree("d1")
    new_tree.right.right = Tree("d0")
    # new_tree.print_tree()
    # print(calculate_fitness(new_tree, input_sets))