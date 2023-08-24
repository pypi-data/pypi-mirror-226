# vercelkit.py - Streamlined Deployment of Django Projects to Vercel

"""
The 'vercelkit.py' module offers a toolkit for simplifying the deployment of Django projects
to the Vercel platform. It includes functions for generating deployment files, configuring
settings, and automating the deployment process.

Usage:
    Import and utilize the functions within this module to streamline the deployment of your
    Django project to Vercel. Refer to the individual function documentation for detailed
    information on usage and parameters.

Features:
    - 'generate_vercel_files()': Generate deployment files required for Vercel deployment.
    - 'configure_project_settings()': Configure project settings for Vercel deployment.
    - 'automate_deployment()': Automate the deployment process to Vercel.

Functions:
    - 'generate_vercel_files()': Generate Vercel-specific deployment files.
    - 'configure_project_settings()': Configure project settings for Vercel deployment.
    - 'automate_deployment()': Automate the deployment process to Vercel.

"""

import sys
from .Base import create_folders, create_templatetags
from .Host import generate_files, Change_the_files
from .Template import convert_to_django_html, djangotemp, t_size
from Designer.BackGroundColor import *
from Designer.ForeGroundColor import *

def print_version():
    """Prints the version information."""
    print("-" * 50)
    print(f"Version: {green('0.0.1')}")
    print("-" * 50)

def print_help():
    """Prints the help message."""
    print("-")
    print("Django Project Helper Script")
    print("This script provides various utilities to assist in managing a Django project.")
    print("\nUsage:")
    print(f"  {blue('--base')}           {pink('Create base folders')} for a new Django project.")
    print(f"  {blue('--vercelhost')}     Generate files and {pink('update settings')} for {pink('Vercel hosting')}.")
    print(f"  {blue('--inphtml <path>')} Convert an HTML file to {pink('Django template')} format.")
    print(f"  {blue('--djhtml')}         Generate a {pink('Django HTML template')}.")
    print(f"  {blue('--version')}        Display {pink('version information')}.")
    print(f"  {blue('-h, --help')}       Display {pink('this help message')}.")
    print("\nOptions:")
    print(f"  {blue('--base')}:")
    print("    Creates the base folders required for a new Django project.")
    print(f"  {blue('--vercelhost')}:")
    print("    Generates files and updates settings for deploying on Vercel hosting.")
    print(f"  {blue('--inphtml <path>')}:")
    print("    Converts an HTML file to a Django template format.")
    print(f"  {blue('--djhtml')}:")
    print("    Generates a Django HTML template file.")
    print(f"  {blue('--version')} / {blue('--V')} / {blue('--v')}:")
    print("    Displays the version of the script.")
    print("\nColor Codes:")
    print(f"  {red('Red')}, {blue('Blue')}, {green('Green')}, {yellow('Yellow')}, {brown('Brown')}, {pink('Pink')}")

def print_error(message):
    """Prints an error message in red."""
    print(red(f"Error: {message}"))

def main():
    # Check for command-line arguments
    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        print_help()
    elif "--base" in sys.argv:
        create_folders()
        create_templatetags()
    elif "--vercelhost" in sys.argv:
        generate_files()
        Change_the_files()
    elif "--inphtml" in sys.argv:
        if len(sys.argv) >= 3:
            convert_to_django_html(sys.argv[2], sys.argv[2])
        else:
            print_error("Please provide the input HTML file path.")
    elif "--djhtml" in sys.argv:
        djangotemp()
    elif "--version" in sys.argv or "--V" in sys.argv or "--v" in sys.argv:
        print_version()
    else:
        print_error("Unknown command. Use '--help' to see available options.")

if __name__ == '__main__':
    main()