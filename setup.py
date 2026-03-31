from setuptools import setup, find_packages

setup(
    name="nse-stock-analysis-skills",
    version="0.1.0",
    description="Claude Code skills for Indian stock market analysis",
    author="Sumin Pillai",
    author_email="suminpillai@gmail.com",
    url="https://github.com/SuminPillai/NSE-STOCK-ANALYSIS-CLAUDE-SKILLS",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.10",
    install_requires=[
        "yfinance>=0.2.31",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "rich>=13.0.0",
        "tabulate>=0.9.0",
        "platformdirs>=4.0.0",
        "PyYAML>=6.0",
    ],
)
