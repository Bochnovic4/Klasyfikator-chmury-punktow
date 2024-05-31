# colors
BACKGROUND_COLOR = "#2b2b2b"
WHITE = "#FFFFFF"
RED = "#8a0606"

# visualization colors
LABEL_COLORS = {
    0: [0, 0, 0],
    1: [0.5, 0.5, 0.5],
    2: [0, 1, 0],
    3: [0, 0.5, 0],
    4: [0, 0.8, 0],
    5: [0, 0.2, 0],
    6: [0.5, 0.5, 0.5],
    7: [0.8, 0.8, 0.8],
    9: [0, 0, 1],
    10: [0.8, 0.5, 0.2],
    11: [0, 1, 0],
    13: [0, 0.3, 0],
    14: [1, 0, 1],
    15: [0.65, 0.5, 0.39],
    16: [0.5, 0, 0.5],
    17: [0.3, 0.3, 0.3],
    18: [1, 1, 1],
    19: [1, 0, 0],
    25: [0.85, 0.85, 0.85],
}

# Liczba rdzeni do traningu modelu
N_JOBS = None

# Maksymalna glebokosc drzewa
MAX_DEPTH = None

# kolumny do treningu modelu
COLUMNS = ['z', 'intensity', 'number_of_returns', 'return_number', 'cylinder_density', 'normal_vectors_x', 'normal_vectors_y', 'normal_vectors_z', 'min_height', 'max_height', 'mean_height']
