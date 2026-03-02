# Kotlin IR Fuzz Playground

Small personal playground for experimenting with fuzzing Kotlin compiler

## What it does

- Generates many small random programs (functions, loops, inline functions).
- Compiles them with `kotlinc`.
- If the compiler crashes or prints an internal error, the input is saved to `crashes/` for further analysis.

## How to run

```bash
python3 src/fuzzer.py
```

## Requirements

- Python 3.10+
- Kotlin compiler `(kotlinc)` available in PATH
