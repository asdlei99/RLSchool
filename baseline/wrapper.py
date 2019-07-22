from rlschool.liftsim.environment.env import LiftSim
from baseline.wrapper_utils import obs_dim, act_dim, mansion_state_preprocessing
from baseline.wrapper_utils import action_idx_to_action, action_to_action_idx


class Wrapper(LiftSim):
    def __init__(self, env):
        self.env = env
        self._mansion = env._mansion
        self.mansion_attr = self._mansion.attribute
        self.elevator_num = self.mansion_attr.ElevatorNumber
        self.observation_space = obs_dim(self.mansion_attr)
        self.action_space = act_dim(self.mansion_attr)
        self.viewer = env.viewer

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError("attempted to get missing private attribute '{}'".format(name))
        return getattr(self.env, name)

    def seed(self, seed=None):
        return self.env.seed(seed)

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        return self.env.reset()

    def render(self):
        return self.env.render()

    def close(self):
        return self.env.close()

    
class RewardWrapper(Wrapper):
    pass

class ActionWrapper(Wrapper):
    def reset(self):
        return self.env.reset()
    
    def step(self, action):
        return self.env.step([self.action(a, self.action_space) for a in action])

    def action(self, action, action_space):
        return action_idx_to_action(action, action_space)

class ObservationWrapper(Wrapper):
    def reset(self):
        self.env.reset()
        return self.observation(self._mansion.state)

    def step(self, action):
        observation, reward, done, info = self.env.step(action)
        return (self.observation(observation), reward, done, info)

    def observation(self, observation):
        return mansion_state_preprocessing(observation) 

    @property
    def state(self):
        return self.observation(self._mansion.state)
