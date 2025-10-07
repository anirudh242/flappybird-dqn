import numpy as np
from flappy import FlappyBirdGame

class FlappyEnv:
    def __init__(self):
        self.game = FlappyBirdGame()
        self.action_space_size = 2 # 0 = nothing; 1 = flap
        self.state_space_size = 4
        
    def _get_state(self):
        bird = self.game.bird

        next_pipe = None
        min_dist = float('inf')
        for pipe in self.game.pipe_group.sprites():
            if pipe.rect.right > bird.rect.left:
                dist = pipe.rect.centerx - bird.rect.centerx
                if dist < min_dist:
                    min_dist = dist
                    next_pipe = pipe
        
        if next_pipe:
            pipes = self.game.pipe_group.sprites()
            bottom_pipe = next((p for p in pipes if p.rect.bottom == next_pipe.rect.bottom), None)
            top_pipe = next((p for p in pipes if p.rect.top == next_pipe.rect.top), None)

            if bottom_pipe and top_pipe:
                gap_center_y = (bottom_pipe.rect.top + top_pipe.rect.bottom) / 2
                dist_y = gap_center_y - bird.rect.centery
            else:
                dist_y = self.game.screen.get_height() / 2 - bird.rect.centery

            dist_x = next_pipe.rect.centerx - bird.rect.centerx
        else:
            dist_x = self.game.screen.get_width()
            dist_y = self.game.screen.get_height() / 2 - bird.rect.centery
        
        state = np.array([bird.rect.y, bird.speed, dist_x, dist_y])
        return state
    
    def _calculate_reward(self, done, score_before, score_after):
        if done: # dead
            return -100
        if score_after > score_before:
            return 1.0 # passing pipe
        return 0.1 # staying alive
    
    def step(self, action):
        score_before = self.game.score
        self.game.step(action)
        score_after = self.game.score
        done = self.game.game_over
        reward = self._calculate_reward(done, score_before, score_after)
        new_state = self._get_state()
        return new_state, reward, done, score_after
    
    def reset(self):
        self.game.reset()
        return self._get_state()
    
    def render(self):
        self.game.render()

if __name__ == '__main__':
    env = FlappyEnv()

    for episode in range(5):
        state = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            action = np.random.randint(0, env.action_space_size)
            new_state, reward, done, score = env.step(action)

            env.render()
            
            total_reward += reward

            if done:
                print(f'Episode {episode + 1}: Score={score}, Total Reward={total_reward:.2f}')

    