#!/usr/bin/env python3
"""
Test runner for Cyber-Researcher test suite.

This script provides various options for running tests with proper
configuration and reporting.
"""

import sys
import subprocess
import argparse
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def run_command(cmd, description):
    """Run a command and handle output."""
    print(f"\n{'=' * 60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'=' * 60}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)

        if result.stdout:
            print("STDOUT:")
            print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        if result.returncode != 0:
            print(f"❌ Command failed with return code {result.returncode}")
            return False
        else:
            print("✅ Command completed successfully")
            return True

    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run Cyber-Researcher tests")

    parser.add_argument(
        "--type", choices=["unit", "integration", "all"], default="all", help="Type of tests to run"
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Run tests in verbose mode")

    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage reporting")

    parser.add_argument("--file", help="Run tests from specific file")

    parser.add_argument("--function", help="Run specific test function")

    parser.add_argument(
        "--install-deps", action="store_true", help="Install test dependencies before running"
    )

    parser.add_argument("--lint", action="store_true", help="Run linting checks")

    parser.add_argument("--format", action="store_true", help="Run code formatting")

    parser.add_argument("--typecheck", action="store_true", help="Run type checking")

    args = parser.parse_args()

    print("🚀 Cyber-Researcher Test Runner")
    print("=" * 60)

    # Install dependencies if requested
    if args.install_deps:
        print("Installing test dependencies...")
        if not run_command(["uv", "sync", "--dev"], "Installing dependencies"):
            return 1

    # Run code formatting if requested
    if args.format:
        print("Running code formatting...")
        if not run_command(["uv", "run", "black", "."], "Code formatting"):
            return 1

    # Run linting if requested
    if args.lint:
        print("Running linting checks...")
        if not run_command(["uv", "run", "ruff", "check", "."], "Linting"):
            return 1

    # Run type checking if requested
    if args.typecheck:
        print("Running type checking...")
        if not run_command(["uv", "run", "mypy", "src/"], "Type checking"):
            return 1

    # Build pytest command
    pytest_cmd = ["uv", "run", "pytest"]

    # Add verbosity
    if args.verbose:
        pytest_cmd.append("-v")

    # Add coverage if requested
    if args.coverage:
        pytest_cmd.extend(["--cov=src/cyber_storm", "--cov-report=html", "--cov-report=term"])

    # Add specific file or function
    if args.file:
        if args.function:
            pytest_cmd.append(f"tests/{args.file}::{args.function}")
        else:
            pytest_cmd.append(f"tests/{args.file}")
    elif args.function:
        pytest_cmd.append(f"-k {args.function}")
    else:
        # Add test type filter
        if args.type == "unit":
            pytest_cmd.extend(["-m", "unit"])
        elif args.type == "integration":
            pytest_cmd.extend(["-m", "integration"])
        else:
            pytest_cmd.append("tests/")

    # Run the tests
    description = f"Running {args.type} tests"
    if args.file:
        description += f" from {args.file}"
    if args.function:
        description += f" function {args.function}"

    success = run_command(pytest_cmd, description)

    if success:
        print("\n🎉 All tests completed successfully!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
