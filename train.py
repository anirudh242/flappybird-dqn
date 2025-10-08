from environment import FlappyEnv
from agent import DQNAgent
import torch
import os

if __name__ == '__main__':
    env = FlappyEnv()
    state_size = env.state_space_size
    action_size = env.action_space_size
    agent = DQNAgent(state_size, action_size)

    episodes = 1000
    batch_size = 64
    
    TARGET_UPDATE_FREQUENCY = 10 

    model_path = 'flappy_bird_dqn_best.pth'
    best_score = -1

    if os.path.exists(model_path):
        checkpoint = torch.load(model_path)
        agent.policy_net.load_state_dict(checkpoint['model_state_dict'])
        agent.target_net.load_state_dict(checkpoint['model_state_dict'])
        best_score = checkpoint['best_score']
        agent.policy_net.eval()
        agent.epsilon = 0.1
        print(f"Loaded saved model. Best score: {best_score}.")
    else:
        print("Starting training from scratch.")

    for e in range(episodes):
        state = env.reset()

        for time in range(5000):
            action = agent.get_action(state)
            next_state, reward, done, score = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            
            if done:
                print(f"Episode: {e+1}/{episodes}, Score: {score}, Epsilon: {agent.epsilon:.2f}")
                
                if agent.epsilon > agent.epsilon_min:
                    agent.epsilon *= agent.epsilon_decay
                
                if score > best_score:
                    best_score = score
                    torch.save({
                        'model_state_dict': agent.policy_net.state_dict(),
                        'best_score': best_score
                    }, model_path)
                    print(f"New best score! Model saved.")
                break
            
            agent.replay(batch_size)
        
        if e % TARGET_UPDATE_FREQUENCY == 0:
            agent.update_target_net()
            print(f"--- Target network updated at episode {e+1} ---")
