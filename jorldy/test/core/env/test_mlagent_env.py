from test.core.env.utils import check_env
from core.env.mlagent import HopperMLAgent, PongMLAgent, DroneDeliveryMLAgent, AirCombatMLAgent


def test_hopper_mlagent(MockAgent):
    env = HopperMLAgent()
    agent = MockAgent(env.state_size, env.action_size, env.action_type)

    check_env(env, agent)


def test_pong_mlagent(MockAgent):
    env = PongMLAgent()
    agent = MockAgent(env.state_size, env.action_size, env.action_type)

    check_env(env, agent)


def test_drone_delivery_mlagent(MockAgent):
    env = DroneDeliveryMLAgent()
    agent = MockAgent(env.state_size, env.action_size, env.action_type)

    check_env(env, agent)


def test_air_combat_mlagent(MockAgent):
    env = AirCombatMLAgent()
    agent = MockAgent(env.state_size, env.action_size, env.action_type)

    check_env(env, agent)


test_air_combat_mlagent()
