"""Download command for API documentation."""

import subprocess
import sys
from pathlib import Path


def download_api_docs(output_dir: str, methods: list, headless: bool, verbose: bool):
    """Download API documentation pages."""
    # For now, call the original script
    # TODO: Refactor the script's logic into this function
    script_path = Path(__file__).parent.parent / "download_api_docs.py"

    cmd = [sys.executable, str(script_path), "--output-dir", output_dir]

    if methods:
        for method in methods:
            cmd.extend(["--method", method])

    if headless:
        cmd.append("--headless")

    if verbose:
        print(f"Running: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=not verbose, text=True)

    if result.returncode != 0:
        if not verbose:
            print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    if not verbose:
        print(f"Downloaded documentation to {output_dir}")
