function [fitness] = calculate_fitness(x)
    ISE = x(1);
    t_r = x(2);
    t_s = x(3);
    M_p = x(4);
    adjustment_factor = 0.001;
    if isnan(ISE) || isnan(t_r) || isnan(t_s) || isnan(M_p)
        fitness = 0;
    else
        fitness_ISE = -0.11*(ISE-200)*adjustment_factor;
        if fitness_ISE < 0
            fitness_ISE = 0;
        end
        fitness_t_r = -4*(t_r-2)*adjustment_factor;
        if fitness_t_r < 0
            fitness_t_r = 0;
        end
        fitness_t_s = -2.5*(t_s-20)*adjustment_factor;
        if fitness_t_s < 0
            fitness_t_s = 0;
        end
        fitness_M_p = -2*(M_p-50)*adjustment_factor;
        if fitness_M_p < 0
            fitness_M_p = 0;
        end
        fitness = fitness_ISE + fitness_t_r + fitness_t_s + fitness_M_p;
    end
end