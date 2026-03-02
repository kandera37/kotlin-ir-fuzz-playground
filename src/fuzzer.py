import random
import string
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

CRASH_DIR = Path("crashes")
KOTLINC_CMD: list[str] = ["kotlinc"]


def random_identifier(prefix: str = "x") -> str:
    """Generate a simple name for variables/function."""
    suffix = "".join(random.choices(string.ascii_lowercase, k=5))
    return f"{prefix}_{suffix}"

def generate_kotlin_program() -> str:
    """
    Generate a small Kotlin program.
    For now, it produces very simple constructions.
    Later I will add more inline functions and patterns.
    """
    func_name = random_identifier("foo")
    arg_name = random_identifier("arg")

    bodies = [
        # simple arithmetic
        (
            f"      val res = {random.randint(1, 10)} + {random.randint(1, 10)}\n"
            f"      println(res)\n"
        ),
        # simple loop
        (
            f"      for (i in 0..{random.randint(1, 5)}) {{\n"
            f"          println(i + {random.randint(0, 3)})\n"
            f"      }}\n"
        ),
        # inline call
        (
            f"inline fun inlineAdd(a: Int, b: Int): Int = a + b\n\n"
            f"fun {func_name}({arg_name}: Int) {{\n"
            f"      println(inlineAdd({arg_name}, {random.randint(1,5)}))\n"
            "}\n"
        ),
    ]

    if random.random() < 0.5:
        body = random.choice(bodies[:-1])
        code = "fun main()  {\n" + body + "}\n"
    else:
        code = bodies[-1]

    return code

def compile_kotlin_source(source_code: str) -> tuple[int, str, str]:
    """
    Compile source and return (returncode, stdout, stderr).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = Path(tmpdir) / "Sample.kt"
        out_path = Path(tmpdir) / "out.jar"

        src_path.write_text(source_code, encoding="utf-8")
        try:
            proc = subprocess.run(
                KOTLINC_CMD + [str(src_path), "-d", str(out_path)],
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            raise SystemExit(
                f"Error: '{KOTLINC_CMD[0]}' not found in PATH. "
                "Install Kotlin compiler or pass --kotlinc /path/to/kotlinc."
            )

        return proc.returncode, proc.stdout, proc.stderr

def is_interesting_failure(stderr: str) -> bool:
    """Simple heuristic: we treat internal compiler errors an interesting failures."""
    lowered = stderr.lower()
    return (
        "internal error" in lowered
        or "exception" in lowered
        or "bug" in lowered
    )

def save_crash_case(source_code: str, stdout: str, stderr: str) -> None:
    """Save a test case that crashes complier (or looks suspicious). """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    base = CRASH_DIR / f"crash_{timestamp}"

    (base.with_suffix(".kt")).write_text(source_code, encoding="utf-8")
    (base.with_suffix(".log")).write_text(
        f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}\n",
        encoding="utf-8",
    )
    print(f"[!] Saved crash case to {base}.kt")

def run_fuzzer(iterations: int, kotlinc_cmd: str, output_dir: Path) -> None:
    """
    Run fuzzing loop for given number of iterations.
    """
    global KOTLINC_CMD, CRASH_DIR

    KOTLINC_CMD = [kotlinc_cmd]
    CRASH_DIR = output_dir
    CRASH_DIR.mkdir(exist_ok=True)

    crashes = 0
    for i in range(1, iterations + 1):
        program = generate_kotlin_program()
        code, out, err = compile_kotlin_source(program)

        if code != 0 and is_interesting_failure(err):
            crashes += 1
            save_crash_case(program, out, err)

        if i % 10 == 0:
            print(f"[+] Iteration {i}: crashes so far {crashes}")

    print(f"Done. Total iterations: {iterations}, crashes: {crashes}")