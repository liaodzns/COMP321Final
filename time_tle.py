#!/usr/bin/env python3
"""
Script to run all test inputs through the inefficient tle.py solution
and measure the runtime for each test case.
"""

import os
import time
import subprocess
import sys
from pathlib import Path

def run_test(input_file, tle_script):
    """
    Run a single test case through the TLE script and measure runtime.
    Returns (runtime_seconds, output, success)
    """
    try:
        with open(input_file, 'r') as f:
            input_data = f.read()
        
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, tle_script],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        end_time = time.time()
        
        runtime = end_time - start_time
        return runtime, result.stdout.strip(), True, None
    
    except subprocess.TimeoutExpired:
        return 30.0, "", False, "TIMEOUT"
    except Exception as e:
        return 0.0, "", False, str(e)

def check_answer(output, answer_file):
    """
    Check if the output matches the expected answer.
    """
    try:
        with open(answer_file, 'r') as f:
            expected = f.read().strip()
        return output == expected
    except:
        return None

def main():
    # Paths
    project_root = Path(__file__).parent
    data_dir = project_root / "data"
    # tle_script = project_root / "submissions" / "time_limit_exceeded" / "tle.py"
    tle_script = project_root / "submissions" / "accepted" / "solution.py"
    
    if not tle_script.exists():
        print(f"Error: TLE script not found at {tle_script}")
        return
    
    # Collect all test files
    test_dirs = [
        ("sample", data_dir / "sample"),
        ("secret", data_dir / "secret")
    ]
    
    all_results = []
    
    for dir_name, dir_path in test_dirs:
        if not dir_path.exists():
            print(f"Warning: Directory {dir_path} not found")
            continue
        
        # Find all .in files
        input_files = sorted(dir_path.glob("*.in"))
        
        for input_file in input_files:
            test_name = input_file.stem  # e.g., "test1"
            answer_file = input_file.with_suffix(".ans")
            
            print(f"Running {dir_name}/{test_name}...", end=" ", flush=True)
            
            runtime, output, success, error = run_test(input_file, tle_script)
            
            # Check correctness
            correct = None
            if success and answer_file.exists():
                correct = check_answer(output, answer_file)
            
            all_results.append({
                "dir": dir_name,
                "test": test_name,
                "runtime": runtime,
                "success": success,
                "correct": correct,
                "error": error,
                "output": output
            })
            
            # Print immediate result
            if not success:
                print(f"❌ {error} ({runtime:.3f}s)")
            elif correct is True:
                print(f"✓ {runtime:.3f}s")
            elif correct is False:
                print(f"⚠️  WRONG ({runtime:.3f}s)")
            else:
                print(f"? {runtime:.3f}s")
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"{'Test':<20} {'Runtime (s)':<15} {'Status':<20}")
    print("-"*70)
    
    total_runtime = 0
    passed = 0
    failed = 0
    timeout = 0
    
    for result in all_results:
        test_label = f"{result['dir']}/{result['test']}"
        runtime_str = f"{result['runtime']:.3f}"
        
        if not result['success']:
            status = result['error']
            timeout += 1
        elif result['correct'] is True:
            status = "✓ CORRECT"
            passed += 1
        elif result['correct'] is False:
            status = "⚠️  WRONG ANSWER"
            failed += 1
        else:
            status = "? NO ANSWER FILE"
        
        print(f"{test_label:<20} {runtime_str:<15} {status:<20}")
        
        if result['success']:
            total_runtime += result['runtime']
    
    print("-"*70)
    print(f"\nTotal tests: {len(all_results)}")
    print(f"Passed: {passed}")
    print(f"Wrong: {failed}")
    print(f"Timeout: {timeout}")
    print(f"Total runtime: {total_runtime:.3f}s")
    
    # Show slowest tests
    successful_tests = [r for r in all_results if r['success']]
    if successful_tests:
        print(f"\nSlowest tests:")
        slowest = sorted(successful_tests, key=lambda x: x['runtime'], reverse=True)[:5]
        for r in slowest:
            print(f"  {r['dir']}/{r['test']}: {r['runtime']:.3f}s")
    
    # Show fastest tests
    if successful_tests:
        print(f"\nFastest tests:")
        fastest = sorted(successful_tests, key=lambda x: x['runtime'])[:5]
        for r in fastest:
            print(f"  {r['dir']}/{r['test']}: {r['runtime']:.3f}s")
    
    # Calculate average runtime
    if successful_tests:
        avg_runtime = sum(r['runtime'] for r in successful_tests) / len(successful_tests)
        print(f"\nAverage runtime: {avg_runtime:.3f}s")
        print(f"Total runtime (all tests): {total_runtime:.3f}s")

if __name__ == "__main__":
    main()

