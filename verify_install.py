import nmap
import rich
import dotenv
import google.generativeai as genai
import sys

print(f"Python version: {sys.version}")
print(f"nmap version: {nmap.__version__ if hasattr(nmap, '__version__') else 'unknown'}")
print(f"rich version: {rich.__version__ if hasattr(rich, '__version__') else 'unknown'}")
print(f"dotenv version: {dotenv.__version__ if hasattr(dotenv, '__version__') else 'unknown'}")
print(f"google-generativeai version: {genai.__version__ if hasattr(genai, '__version__') else 'unknown'}")

print("\nVerification successful! All modules imported correctly.")
