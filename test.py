from envs.sibrivalry.toy_maze import MultiGoalPointMaze2D
from envs.sibrivalry.toy_maze.rubber_leash_maze import CustomMultiGoalPointMaze2D

env = CustomMultiGoalPointMaze2D(test=False, maze_type="16x16", elasticity_coef=0.8)
#env.step(action=[0.25, 0.25])
for i in range(40):
    env.step(action=[0., 0.])
env.render()