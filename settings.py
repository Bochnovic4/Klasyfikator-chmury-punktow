# default values


# colors
BACKGROUND_COLOR = "#2b2b2b"
WHITE = "#FFFFFF"
RED = "#8a0606"
LABEL_COLORS = {
0: [0, 0, 0], # Never classified (Black)
1: [0.5, 0.5, 0.5], # Unassigned (Gray)
2: [0, 1, 0], # Ground (Green)
3: [0, 0.5, 0], # Low Vegetation (Dark Green)
4: [0, 0.8, 0], # Medium Vegetation (Light Green)
5: [0, 0.2, 0], # High Vegetation (Very Dark Green)
6: [0.5, 0.5, 0.5], # Building (Gray)
7: [0.8, 0.8, 0.8], # Low Point (Light Gray)
9: [0, 0, 1], # Water (Blue)
10: [0.8, 0.5, 0.2], # Rail (Brownish)
11: [0, 1, 0], # grass (Green)
13: [0, 0.3, 0], # unknown (Dark Green)
14: [1, 0, 1], # Wire - Conductor (Magenta)
15: [0.65, 0.50, 0.39], # Buildings (Walnut)
16: [0.5, 0, 0.5], # Wire-Structure Connector (Purple)
17: [0.3, 0.3, 0.3], # street (Dark Gray)
18: [1, 1, 1], # High Noise (White)
19: [1, 0, 0], # Wires (Red)
25: [0.85, 0.85, 0.85] # road (Gray)
}
# Liczba rdzeni do traningu modelu
N_JOBS = -1
# kolumny do treningu modelu
COLUMNS = ['x', 'y', 'z']
# rozmiar voxela do downsamplingu
VOXEL_SIZE = 0.5
