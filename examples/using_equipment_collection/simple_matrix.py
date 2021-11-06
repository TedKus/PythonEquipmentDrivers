import pythonequipmentdrivers as ped
from time import sleep


# see file for equipment details and initialization
equipment = ped.connect_equipment(configuration='.\\equipment.config',
                                  init=True)

# conditions to test, test parameters, location to store data
v_in_conditions = (40, 48, 54, 60)
i_out_conditions = range(0, 120+1, 10)

measure_delay = 0.5
cooldown_delay = 5

output_data_file = 'C:\\top_sneaky\\test_data.csv'

# create file to store data using the utility function
ped.utility.log_data(output_data_file,
                     'v_in_set', 'i_out_set', 'v_in',         # columns names
                     'i_in', 'v_out', 'i_out', 'efficiency',  # of the data csv
                     init=True)

# run test
equipment.source.on()
equipment.sink.on()
for v_in_set in v_in_conditions:
    equipment.source.set_voltage(v_in_set)

    for i_out_set in i_out_conditions:
        print(f'Testing V_in = {v_in_set} V, I_out = {i_out_set} A')
        equipment.sink.set_current(i_out_set)

        sleep(measure_delay)
        measurement = [v_in_set, i_out_set,
                       equipment.v_in_meter.measure_voltage(),
                       equipment.source.measure_current(),
                       equipment.v_out_meter.measure_voltage(),
                       equipment.sink.measure_current()]

        equipment.sink.set_current(0)

        # calculations
        v_in, i_in, v_out, i_out = measurement[2:5+1]
        eff = (v_out*i_out)/(v_in*i_in)

        # add to data
        measurement.append(eff)

        # log measurements
        ped.utility.log_data(output_data_file, *measurement)

        sleep(cooldown_delay)  # cool down unit

# shutdown test setup
print('Test complete!')
equipment.source.set_voltage(0)
equipment.source.off()
equipment.sink.set_current(0)
equipment.sink.off()
