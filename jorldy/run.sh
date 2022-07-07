# Examples: python main.py [run mode] --config [config path]
#python main.py --config config.dqn.cartpole
#python main.py --async --config config.ape_x.cartpole

# Examples: python main.py [run mode] --config [config path] --[optional parameter key] [parameter value]
#python main.py --config config.rainbow.atari --env.name breakout
#python main.py --sync --config config.ppo.cartpole --train.num_workers 8

python main.py --config config.ppo.hopper_mlagent