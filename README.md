# Flappy Bird RL: Deep Q-Network (DQN) Implementation

A high-performance Reinforcement Learning (RL) agent capable of playing Flappy Bird using Deep Q-Learning. This project implements a Deep Q-Network (DQN) from scratch using PyTorch to navigate the classic game environment by learning optimal flight patterns through trial and error.

## Overview

The goal of this project was to apply Deep Reinforcement Learning techniques to a real-time environment. The agent interacts with a modified version of the Flappy Bird game, receiving rewards for passing pipes and penalties for collisions. Over thousands of episodes, the agent learns to maximize its expected future reward, eventually achieving human-like or superhuman performance.

## Key Features

**DQN Architecture**: Implements a Convolutional Neural Network (CNN) or Deep Neural Network (DNN) to approximate the Q-value function.

**Experience Replay**: Utilizes a replay buffer to store past transitions, breaking the correlation between consecutive samples and stabilizing the learning process.

**Target Network**: Employs a separate target network that is updated periodically to provide stable Q-value targets during training.

**$\epsilon$-Greedy Exploration**: A decaying exploration strategy to balance exploring new actions and exploiting known high-reward paths.

**Custom Environment Wrapper**: A specialized interface that bridges the Pygame-based game logic with the RL training loop, handling state preprocessing and reward shaping.

## Tech Stack

**Language**: Python 3

**Deep Learning Framework**: PyTorch

**Game Engine**: Pygame

**Core Libraries**: NumPy (Numerical processing), OpenCV (Image preprocessing, if applicable)

## Project Structure

agent.py: Defines the DQN model architecture and the RL agent's logic (choosing actions, learning).

environment.py: Wraps the game logic into an OpenAI Gym-like interface for the agent.

flappy.py: The core game engine implementation.

train.py: The main entry point for training the model.

test.py: Script to load pre-trained weights (.pth files) and evaluate agent performance.

flappy_bird_dqn_best.pth: Saved weights of the most successful training iteration.

## Installation & Setup
1. Clone the repository:
```bash
git clone https://github.com/anirudh242/flappybird-dqn.git
cd flappybird-dqn
```

2. Install dependencies:
```bash
pip install torch pygame numpy opencv-python
```

## Usage

### Training the Agent

To start the training process from scratch:
```bash
python train.py
```
### Testing/Evaluating the Agent

To run the game using the pre-trained "best" model weights:
```bash
python test.py
```

## Methodology

The agent's training involves the following steps:

State Representation: The environment provides the current game state (either raw pixels or coordinate-based distances).

Reward Function:

$+0.1$ for every frame survived.

$+1.0$ for successfully passing a pipe.

$-1.0$ for crashing into a pipe or the ground.

Optimisation: The model is optimised using the Huber loss (or MSE) between the predicted Q-values and the Target Q-values calculated via the Bellman Equation.

*Developed as a project to demonstrate proficiency in Reinforcement Learning and Neural Network optimisation.*
