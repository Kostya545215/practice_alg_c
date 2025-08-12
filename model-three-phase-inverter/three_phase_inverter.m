function three_phase_inverter(config, csv_path, options)

    % 
    arguments
        config string
        csv_path string
        options.Time_simulation (1,1) int32 = 0.1
        options.Threshold_voltage (1,1) double
        options.off_state_conductance (1,1) double
        options.drain_source_on_resistance (1,1) double
        options.Diode_forward_voltage (1,1) double
    end

    T = readtable('params.csv', 'TextType', 'string');
    
    model = 'three0x2Dphase0x2Dinventer1';

    load_system(model);

    modelWs = get_param(model, 'ModelWorkspace');
    assignin(modelWs, 'Threshold_voltage', T.Threshold_voltage(T.Name == config));
    set_param(model, 'StopTime', num2str(options.Time_simulation*1000));  % умножение на 1000, тк вводим реальное желаемое время симуляции
                                                                          % а наша модель работает в 1000 раз медленнее
    
    sim(model);

    F = load('test.mat');
    
    csv_data = [F.test.Time, squeeze(F.test.Data(1, 1:3, :))'];
    col_names = {'Time', 'sin1', 'sin2', 'sin3'};
    result_table = array2table(csv_data, 'VariableNames', col_names);
    writetable(result_table, csv_path);

end