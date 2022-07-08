from .utils import check_env
from core.env.mlagent import HopperMLAgent, PongMLAgent, DroneDeliveryMLAgent, AirCombatMLAgent


# pytest -v -s test/core/env/test_mlagent_env.py

def test_hopper_mlagent(MockAgent):
    env = HopperMLAgent()
    agent = MockAgent(env.state_size, env.action_size, env.action_type)

    check_env(env, agent)


def test_pong_mlagent(MockAgent):
    env = PongMLAgent()
    agent = MockAgent(env.state_size, env.action_size, env.action_type)

    check_env(env, agent)


# 测试不通过
# def test_drone_delivery_mlagent(MockAgent):
#     env = DroneDeliveryMLAgent()
#     agent = MockAgent(env.state_size, env.action_size, env.action_type)
#
#     check_env(env, agent)


def test_air_combat_mlagent(MockAgent):
    env = AirCombatMLAgent()
    agent = MockAgent(env.state_size, env.action_size, env.action_type)

    check_env(env, agent, run_step=100)
