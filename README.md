# Filipino-Mahjong
Filipino Mahjong with family rules

## How to run

Requires Python 3.10+. No dependencies.

```bash
python3 main.py
```

Starts a game with 1 human player and 3 CPU opponents.

### Controls

When it's your turn, you'll be prompted to discard a tile using suit code + value:

| Suit | Code |
|------|------|
| Balls | `b` |
| Sticks | `s` |
| Characters | `c` |

Example: `b 5` discards the 5 of Balls.

If a discard is available to chow, you'll be asked `bunot` or `chow`. When claiming out-of-turn (pong, kong, or mahjong), you'll be prompted after each discard.
