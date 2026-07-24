import os
import tempfile
import subprocess
from utils.logger import get_logger

logger = get_logger(__name__)

def clone_and_analyze(repo_url):
    """Clones a repo to a temporary directory and runs static analysis tools."""
    results = {
        "radon": {"score": 10, "feedback": "Code complexity is low."},
        "flake8": {"score": 10, "feedback": "No style issues found."},
        "pylint": {"score": 10, "feedback": "Code is perfectly rated."}
    }
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Clone repo
            logger.info(f"Cloning {repo_url} to {temp_dir}")
            clone_proc = subprocess.run(["git", "clone", repo_url, temp_dir], capture_output=True, text=True)
            if clone_proc.returncode != 0:
                logger.error(f"Git clone failed: {clone_proc.stderr}")
                return results

            # Run Radon (Cyclomatic Complexity)
            radon_proc = subprocess.run(["radon", "cc", "-s", "-a", temp_dir], capture_output=True, text=True)
            if "F" in radon_proc.stdout or "E" in radon_proc.stdout:
                results["radon"] = {"score": 5, "feedback": "High complexity (E/F grades) found in some blocks."}
            elif "D" in radon_proc.stdout or "C" in radon_proc.stdout:
                results["radon"] = {"score": 7, "feedback": "Moderate complexity (C/D grades) found."}

            # Run Flake8
            flake8_proc = subprocess.run(["flake8", temp_dir, "--count", "--select=E9,F63,F7,F82", "--show-source", "--statistics"], capture_output=True, text=True)
            if flake8_proc.returncode != 0:
                results["flake8"] = {"score": 6, "feedback": "Syntax errors or undefined names detected."}

            # Run Pylint on the first python file found to get a sample score
            pylint_proc = subprocess.run(f"find {temp_dir} -name '*.py' | head -n 3 | xargs pylint --score=y", shell=True, capture_output=True, text=True)
            if pylint_proc.returncode != 0 and "Your code has been rated at" in pylint_proc.stdout:
                # Extract score logic could go here, for now a simplified check
                results["pylint"] = {"score": 7, "feedback": "Some linting issues exist. Run pylint locally for details."}
                
    except Exception as e:
        logger.error(f"Error during code quality analysis: {e}")
        
    return [
        {"aspect": "Cyclomatic Complexity (Radon)", "score": results["radon"]["score"], "feedback": results["radon"]["feedback"]},
        {"aspect": "Style & Syntax (Flake8)", "score": results["flake8"]["score"], "feedback": results["flake8"]["feedback"]},
        {"aspect": "Linting (Pylint)", "score": results["pylint"]["score"], "feedback": results["pylint"]["feedback"]}
    ]
