import itertools

from utils import read_input


def product_of_ranges(input):
    vars = {}
    cuboids = set()
    for line in input:
        step = line.split(',')
        on_off = step[0].split()[0]
        skip = False
        for d in step:
            values = list(map(int, d.split('=')[1].replace('..', ',').split(',')))
            vars[d.split('=')[0][-1]] = set(range(values[0], values[1]+1))
            if 50 < values[1] or -50 > values[0]:
                skip = True
        if skip:
            continue
        cartesian_product = itertools.product(*vars.values())
        for p in cartesian_product:
            if on_off == 'on':
                cuboids.add(p)
            elif on_off == 'off':
                cuboids -= {p}
        #print(len(cuboids))
    return len(cuboids)


def get_intersections(cubes, new):
    #print("new", new)
    intersections = []
    for cube in cubes:
        #print("c", cube)
        cube_state = cube.get('state')
        # If new True, cube True, then new state False
        # If new True, cube False, then state True
        # If new False, cube False, then state True
        # If new False, cube True, then state False
        intersection = {'state': not cube_state}

        inter = True

        for v, mm in cube.items():
            if v == 'state':
                continue

            inter_v = False

            if new[v]['min'] in range(mm['min'], mm['max'] +1): # Intersection exists: new min in mm
                i_min = new[v]['min']
                inter_v = True

            if new[v]['max'] in range(mm['min'], mm['max'] +1):  # Intersection exists: new max in mm
                i_max = new[v]['max']
                if not inter_v: # Only new max intersection
                    i_min = mm['min']
                    inter_v = True
            else:
                if inter_v: # Ony new min intersection
                    i_max = mm['max']

            if not inter_v:
                if mm['min'] in range(new[v]['min'], new[v]['max'] + 1):  # Intersection exists: mm min in new
                    i_min = mm['min']
                    inter_v = True

                if mm['max'] in range(new[v]['min'], new[v]['max'] + 1):  # Intersection exists: mm max in new
                    i_max = mm['max']
                    if not inter_v:  # Only max intersection
                        i_min = new[v]['min']
                else:
                    if inter_v:  # Ony min intersection
                        i_max = new[v]['max']
                    else:  # No intersection
                        inter = False
                        break
            intersection[v] = {'min': i_min, 'max': i_max}
        if inter:
            #print("intersection", intersection)
            intersections.append(intersection)
    return intersections


def get_number_of_cuboids(c):
    n = 1
    for v, mm in c.items():
        if v == 'state':
            continue
        n *= (max(mm['max'] - mm['min'], mm['min'] - mm['max']) + 1)
    return n


def get_cuboids_on(input):
    cuboids = []
    turned_on = 0
    for line in input:
        #print(turned_on)
        step = line.split(',')
        cuboid = {'state': True if step[0].split()[0] == 'on' else False}

        for d in step:
            min_max_values = list(map(int, d.split('=')[1].replace('..', ',').split(',')))
            cuboid[d.split('=')[0][-1]] = {'min': min_max_values[0], 'max': min_max_values[1]}

        intersections = get_intersections(cuboids, cuboid)

        for intersection in intersections:
            cuboids.append(intersection)
            if intersection['state'] == True:
                turned_on += get_number_of_cuboids(intersection)
            elif intersection['state'] == False:
                turned_on -= get_number_of_cuboids(intersection)

        if cuboid['state'] == True:
            cuboids.append(cuboid)
            turned_on += get_number_of_cuboids(cuboid)

    return turned_on


debug = False
files = ['example.txt', 'own_example.txt', 'example2.txt', 'example3.txt', 'input.txt', 'input2.txt']

for f in files:

    input = read_input(f)

    # Not efficient
    p1 = product_of_ranges(input)
    print(f"{f} - Part 1: {p1}")

    # Works but could be improved using named tuples instead
    p2 = get_cuboids_on(input)
    print(f"{f} - Part 2: {p2}")
