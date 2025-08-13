function three_phase_inverter(config, csv_path, options)

% THREE_PHASE_INVERTER Генерация трехфазного инвертора с сохранением данных
%
%   THREE_PHASE_INVERTER(CONFIG, CSV_PATH, OPTIONS) создает модель трехфазного
%   инвертора и сохраняет результаты в CSV-файл.
%
%   Входные параметры:
%       CONFIG    - Название конфигурации в файле params.csv (например, 'config1')
%       CSV_PATH  - Полный путь к файлу для сохранения (например, 'C:\data.csv')
%       OPTIONS   - Структура с параметрами:
%           * Time_simulation       - Время симуляции (sec, по умолчанию 0.1)
%           * R_load                - Сопротивление нагрузки (ohm, по умолчанию 50)
%           * C_load                - Ёмкость нагрузки (H, по умолчанию 0.01)
%           * L_load                - Индуктивность нагрузки (F, по умолчанию 0.0001)
%           * Voltage               - Напряжение источника (V, по умолчанию 50)
    arguments
        config string
        csv_path string
        options.Time_simulation (1,1) double = 0.1
        options.R_load (1,1) double = 50
        options.C_load (1,1) double = 0.01
        options.L_load (1,1) double = 0.0001
        options.voltage (1,1) double = 50
    end

    T = readtable('params.csv', 'TextType', 'string');
    
    model = 'three0x2Dphase0x2Dinventer1';

    load_system(model);

    modelWs = get_param(model, 'ModelWorkspace');
    assignin(modelWs, 'Threshold_voltage', T.Threshold_voltage(T.Name == config));
    assignin(modelWs, 'off_state_conductance', T.off_state_conductance(T.Name == config));
    assignin(modelWs, 'drain_source_on_resistance', T.drain_source_on_resistance(T.Name == config));
    assignin(modelWs, 'Diode_forward_voltage', T.Diode_forward_voltage(T.Name == config));

    set_param(model, 'StopTime', num2str(options.Time_simulation*1000));  % умножение на 1000, тк вводим реальное желаемое время симуляции
                                                                          % а наша модель работает в 1000 раз медленнее
    sim(model);

    F = load('values_current.mat');
    G = load('values_voltage.mat');

    csv_data = [F.values_current.Time, squeeze(F.values_current.Data(1, 1:3, :))', squeeze(G.values_voltage.Data(1, 1:3, :))'];
    col_names = {'Time', 'current1', 'current2', 'current3', 'voltage1', 'voltage2', 'voltage3'};
    result_table = array2table(csv_data, 'VariableNames', col_names);
    writetable(result_table, csv_path);

end