#!/usr/bin/env python3

import temperature.temperature_reader

temp_reader = temperature.temperature_reader.TemperatureReader()

t_c = temp_reader.read_temp_c()
t_f = temp_reader.read_temp_f()
print(
    "Current Temperature: {c:4.0f} C --- ### {f:4.0f} F ###    === {c:8.4f} C --- {f:8.4f} F".format(c=t_c, f=t_f))
