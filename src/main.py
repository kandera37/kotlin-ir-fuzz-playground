import argparse
from pathlib import Path
from fuzzer import run_fuzzer

def main() -> None:
    parser = argparse.ArgumentParser(description="Small personal playground for experimenting with fuzzing Kotlin compiler.")
    parser.add_argument(
        "--iterations",
        type=int,
        default=200,
        help="Number of iterations to run the fuzzing process.",
    )
    parser.add_argument(
        "--kotlinc",
        default="kotlinc",
        help="Kotlin compiler executable.",
    )
    parser.add_argument(
        "--output-dir",
        default="crashes/",
        help="Output directory to save generated files.",
    )

    args = parser.parse_args()

    run_fuzzer(
        iterations=args.iterations,
        kotlinc_cmd=args.kotlinc,
        output_dir=Path(args.output_dir),
    )
if __name__ == "__main__":
    main()