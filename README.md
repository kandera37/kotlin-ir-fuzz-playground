# Kotlin IR Fuzz Playground

## Why I built this

I wanted to experiment with compiler fuzzing in a small and simple project.
This playground generates random Kotlin programs, compiles them with `kotlinc`, and saves interesting crash cases for later analysis

## What it does

- Generates many small random programs (functions, loops, inline functions).
- Compiles them with `kotlinc`.
- If the compiler crashes or prints an internal error, the input is saved to `crashes/` for further analysis.

## How to run

```bash
python3 src/main.py --iterations 200
```

## CLI options

- `--iterations` — number of fuzzing iterations
- `--kotlinc` — Kotlin compiler executable or path
- `--output-dir` — directory for saved crash cases

## Requirements

- Python 3.10+
- Kotlin compiler `(kotlinc)` available in PATH
