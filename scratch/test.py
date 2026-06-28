import sys
sys.path.append('c:\\Study\\AI\\Final_project_pygame')
from algorithms.complex_env import partial_observation_search
grid = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
try:
    gen = partial_observation_search(grid, (0,0), [(0,2), (3,3)])
    print(f"Total states: {len(gen)}")
except Exception as e:
    import traceback
    traceback.print_exc()
