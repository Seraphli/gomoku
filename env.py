import random


class Env(object):
    def __init__(self, size=15, con=5):
        self.size = size
        self.con = con
        self.check_v = 2 ** self.con - 1

    def reset(self):
        self._size = self.size + self.con * 2 - 2
        self.state = [[0] * self._size for _ in range(2)]
        self.state_t = [[0] * self._size for _ in range(2)]
        self.state_0 = [[0] * (self._size * 2 - 1) for _ in range(2)]
        self.state_0_t = [[0] * (self._size * 2 - 1) for _ in range(2)]
        self._actions = set([(x, y) for x in range(self.size)
                             for y in range(self.size)])
        self.player = 0
        self.game_over = False

    def take_action(self, action):
        assert not self.game_over
        assert action in self._actions
        x, y = action
        x += self.con - 1
        y += self.con - 1
        p = self.player
        check_v = self.check_v
        _size = self._size
        self.player = 1 - self.player

        s = self.state[p]
        s[y] |= 1 << x
        s = s[y]
        self._actions.remove(action)
        if not self._actions:
            self.game_over = True
            return
        if s >= check_v:
            for _x in range(x - self.con + 1, x + 1):
                if check_v == check_v & (s >> _x):
                    self.game_over = True
                    return

        s_t = self.state_t[p]
        s_t[x] |= 1 << y
        s_t = s_t[x]
        if s_t >= check_v:
            for _y in range(y - self.con + 1, y + 1):
                if check_v == check_v & (s_t >> _y):
                    self.game_over = True
                    return

        _y = x + y
        _x = x if _y < _size else x - _y + _size - 1
        s_0 = self.state_0[p]
        s_0[_y] |= 1 << _x
        s_0 = s_0[_y]
        if s_0 >= check_v:
            for __x in range(_x - self.con + 1, _x + 1):
                if check_v == check_v & (s_0 >> __x):
                    self.game_over = True
                    return

        _y = _size - 1 - x + y
        _x = y if _y < _size else y - _y + _size - 1
        s_0_t = self.state_0_t[p]
        s_0_t[_y] |= 1 << _x
        s_0_t = s_0_t[_y]
        if s_0_t >= check_v:
            for __x in range(_x - self.con + 1, _x + 1):
                if check_v == check_v & (s_0_t >> __x):
                    self.game_over = True
                    return

    @property
    def actions(self):
        return tuple(self._actions)


if __name__ == '__main__':
    import time

    env = Env()
    st = time.time()
    step = 0
    for _ in range(10000):
        env.reset()
        while not env.game_over:
            step += 1
            env.take_action(random.choice(env.actions))
    print('total time', time.time() - st)
    print('avg step', step / 10000)
