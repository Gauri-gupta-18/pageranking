"""
Main file to execute all SEO factors using plugin architecture.

Every .py file containing a check_* function is automatically loaded.
Future-ready for:
- URL
- Keyword
- Multiple Keywords
- Competitor URL
"""

from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import sys

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

def load_plugins():
    # Load all plugin files

    plugins = []

    python_files = list(BASE_DIR.glob("*.py"))

    metrics_dir = BASE_DIR / "metrics"

    if metrics_dir.exists():
        python_files.extend(metrics_dir.glob("*.py"))

    for file in python_files:

        # Skip main.py
        if file.name == Path(__file__).name:
            continue

        # Skip __init__.py
        if file.name.startswith("__"):
            continue

        try:

            spec = spec_from_file_location(
                file.stem,
                str(file)
            )

            module = module_from_spec(spec)

            spec.loader.exec_module(module)

            # Find all checker functions
            for name in dir(module):

                if not name.startswith("check_"):
                    continue

                func = getattr(module, name)

                if callable(func):

                    plugins.append(
                        {
                            "file": file.name,
                            "function": name,
                            "callable": func
                        }
                    )

        except Exception as error:

            print(
                f"Failed to load plugin "
                f"{file.name}: {error}"
            )

    return plugins


def run_seo_analysis(context):
    # Execute all plugins

    report = {}

    print("\nStarting SEO Analysis...\n")

    plugins = load_plugins()

    if not plugins:

        print("No plugins found.")

        return report

    for plugin in plugins:

        function_name = plugin["function"]

        factor_name = (
            function_name
            .replace("check_", "")
            .replace("_", " ")
            .title()
        )

        print(
            f"Running {factor_name} "
            f"from {plugin['file']}"
        )

        try:

            result = plugin["callable"](context)

            report[
                result.get(
                    "factor",
                    factor_name
                )
            ] = result

        except Exception as error:

            report[factor_name] = {
                "factor": factor_name,
                "status": "Error",
                "error": str(error)
            }

    print("\nSEO Analysis Completed!")

    return report


def display_report(report):
    # Print final report

    print(
        "\n========== FINAL SEO REPORT ==========\n"
    )

    for factor, result in report.items():

        print(f"{factor}")

        print(result)

        print("-" * 50)


if __name__ == "__main__":

    # Website URL
    url = input(
        "Enter Website URL: "
    ).strip()

    # Primary keyword
    keyword = input(
        "Enter Primary Keyword (optional): "
    ).strip()

    # Multiple keywords
    keywords_input = input(
        "Enter Keywords separated by comma (optional): "
    ).strip()

    keywords = []

    if keywords_input:

        keywords = [
            item.strip()
            for item in keywords_input.split(",")
            if item.strip()
        ]

    # Competitor URL
    competitor_url = input(
        "Enter Competitor URL (optional): "
    ).strip()

    # Shared context for all plugins
    context = {
        "url": url,
        "keyword": keyword,
        "keywords": keywords,
        "competitor_url": competitor_url
    }

    report = run_seo_analysis(context)

    display_report(report)

# nitin
