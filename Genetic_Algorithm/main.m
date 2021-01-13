population = 50;
crossover_probability = 0.6;
mutation_probability = 0.03;
max_num_generations = 150;
curr_num_generation = 0;
initial_generation = generateRandomValues(population);
initial_fitness_arr = zeros(population, 1);
final_solution = zeros(population, 3);
curr_generation = initial_generation;
curr_fitness_arr = initial_fitness_arr;
chromosome_length = 29;
% the representation has 29 bits so the array has 29 columns
parents_selected = zeros(population, chromosome_length);
children_selected = zeros(population, chromosome_length);
best_fitness_arr = [];
best_kp_arr = [];
best_ti_arr = [];
best_td_arr = [];
best_ISE_arr = [];
best_t_r_arr = [];
best_t_s_arr = [];
best_M_p_arr = [];
index_arr = size(population, max_num_generations);
while curr_num_generation < max_num_generations
    curr_num_generation
    % calculate fitness function
    for i = 1:population
        % map chromsomes to the appropriate range
        [curr_kp, curr_ti, curr_td, x] = mapValues(curr_generation(i,:));
        curr_generation(i,:) = x;
        % find current values of perfFCN
        [curr_ISE, curr_t_r, curr_t_s, curr_M_p] = perfFCN([curr_kp; curr_ti; curr_td]);
        curr_fitness = calculate_fitness([curr_ISE, curr_t_r, curr_t_s, curr_M_p]);
        % add current fitness into the current fitness array
        curr_fitness_arr(i) = curr_fitness;
    end
    curr_best_fitness_arr = curr_fitness_arr;
    [best_fitness, index] = max(curr_best_fitness_arr);
    index_arr(1, curr_num_generation+1) = index;
    parents_selected(1,:) = curr_generation(index,:); 
    [curr_kp, curr_ti, curr_td] = mapValues(curr_generation(index,:));
    [best_ISE, best_t_r, best_t_s, best_M_p] = perfFCN([curr_kp; curr_ti; curr_td]);
     % set the best value to 0 so it is no longer the best value
    curr_best_fitness_arr(index) = 0;
    best_fitness_arr = [best_fitness_arr best_fitness];
    best_kp_arr = [best_kp_arr curr_kp];
    best_ti_arr = [best_ti_arr curr_ti];
    best_td_arr = [best_td_arr curr_td];
    best_ISE_arr = [best_ISE_arr best_ISE];
    best_t_r_arr = [best_t_r_arr best_t_r];
    best_t_s_arr = [best_t_s_arr best_t_s];
    best_M_p_arr = [best_M_p_arr best_M_p];
    % this will now get the second best value in the array
    [~, index] = max(curr_best_fitness_arr);
    index_arr(2, curr_num_generation+1) = index;
    parents_selected(2,:) = curr_generation(index,:);     
    % calculate each probability using FPS
    curr_fitness_arr = bsxfun(@rdivide, curr_fitness_arr, sum(curr_fitness_arr));
    % create ranges to pick probabilities from
    curr_fitness_arr = cumsum(curr_fitness_arr);
    % spin roulette wheel n-2 times
    for i = 3:population
        rand_num = rand;
        % find index where the random number lands
        index = find(curr_fitness_arr > rand_num, 1);
        index_arr(i, curr_num_generation+1) = index;
        % add the curr_generation into the parent selection array
        parents_selected(i,:) = curr_generation(index,:); 
    end
    % shuffles array
    parents_selected = parents_selected(randperm(size(parents_selected, 1)), :);
    % use uniform crossover
    for i = 1:population/2
        rand_num = rand;
        index_1 = 2*i-1;
        index_2 = 2*i;
        if rand_num < crossover_probability
            parent_1 = parents_selected(index_1,:);
            parent_2 = parents_selected(index_2,:);
            for j = 1:chromosome_length
                coin_flip = rand;
                % depending on result of coin flip, assign the chromosome
                % accordingly
                if coin_flip > 0.5
                     children_selected(index_1,j) = parent_1(j);
                     children_selected(index_2,j) = parent_2(j);
                else
                     children_selected(index_1,j) = parent_2(j);
                     children_selected(index_2,j) = parent_1(j);
                end
            end
        else
            children_selected(index_1,:) = parents_selected(index_1,:);
            children_selected(index_2,:) = parents_selected(index_2,:);
        end
    end
    % use uniform mutation
    for i = 1:population
        for j = 1:chromosome_length
            rand_num = rand;
            if rand_num < mutation_probability
                % flips the mutated bit
                children_selected(i,j) = ~children_selected(i,j);
            end
        end
    end
    curr_generation = children_selected;
    curr_num_generation = curr_num_generation + 1;
end
for i = 1:population
    % map chromsomes to the appropriate range
    [curr_kp, curr_ti, curr_td] = mapValues(curr_generation(i,:));
    % find current values of perfFCN
    [curr_ISE, curr_t_r, curr_t_s, curr_M_p] = perfFCN([curr_kp; curr_ti; curr_td]);
    final_solution(i,:) = [curr_kp, curr_ti, curr_td];
end
num_generations = 1:max_num_generations;

figure(1)
plot(num_generations, best_fitness_arr)
title("Best fitness")
xlabel('Generation Number') 
ylabel('Fitness Value') 
figure(2)
plot(num_generations, best_kp_arr)
title("Best Kp")
figure(3)
plot(num_generations, best_ti_arr)
title("Best Ti")
figure(4)
plot(num_generations, best_td_arr)
title("Best Td")
figure(5)
plot(num_generations, best_ISE_arr)
title("Best ISE")
figure(6)
plot(num_generations, best_t_r_arr)
title("Best Tr")
figure(7)
plot(num_generations, best_t_s_arr)
title("Best Ts")
figure(8)
plot(num_generations, best_M_p_arr)
title("Best Mp")
last_best_kp = best_kp_arr(1, max_num_generations)
last_best_ti = best_ti_arr(1, max_num_generations)
last_best_td = best_td_arr(1, max_num_generations)