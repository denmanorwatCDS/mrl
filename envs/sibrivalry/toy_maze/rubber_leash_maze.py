from math import sqrt
from envs.sibrivalry.toy_maze.mazes import Maze
from envs.sibrivalry.toy_maze.maze_maps.maze_parser import get_maze
from envs.sibrivalry.toy_maze import MultiGoalPointMaze2D, PointMaze2D, Env
import numpy as np
import gym

class RubberLeashMaze(Maze):
    def __init__(self, *segment_dicts, action_range=0.95, labyrinth_side=10., leash_attachment_point = (-0.5, -0.5),
                 goal_squares=None, start_squares=None, elasticity_coef=0.8):
        super().__init__(*segment_dicts, goal_squares=goal_squares, start_squares=start_squares)
        self.max_elasticity = action_range*elasticity_coef
        self.leash_attachment_point = leash_attachment_point
        self.max_distance = sqrt(2)*labyrinth_side
        self.action_range = action_range

    def move(self, coord_start, coord_delta, depth=None, apply_elasticity=False):
        if apply_elasticity:
            leash_x, leash_y = self.leash_attachment_point
            agent_x, agent_y = coord_start
            pull_vec_x, pull_vec_y = leash_x - agent_x, leash_y - agent_y

            force_coef = 1/self.max_distance*self.max_elasticity
            pull_force_x, pull_force_y = pull_vec_x*force_coef, pull_vec_y*force_coef

            total_delta_x, total_delta_y = coord_delta[0] + pull_force_x, coord_delta[1] + pull_force_y
            coord_delta = (total_delta_x, total_delta_y)
        return super().move(coord_start, coord_delta, depth)

    
    
class CustomEnv(Env):
    def __init__(self, elasticity_coef, n=None, maze_type="10x10", use_antigoal=True, ddiff=False, ignore_reset_start=False):
        self.n = n

        self.maze_type = maze_type
        self._ignore_reset_start = bool(ignore_reset_start)

        self.use_antigoal = bool(use_antigoal)
        self.ddiff = bool(ddiff)

        self._state = dict(s0=None, prev_state=None, state=None, goal=None, n=None, done=None, d_goal_0=None, d_antigoal_0=None)

        self.dist_threshold = 0.15

        maze_segments, maze_size, self.action_range_scalar, goal_squares = get_maze(maze_type)
        self.maze_env = RubberLeashMaze(*maze_segments, action_range=self.action_range, labyrinth_side=maze_size, 
                                        elasticity_coef=elasticity_coef, goal_squares=goal_squares)
        self.maze_type = self.maze_type+"_square"

        self.reset()

    @property
    def maze(self):
        return self.maze_env
    
    @property
    def action_range(self):
        return self.action_range_scalar
    

class CustomMultiGoalPointMaze2D(MultiGoalPointMaze2D):
    def __init__(self, test=False, maze_type="10x10", elasticity_coef=0.8):
        super(PointMaze2D).__init__()
        self._env = CustomEnv(n=50, elasticity_coef=elasticity_coef,
                              maze_type=maze_type, use_antigoal=False, ddiff=False, ignore_reset_start=True)
        #Env(n=50, maze_type='multigoal_square_large', use_antigoal=False, ddiff=False, ignore_reset_start=True)
        self.maze = self._env.maze
        self.dist_threshold = 0.15

        self.action_space = gym.spaces.Box(-0.95, 0.95, (2, ))
        observation_space = gym.spaces.Box(-np.inf, np.inf, (2, ))
        goal_space = gym.spaces.Box(-np.inf, np.inf, (2, ))
        self.observation_space = gym.spaces.Dict({
            'observation': observation_space,
            'desired_goal': goal_space,
            'achieved_goal': goal_space
        })

        self.s_xy = np.array(self.maze.sample_start())
        self.g_xy = np.array(self.maze.sample_goal(min_wall_dist=0.025 + self.dist_threshold))
        self.max_steps = 50
        self.num_steps = 0
        self.test = test
        self.background = None
        self.goal_idx = 0

    def step(self, action):
        print(self.s_xy)
        try:
            s_xy = np.array(self.maze.move(tuple(self.s_xy), tuple(action), apply_elasticity=True))
        except:
            print('failed to move', tuple(self.s_xy), tuple(action))
            raise

        self.s_xy = s_xy
        reward = self.compute_reward(s_xy, self.g_xy, None)
        info = {}
        self.num_steps += 1

        if self.test:
            done = np.allclose(0., reward)
            # info['is_success'] = done
            info = self.add_pertask_success(info, goal_idx=self.goal_idx)
        else:
            done = False
            # info['is_success'] = np.allclose(0., reward)
            info = self.add_pertask_success(info, goal_idx=None)

        if self.num_steps >= self.max_steps and not done:
            done = True
            info['TimeLimit.truncated'] = True

        obs = {
            'observation': s_xy,
            'achieved_goal': s_xy,
            'desired_goal': self.g_xy,
        }

        return obs, reward, done, info