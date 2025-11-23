#!/usr/bin/env python3
"""
Benchmark Tool for Kattis-style Problem Solutions
Evaluates multiple language solutions against test cases
"""

import os
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import sys

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class BenchmarkRunner:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.submissions_dir = project_root / "submissions" / "accepted"
        self.sample_dir = project_root / "data" / "sample"
        self.secret_dir = project_root / "data" / "secret"
        
        # Solution configurations
        self.solutions = {
            "Python": {
                "source": self.submissions_dir / "solution.py",
                "compile_cmd": None,
                "run_cmd": lambda: [sys.executable, str(self.submissions_dir / "solution.py")],
                "compiled": False
            },
            "Java": {
                "source": self.submissions_dir / "Main.java",
                "compile_cmd": lambda: ["javac", str(self.submissions_dir / "Main.java")],
                "run_cmd": lambda: ["java", "-cp", str(self.submissions_dir), "Main"],
                "compiled": False
            },
            "C++": {
                "source": self.submissions_dir / "solution.cpp",
                "compile_cmd": lambda: ["g++", "-O2", "-std=c++17", 
                                        str(self.submissions_dir / "solution.cpp"),
                                        "-o", str(self.submissions_dir / "solution")],
                "run_cmd": lambda: [str(self.submissions_dir / "solution.exe" if os.name == 'nt' else self.submissions_dir / "solution")],
                "compiled": False
            }
        }
        
        self.results = {}
        
    def compile_solutions(self) -> bool:
        """Compile solutions that need compilation"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}COMPILING SOLUTIONS{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
        
        all_success = True
        
        for lang, config in self.solutions.items():
            if config["compile_cmd"] is None:
                print(f"{Colors.CYAN}[{lang}]{Colors.END} No compilation needed")
                config["compiled"] = True
                continue
                
            print(f"{Colors.CYAN}[{lang}]{Colors.END} Compiling...", end=" ")
            try:
                result = subprocess.run(
                    config["compile_cmd"](),
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    print(f"{Colors.GREEN}[OK] Success{Colors.END}")
                    config["compiled"] = True
                else:
                    print(f"{Colors.RED}[FAIL] Failed{Colors.END}")
                    print(f"  Error: {result.stderr}")
                    config["compiled"] = False
                    all_success = False
                    
            except subprocess.TimeoutExpired:
                print(f"{Colors.RED}[FAIL] Timeout{Colors.END}")
                config["compiled"] = False
                all_success = False
            except Exception as e:
                print(f"{Colors.RED}[FAIL] Error: {e}{Colors.END}")
                config["compiled"] = False
                all_success = False
                
        return all_success
    
    def get_test_cases(self) -> Dict[str, List[Tuple[Path, Path]]]:
        """Collect all test cases from sample and secret directories"""
        test_cases = {"sample": [], "secret": []}
        
        for category, directory in [("sample", self.sample_dir), ("secret", self.secret_dir)]:
            if not directory.exists():
                continue
                
            # Find all .in files
            in_files = sorted(directory.glob("*.in"))
            
            for in_file in in_files:
                ans_file = in_file.with_suffix(".ans")
                if ans_file.exists():
                    test_cases[category].append((in_file, ans_file))
                    
        return test_cases
    
    def run_solution(self, lang: str, input_file: Path, timeout: int = 10) -> Tuple[Optional[str], float, bool]:
        """
        Run a solution with given input
        Returns: (output, execution_time, success)
        """
        config = self.solutions[lang]
        
        if not config["compiled"]:
            return None, 0.0, False
            
        try:
            with open(input_file, 'r') as f:
                input_data = f.read()
            
            start_time = time.perf_counter()
            result = subprocess.run(
                config["run_cmd"](),
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            end_time = time.perf_counter()
            
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if result.returncode == 0:
                return result.stdout.strip(), execution_time, True
            else:
                return None, execution_time, False
                
        except subprocess.TimeoutExpired:
            return None, timeout * 1000, False
        except Exception as e:
            return None, 0.0, False
    
    def verify_output(self, actual: str, expected: str) -> bool:
        """Verify if actual output matches expected output"""
        # Strip whitespace and compare
        return actual.strip() == expected.strip()
    
    def run_benchmarks(self):
        """Run all solutions against all test cases"""
        test_cases = self.get_test_cases()
        total_tests = sum(len(cases) for cases in test_cases.values())
        
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}RUNNING BENCHMARKS{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"Total test cases: {total_tests} (Sample: {len(test_cases['sample'])}, Secret: {len(test_cases['secret'])})\n")
        
        for lang, config in self.solutions.items():
            if not config["compiled"]:
                print(f"{Colors.YELLOW}[{lang}] Skipped (compilation failed){Colors.END}\n")
                continue
                
            self.results[lang] = {
                "sample": [],
                "secret": [],
                "summary": {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "total_time": 0.0,
                    "avg_time": 0.0,
                    "min_time": float('inf'),
                    "max_time": 0.0
                }
            }
            
            print(f"{Colors.CYAN}{Colors.BOLD}[{lang}]{Colors.END}")
            print("-" * 60)
            
            for category in ["sample", "secret"]:
                for in_file, ans_file in test_cases[category]:
                    test_name = in_file.stem
                    
                    # Read expected output
                    with open(ans_file, 'r') as f:
                        expected = f.read().strip()
                    
                    # Run solution
                    output, exec_time, success = self.run_solution(lang, in_file)
                    
                    # Verify correctness
                    if success and output is not None:
                        correct = self.verify_output(output, expected)
                    else:
                        correct = False
                    
                    # Store results
                    result = {
                        "test": test_name,
                        "time_ms": exec_time,
                        "correct": correct,
                        "success": success
                    }
                    
                    self.results[lang][category].append(result)
                    self.results[lang]["summary"]["total"] += 1
                    
                    if correct:
                        self.results[lang]["summary"]["passed"] += 1
                        status = f"{Colors.GREEN}[PASS]{Colors.END}"
                    else:
                        self.results[lang]["summary"]["failed"] += 1
                        status = f"{Colors.RED}[FAIL]{Colors.END}"
                    
                    if success:
                        self.results[lang]["summary"]["total_time"] += exec_time
                        self.results[lang]["summary"]["min_time"] = min(
                            self.results[lang]["summary"]["min_time"], exec_time
                        )
                        self.results[lang]["summary"]["max_time"] = max(
                            self.results[lang]["summary"]["max_time"], exec_time
                        )
                    
                    print(f"  {category:8} {test_name:10} {status}  {exec_time:8.2f} ms")
            
            # Calculate average
            if self.results[lang]["summary"]["passed"] > 0:
                self.results[lang]["summary"]["avg_time"] = (
                    self.results[lang]["summary"]["total_time"] / 
                    self.results[lang]["summary"]["passed"]
                )
            
            print()
    
    def print_summary(self):
        """Print summary statistics"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}SUMMARY{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
        
        # Table header
        print(f"{'Language':<15} {'Passed':<10} {'Failed':<10} {'Avg (ms)':<12} {'Min (ms)':<12} {'Max (ms)':<12}")
        print("-" * 80)
        
        for lang in ["Python", "Java", "C++"]:
            if lang not in self.results:
                print(f"{lang:<15} {'N/A':<10} {'N/A':<10} {'N/A':<12} {'N/A':<12} {'N/A':<12}")
                continue
                
            summary = self.results[lang]["summary"]
            
            passed_str = f"{Colors.GREEN}{summary['passed']}/{summary['total']}{Colors.END}"
            failed_str = f"{Colors.RED}{summary['failed']}{Colors.END}" if summary['failed'] > 0 else "0"
            
            if summary['passed'] > 0:
                avg_time = f"{summary['avg_time']:.2f}"
                min_time = f"{summary['min_time']:.2f}"
                max_time = f"{summary['max_time']:.2f}"
            else:
                avg_time = min_time = max_time = "N/A"
            
            print(f"{lang:<15} {passed_str:<20} {failed_str:<20} {avg_time:<12} {min_time:<12} {max_time:<12}")
        
        print()
    
    def print_performance_comparison(self):
        """Print performance comparison between languages"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}PERFORMANCE COMPARISON (for passed tests only){Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
        
        # Get languages with valid results
        valid_langs = [lang for lang in self.results 
                      if self.results[lang]["summary"]["passed"] > 0]
        
        if not valid_langs:
            print("No valid results to compare\n")
            return
        
        # Find fastest language
        fastest_lang = min(valid_langs, 
                          key=lambda l: self.results[l]["summary"]["avg_time"])
        fastest_time = self.results[fastest_lang]["summary"]["avg_time"]
        
        print(f"{'Language':<15} {'Avg Time (ms)':<15} {'Relative Speed':<20}")
        print("-" * 50)
        
        for lang in ["C++", "Java", "Python"]:  # Order by typical speed
            if lang not in valid_langs:
                continue
                
            avg_time = self.results[lang]["summary"]["avg_time"]
            relative = avg_time / fastest_time
            
            if lang == fastest_lang:
                speed_str = f"{Colors.GREEN}1.00x (fastest){Colors.END}"
            else:
                speed_str = f"{relative:.2f}x slower"
            
            print(f"{lang:<15} {avg_time:<15.2f} {speed_str}")
        
        print()
    
    def save_results_json(self, output_file: Path = None):
        """Save detailed results to JSON file"""
        if output_file is None:
            output_file = self.project_root / "benchmark_results.json"
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"Detailed results saved to: {output_file}\n")
    
    def run(self):
        """Run the complete benchmark suite"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}   KATTIS PROBLEM BENCHMARK TOOL - Connected Components{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")
        
        # Compile solutions
        if not self.compile_solutions():
            print(f"\n{Colors.YELLOW}Warning: Some solutions failed to compile{Colors.END}")
        
        # Run benchmarks
        self.run_benchmarks()
        
        # Print summaries
        self.print_summary()
        self.print_performance_comparison()
        
        # Save results
        self.save_results_json()
        
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def main():
    # Get project root
    project_root = Path(__file__).parent
    
    # Create and run benchmark
    runner = BenchmarkRunner(project_root)
    runner.run()


if __name__ == "__main__":
    main()

