function [rand_population] = generateRandomValues(population)
    rand_population = zeros(population, 29);
    kp_min = 2;
    kp_max = 18;
    ti_min = 1.05;
    ti_max = 9.42;
    td_min = 0.26;
    td_max = 2.37;
    for i=1:population
        % shift the random value to the set ranges for each parameter
        kp = (kp_max-kp_min)*rand + kp_min;
        ti = (ti_max-ti_min)*rand + ti_min;
        td = (td_max-td_min)*rand + td_min;
        % round each answer to a precision of two decimal values
        % use these answers to convert to binary representation
        kp = de2bi(int16((round(kp, 2) - kp_min) * 100), 11);
        ti = de2bi(int16((round(ti, 2) - ti_min) * 100), 10);
        td = de2bi(int16((round(td, 2) - td_min) * 100), 8);
        rand_population(i,:) = [kp ti td];
    end     
end
