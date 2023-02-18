
import os
import re
import fileinput
import sys
from car import Car 

STEAM_PATHS = [

]

def get_car_paths():
    car_paths = []
    for steam_path in STEAM_PATHS:
        for root, dirs, files in os.walk(steam_path, topdown=False):
            for name in files:
                if name.startswith('config'):
                    car_paths.append(os.path.join(root, name))

        return car_paths

def get_full_name(path):
    name = os.path.join(os.path.dirname(path), 'name.txt')
    if os.path.exists(name):
        return open(name).read()
    
    else:
        for line in open(path).readlines():
            line = line.strip()
            if line.startswith('carVersion'):
                return line.split('=')[1]

def read_car_path(path):
    car_specs = {}
    car_specs['full_name'] = get_full_name(path)
    car_specs['car_path'] = os.path.dirname(path)
    for line in open(path).readlines():
        line = line.strip()
        if '=' not in line:
            continue
    
        car_specs[line.split('=')[0]] = line.split('=')[1]

    return car_specs

def get_all_swap_options(cars):
    engines = set()
    for car in cars:
        if car.specs.get('swapoptions'):
            car_swap_options = car.specs['swapoptions'].split(',')
            for engine in car_swap_options:
                if not engine:
                    continue
                engines.add(engine)

    return list(engines)

def replace(file, pattern, subst):
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    file_string = (re.sub(pattern, subst, file_string))

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()

def modify_swap_options(car, options):
    car_path = car.specs['car_path']
    replacement_options = 'swapoptions=' + ','.join(options)
    for filename in [filename for filename in os.listdir(car.specs['car_path']) if filename.startswith('config')]:
        config_path = os.path.join(car_path, filename)

















all_cars = []
for path in get_car_paths():
    specs = read_car_path(path)
    try:
        car = Car(specs['carBrand'], specs['full_name'], specs)
        all_cars.append(car)
    except:
        pass

all_swap_options = get_all_swap_options(all_cars)

for car in all_cars:
    modify_swap_options(car, all_swap_options)

print()