import numpy as np
import matplotlib.pyplot as plt

import sys
import re

if __name__=='__main__':
    if len(sys.argv) <= 1:
        print('specify gcode file', file=sys.stderr)
        exit(1)
        
    gcode_file_name = sys.argv[1]

    with open(gcode_file_name) as gcode_file:
        gcode_lines = gcode_file.readlines()
        
    moves = filter(lambda l : l.startswith('G1'), gcode_lines)
    moves = list(moves)
    
    move_regexp = re.compile(r'G1\s*(X([^ ]*))?\s*(Y([^ ]*))?\s*(Z([^ ]*))?')
    moves_matches = map(lambda l : re.search(move_regexp, l), moves)
    moves_matches = map(lambda l : (l.group(2), l.group(4), l.group(6)), moves_matches)
    moves_matches = list(moves_matches)
    
    waypoints = [(0,0,0)]
    
    for p in moves_matches:
        x_s, y_s, z_s = p
        x_prev, y_prev, z_prev = waypoints[-1]
        
        x = x_prev if x_s is None else float(x_s)
        y = y_prev if y_s is None else float(y_s)
        z = z_prev if z_s is None else float(z_s)
        
        waypoints.append((x,y,z))

    waypoints = np.array(waypoints)
    print(waypoints.shape)

    ax = plt.axes(projection='3d')
    plt.plot(waypoints[:,0], waypoints[:,1], waypoints[:,2])
    plt.show()