from env import Env
import random

env = Env()
for dx in range(-1, 2):
    for dy in range(-1, 2):
        if dx == 0 and dy == 0:
            continue
        for x in range(0, 15):
            for y in range(0, 15):
                if dx < 0 and x < 5:
                    continue
                if dx > 0 and x > 10:
                    continue
                if dy < 0 and y < 5:
                    continue
                if dy > 0 and y > 10:
                    continue
                for m in range(100):
                    env.reset()
                    actions = []
                    for i in range(5):
                        actions.append((x + dx * i, y + dy * i))
                    for i in range(4):
                        action = random.choice(env.actions)
                        while action in actions:
                            action = random.choice(env.actions)
                        env.take_action(actions[i])
                        assert not env.game_over
                        env.take_action(action)
                        assert not env.game_over

                    env.take_action(actions[4])
                    assert env.game_over
