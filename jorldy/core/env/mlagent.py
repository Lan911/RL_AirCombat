from mlagents_envs.environment import UnityEnvironment, ActionTuple
from mlagents_envs.side_channel.engine_configuration_channel import (
    EngineConfigurationChannel,
)

import numpy as np
import platform, subprocess
from .base import BaseEnv


def match_build():
    os = platform.system()
    return {"Windows": "Windows", "Darwin": "Mac", "Linux": "Linux"}[os]


class _MLAgent(BaseEnv):
    """MLAgent environment.

    Args:
        env_name (str): name of environment in ML-Agents.
        render (bool): parameter that determine whether to render.
        time_scale (bool): parameter that determine frame time_scale.
    """

    def __init__(self, env_name, render=False, time_scale=12.0, id=None, **kwargs):
        # env_path = f"./core/env/mlagents/{env_name}/{match_build()}/{env_name}"
        env_path = f"../../mlagents-env/{env_name}/{match_build()}/{env_name}"
        print("env_path:", env_path)
        id = (
            np.random.randint(65534 - UnityEnvironment.BASE_ENVIRONMENT_PORT)
            if id is None
            else id
        )

        graphic_available = False if subprocess.getoutput("which Xorg") == "" else True
        no_graphics = not (render and graphic_available)

        engine_configuration_channel = EngineConfigurationChannel()
        self.env = UnityEnvironment(
            file_name=env_path,
            side_channels=[engine_configuration_channel],
            worker_id=id,
            no_graphics=no_graphics,
        )

        self.env.reset()

        self.score = 0

        self.behavior_name = list(self.env.behavior_specs.keys())[0]
        self.spec = self.env.behavior_specs[self.behavior_name]

        self.is_continuous_action = self.spec.action_spec.is_continuous()

        engine_configuration_channel.set_configuration_parameters(time_scale=time_scale)
        dec, term = self.env.get_steps(self.behavior_name)

    def reset(self):
        self.score = 0
        self.env.reset()
        dec, term = self.env.get_steps(self.behavior_name)
        state = self.state_processing(dec.obs)

        return state

    def step(self, action):
        action_tuple = ActionTuple()

        if self.is_continuous_action:
            action_tuple.add_continuous(action)
        else:
            action_tuple.add_discrete(action)

        self.env.set_actions(self.behavior_name, action_tuple)
        self.env.step()

        dec, term = self.env.get_steps(self.behavior_name)
        done = len(term.agent_id) > 0
        reward = term.reward if done else dec.reward
        next_state = (
            self.state_processing(term.obs) if done else self.state_processing(dec.obs)
        )

        self.score += reward[0]

        reward, done = map(lambda x: np.expand_dims(x, 0), [reward, [done]])

        return (next_state, reward, done)

    def state_processing(self, obs):
        return obs[0]

    def close(self):
        self.env.close()


class HopperMLAgent(_MLAgent):
    def __init__(self, **kwargs):
        env_name = "Hopper"
        super(HopperMLAgent, self).__init__(env_name, **kwargs)

        self.state_size = 19 * 4
        self.action_size = 3
        self.action_type = "continuous"


class PongMLAgent(_MLAgent):
    def __init__(self, **kwargs):
        env_name = "Pong"
        super(PongMLAgent, self).__init__(env_name, **kwargs)

        self.state_size = 8 * 1
        self.action_size = 3
        self.action_type = "discrete"


class DroneDeliveryMLAgent(_MLAgent):
    def __init__(self, **kwargs):
        env_name = "DroneDelivery"
        super(DroneDeliveryMLAgent, self).__init__(env_name, **kwargs)

        self.state_size = [[15, 36, 64], 95]
        self.action_size = 3
        self.action_type = "continuous"


class AirCombatMLAgent(_MLAgent):
    def __init__(self, **kwargs):
        env_name = "AirCombat"
        super(AirCombatMLAgent, self).__init__(env_name, **kwargs)

        self.state_size = 65
        self.action_size = 6
        self.action_type = "continuous"

    def state_processing(self, obs):
        vis_obs = []

        for _obs in obs:
            if len(_obs.shape) == 2:  # vector observation
                vec_obs = _obs
            else:  # visual observation
                vis_obs.append(_obs)

        # vis obs processing
        vis_obs = np.concatenate(vis_obs, axis=-1)
        vis_obs = np.transpose(vis_obs, (0, 3, 1, 2))
        vis_obs = (vis_obs * 255).astype(np.uint8)

        return [vis_obs, vec_obs]
