### PPO Hopper Config ###

env = {"name": "air_combat_mlagent", "time_scale": 12.0}

agent = {
    "name": "ppo",
    "network": "continuous_policy_value",
    "gamma": 0.99,
    "batch_size": 2048,
    "n_step": 128,
    "n_epoch": 3,
    "_lambda": 0.95,
    "epsilon_clip": 0.2,
    "vf_coef": 1.0,
    "ent_coef": 0.005,
    "lr_decay": True,
}

optim = {
    "name": "adam",
    "lr": 2.5e-4,
}

train = {
    "training": True,
    "load_path": None,
    "run_step": 10000000,
    "print_period": 5000,
    "save_period": 50000,
    "eval_iteration": 10,
    # distributed setting
    "distributed_batch_size": agent["batch_size"],
    "update_period": agent["n_step"],
    "num_workers": 8,
}
