# Base.py - Essential Functions for Django Project Setup and Configuration

"""
The 'Base.py' module in your Django project provides essential functions for setting up,
configuring, and enhancing your Django project's structure. It offers tools for creating
necessary folders, modifying settings, and optimizing configurations to streamline the
development process.

Usage:
    Import and utilize the functions within this module to facilitate Django project setup
    and configuration tasks.

Features:
    - 'create_folders()': Creates essential 'templates' and 'static' folders for your
      Django project if they don't exist.
    - 'add_to_installed_apps(file_path, app_name)': Adds an app to the INSTALLED_APPS list
      in your project's settings.
    - 'set_allowed_hosts(file_path, desired_allowed_hosts)': Sets the desired ALLOWED_HOSTS
      list in your project's settings.
    - 'comment_out_databases(file_path)': Comments out the DATABASES configuration in
      your project's settings.
    - 'update_static_settings(file_path)': Updates static and media settings for your project.
    - 'base_edit_settings_file(settings_file_path)': Performs a series of base configuration
      updates on your project's settings.

Functions:
    - 'create_folders()': Create necessary 'templates' and 'static' folders.
    - 'add_to_installed_apps(file_path, app_name)': Add an app to INSTALLED_APPS list.
    - 'set_allowed_hosts(file_path, desired_allowed_hosts)': Set ALLOWED_HOSTS.
    - 'comment_out_databases(file_path)': Comment out the DATABASES configuration.
    - 'update_static_settings(file_path)': Update static and media settings.
    - 'base_edit_settings_file(settings_file_path)': Perform base configuration updates.

"""

from .Host import base_edit_settings_file, edit_urls_file, get_app_name, t_size,find_views_folder
import os, re
from Designer.BackGroundColor import *
from Designer.ForeGroundColor import *
from .templatetage import Data

def create_templatetags():
    """
    Creates a 'templatetags' folder within the views folder of the Django project.

    This function checks if the 'templatetags' folder already exists within the views
    folder of the Django project. If it doesn't exist, the function creates the
    'templatetags' folder. If the folder already exists, the function prints a message
    indicating that the folder is already present.

    Note:
        This function assumes that it's being run within a Django project directory
        and that the 'find_views_folder()' function is available to determine the
        views folder.

    Returns:
        None
    """
    # try:
    path = os.path.join(os.getcwd(),find_views_folder())
    tag_path = os.path.join(path,'templatetags')
    if not os.path.exists('templatetags'):
            # Create the folder
            try:
                os.makedirs(tag_path)
            except:
                print(f"{yellow('Warning:')} {blue('templatetags')} {yellow('directory already exists.')}")
            print(tag_path)
            with open(os.path.join(tag_path,"djtemp.py"),'w') as fs:
                fs.write(Data)
            print(f"Folder '{blue('templatetags')}' created successfully. - {green('OK')}")
    else:
        print(f"{red('Folder')} '{blue('templatetags')}'{red(' already exists.')}")
    # except:
    #     print(f'''{red("Error:")} {yellow("manage.py")} {red("is not found in the current directory.")} {green("Please navigate to the directory containing")} {yellow("manage.py")} {green("to proceed.")}''')

    
def create_folders():
    """
    Creates necessary folders and modifies Django settings and URLs files.

    This function creates the 'templates' and 'static' folders if they don't already exist.
    It also checks and edits the Django settings and URLs files to include the 'templates'
    folder in the 'DIRS' list and applies necessary modifications.

    Note:
        This function assumes that it's being run within a Django project directory
        and that functions like 't_size()', 'blue()', 'green()', 'get_app_name()',
        'base_edit_settings_file()', and 'edit_urls_file()' are available in the codebase.

    Returns:
        None
    """

    # Replace 'folder_name' with the name of the folder you want to create
    print((brown(" Base File Creations ".center(t_size()[0],'-'))))
    for folder_name in ['templates','static']:
        # Check if the folder already exists
        if not os.path.exists(folder_name):
            # Create the folder
            os.makedirs(folder_name)
            print(f"Folder '{blue(folder_name)}' created successfully. - {green('OK')}")
        else:
            print(f"{red('Folder')} '{blue(folder_name)}'{red(' already exists.')}")
    print(brown('-')*t_size()[0])
    
    # Define the regular expression pattern to match the 'DIRS' list
    pattern = r"'DIRS': \[\s*\]"
    run=False
    try:
        root_directory = os.path.join(os.getcwd(),get_app_name())
        run=True
    except:
        print(f'''{red(f"The {blue('manage.py')}")}{red(' are not exist your current location')} - {green1(f"Please redirect to the {blue('manage.py')} {green1('location')}.")}''')
        
    if run:
        settings_file_path = os.path.join(root_directory, 'settings.py')
        with open(settings_file_path,'r') as f:
            settings_data = f.read()
            # Check if the 'DIRS' list is empty
            if re.search(pattern, settings_data):
                # If it is empty, add 'templates' to the 'DIRS' list using re.sub()
                modified_settings_data = re.sub(pattern, "'DIRS': ['templates']", settings_data)
                with open(settings_file_path, 'w') as f:
                    f.write(modified_settings_data)
            else:
                modified_settings_data = settings_data
        base_edit_settings_file(settings_file_path)
        edit_urls_file(os.path.join(root_directory, 'urls.py'))
