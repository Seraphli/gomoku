Simulate the game Gomoku on a board.

The default implement is in `env.py`.

The default board size is 15. The max support size is 64.

10000 games take about 8 seconds.

The average step is used to verify the environment, and the number is supposed to be about 109.

There is another implement in `env_rec.py`. I keep this here because I think the way to check if the game is end is interesting, and also it supports the board size larger than 64. But it is slower than `env.py`, about 16 seconds for 10000 games.

`verify.py` is used to verify the environment.