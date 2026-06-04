"""
Training entry for the LSTM-SAC racing controller.

This partial open-source release keeps only the high-level training pipeline used in
the paper. The CarSim environment, LSTM feature extractor, vehicle interface, and
custom callback implementations are intentionally withheld and listed in the
README TODO section.
"""

import datetime
import os
import sys
from typing import Any

import gymnasium as gym
import torch
from stable_baselines3 import SAC
from stable_baselines3.common.callbacks import CallbackList, CheckpointCallback

sys.path.append(".")

# TODO(open-source): provide the environment registration module.
# import sim_env

# TODO(open-source): provide the LSTM feature extractor implementation.
# from custom_policy.sac_lstm_mlp_policy import LSTMExtractor

# TODO(open-source): provide the custom TensorBoard callback implementation.
# from sb_call_back.custom_sb3_callback import TensorboardExtraDataCallback

# TODO(open-source): provide command-line argument helper or replace it with argparse.
# from utils.arg_builder import get_train_args


def main() -> None:
    """Train the LSTM-SAC controller in the CarSim racing environment."""
    train_args: Any = get_train_args()
    print(train_args.model_dump_json(indent=2))

    task_name: str = "racing"
    current_time_str: str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir: str = os.path.join(train_args.log_dir, f"sac_{task_name}_{current_time_str}")

    env: gym.Env = gym.make(
        "env_carsim_time_related_v4",
        carsim_db_dir=train_args.carsim_db_dir,
    )

    device: str = "cuda" if torch.cuda.is_available() else "cpu"

    if train_args.is_new:
        policy_kwargs = {
            "features_extractor_class": LSTMExtractor,
            "features_extractor_kwargs": {},
            "net_arch": dict(pi=[64, 64], qf=[64, 64]),
        }

        model: SAC = SAC(
            policy="MlpPolicy",
            env=env,
            learning_rate=train_args.learning_rate,
            buffer_size=train_args.buffer_size,
            learning_starts=train_args.learning_starts,
            batch_size=train_args.batch_size,
            tau=0.005,
            gamma=0.99,
            ent_coef=0.1,
            verbose=1,
            device=device,
            tensorboard_log=log_dir,
            policy_kwargs=policy_kwargs,
        )
    else:
        print(f"Load model from {train_args.model_path}")
        model = SAC.load(str(train_args.model_path), env=env)
        model.tensorboard_log = log_dir

    print(model.policy)

    checkpoint_callback: CheckpointCallback = CheckpointCallback(
        save_freq=train_args.save_freq,
        save_path=log_dir,
        name_prefix=f"sac_{task_name}_{current_time_str}",
        verbose=1,
    )

    extra_data_callback: TensorboardExtraDataCallback = TensorboardExtraDataCallback(
        verbose=1,
        log_every_n_episodes=100,
    )

    callback_list: CallbackList = CallbackList([checkpoint_callback, extra_data_callback])

    model.learn(
        total_timesteps=train_args.total_timesteps,
        callback=callback_list,
        progress_bar=True,
    )


if __name__ == "__main__":
    main()
