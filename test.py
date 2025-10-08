import torch
import os
import time
from environment import FlappyEnv
from agent import DQNAgent

if __name__ == '__main__':
    env = FlappyEnv()
    state_size = env.state_space_size
    action_size = env.action_space_size
    agent = DQNAgent(state_size, action_size)

    model_path = 'flappy_bird_dqn_best.pth'
    if os.path.exists(model_path):
        checkpoint = torch.load(model_path)
        agent.policy_net.load_state_dict(checkpoint['model_state_dict'])
        best_score = checkpoint['best_score']
        agent.policy_net.eval() 
        
        print(f"Loaded saved model from '{model_path}'. Best recorded score: {best_score}.")
    else:
        print(f"No saved model found at '{model_path}'. Please run train.py to train a model first.")
        exit() 

    agent.epsilon = 0.0

    state = env.reset()
    done = False
    
    print("Starting game...")

    while not done:
        env.render()
        
        action = agent.get_action(state)
        
        next_state, reward, done, score = env.step(action)
        
        state = next_state
        
        time.sleep(1/60) 

    print(f"\nGame Over! Final Score: {score}")