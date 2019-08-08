import numpy as np
import random


class Env(object):
    def __init__(self, size=15, con=5):
        self.size = size
        self.con = con

    def reset(self):
        self.state = np.zeros((self.size + self.con * 2 - 2,
                               self.size + self.con * 2 - 2, 2), dtype=np.bool)
        self._actions = set([(x, y) for x in range(self.size)
                             for y in range(self.size)])
        self.player = 0
        self.game_over = False

    def check(self, s, x, y, dx, dy, c):
        if s[x, y]:
            if c == 1:
                return True
            elif x + dx * (c - 1) < self.con * 2 - 1 and y + dy * (
                    c - 1) < self.con * 2 - 1 and c > 1:
                return self.check(s, x + dx, y + dy, dx, dy, c - 1)
            else:
                return False
        else:
            if x + dx < self.con and y + dy < self.con:
                return self.check(s, x + dx, y + dy, dx, dy, self.con)
            else:
                return False

    def take_action(self, action):
        assert not self.game_over
        assert action in self._actions
        x, y = action
        x += self.con - 1
        y += self.con - 1
        self.state[x, y, self.player] = True
        s = self.state[x - self.con + 1:x + self.con,
            y - self.con + 1:y + self.con, self.player]
        self.player = 1 - self.player
        self._actions.remove(action)
        if not self._actions:
            self.game_over = True
            return
        self.game_over = self.check(
            s, 0, self.con - 1, 1, 0, self.con) or self.check(
            s, self.con - 1, 0, 0, 1, self.con) or self.check(
            s, 0, 0, 1, 1, self.con) or self.check(
            s[::-1, :], 0, 0, 1, 1, self.con)

    @property
    def actions(self):
        return tuple(self._actions)

    def __repr__(self):
        return str(self.state[self.con - 1:self.size + self.con - 1,
                   self.con - 1:self.size + self.con - 1, 0] +
                   2 * self.state[self.con - 1:self.size + self.con - 1,
                       self.con - 1:self.size + self.con - 1, 1])


if __name__ == '__main__':
    import time

    env = Env()
    step = 0
    st = time.time()
    for _ in range(10000):
        env.reset()
        while not env.game_over:
            step += 1
            env.take_action(random.choice(env.actions))
    print('total time', time.time() - st)
    print('avg step', step / 10000)
