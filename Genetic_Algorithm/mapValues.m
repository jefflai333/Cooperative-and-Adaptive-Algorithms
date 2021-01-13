function [kp, ti, td, x] = Binary_mapValues(x)
    kp_min = 2;
    kp_max = 18;
    ti_min = 1.05;
    ti_max = 9.42;
    td_min = 0.26;
    td_max = 2.37;
    % separate each value into kp, ti and td
    kp_binary = x(1:11);
    ti_binary = x(12:21);
    td_binary = x(22:29);
    kp = (bi2de(kp_binary)/100) + kp_min;
    ti = (bi2de(ti_binary)/100) + ti_min;
    td = (bi2de(td_binary)/100) + td_min;
    if kp > kp_max
        kp = kp_max;
        kp_binary = de2bi(1600);
    end
    if ti > ti_max
        ti = ti_max;
        ti_binary = de2bi(837);
    end
    if td > td_max
        td = td_max;
        td_binary = de2bi(211);
    end
    x = [kp_binary ti_binary td_binary];
end