# airodor-wifi-api

Python API for the [Airodor WiFi module](https://www.limot.de/) from Limot.

## Reverse Engineered API

General address to contact:

```
http://<ip-address>/msg?Function=<action><group>[<mode>]
```

### Actions

| Action | Description       |
| ------ | ----------------- |
| `R`    | Read mode         |
| `W`    | Set mode          |
| `T`    | Read off-timer    |
| `S`    | Set off-timer     |

### Groups

| Group | Description     |
| ----- | --------------- |
| `A`   | Vent group A    |
| `B`   | Vent group B    |

### Ventilation Modes

#### Setting

| Value | Mode                      |
| ----- | ------------------------- |
| 0     | Off                       |
| 1     | Min – alternating         |
| 2     | Med – alternating         |
| 4     | Max – alternating         |
| 8     | Med – permanent one dir   |
| 16    | Max – permanent one dir   |
| 32    | Med – permanent inside    |
| 64    | Max – permanent inside    |

#### Reading

| Value | Mode                                   |
| ----- | -------------------------------------- |
| 0     | Off                                    |
| 1     | Min – alternating                      |
| 2     | Med – alternating                      |
| 3     | Med – alternating (forced)             |
| 6     | Max – alternating                      |
| 10    | Med – permanent one dir                |
| 18    | Max – permanent one dir                |
| 34    | Med – permanent inside                 |
| 66    | Max – permanent inside                 |
| 128   | Off – with timer activated             |

### Timer

Timer values: `0` = off, `1..12` = hours.

### Answers

| Request | Answer format   | Example  |
| ------- | --------------- | -------- |
| `R`     | `R<group><mode>` | `RA2`   |
| `W`     | `M<group>OK`     | `MAOK`  |
| `T`     | `T<group><val>`  | `TA3`   |
| `S`     | `S<group>OK`     | `SAOK`  |

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Lint & format
uv run ruff check .
uv run ruff format .

# Type check
uv run ty check

# Run all checks (lint, format, type check, tests)
uvx prek --all-files
```

## License

[MIT](LICENSE)
