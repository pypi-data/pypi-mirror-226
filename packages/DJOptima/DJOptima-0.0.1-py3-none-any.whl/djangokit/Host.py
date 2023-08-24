"""
The 'Host.py' module in your Django project simplifies the hosting and deployment process
by providing tools to generate necessary files, configure settings, and streamline the
deployment of your project to hosting platforms like Vercel.

Usage:
    This module is intended to be imported and used within your Django project to facilitate
    the hosting and deployment process.

Features:
    - 'generate_files()': Generate essential files required for deployment, such as
      'vercel.json', 'requirements.txt', and 'build_files.sh'.
    - 'Change_the_files()': Perform a series of essential configuration updates for
      deployment, including updating settings, wsgi files, and URLs.
    - 'Host.djangotemp()': Batch convert HTML files to Django template format in the
      'Host.py' module.

Functions:
    - 'generate_files()': Generate essential deployment files.
    - 'Change_the_files()': Perform essential configuration updates for deployment.
    - 'Host.djangotemp()': Batch convert HTML files to Django template format.
    - ... Other functions related to hosting and deployment.

"""

import os, re, json, ast
import importlib.metadata as metadata
from Designer.BackGroundColor import *
from Designer.ForeGroundColor import *
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> find and get the imported package and there versions >>>>>>>>>>>>>>>>>>>>>>>>

def find_views_folder():
    """
    Searches for the 'views' folder within the current Django project directory.

    This function iterates through the current directory and its subdirectories to locate
    a 'models.py' file. Once found, it identifies the corresponding 'views' folder and
    returns its name.

    Returns:
        str or None: The name of the 'views' folder if found, or None if not found.
    """
    current_directory = os.getcwd()

    for root, dirs, files in os.walk(current_directory):
        if 'models.py' in files:
            return os.path.basename(root)

    return None

def t_size():
    """
    Retrieves the size of the terminal window.

    This function uses the 'os.get_terminal_size()' function to determine the width and height
    of the current terminal window in columns and lines, respectively.

    Returns:
        list: A list containing the terminal width and height in columns and lines.
    """
    terminal_size = os.get_terminal_size()
    terminal_width = terminal_size.columns
    terminal_height = terminal_size.lines
    return [terminal_width, terminal_height]

def get_imported_modules(file_path):
    """
    Retrieves a set of imported modules from a given Python source file.

    This function reads the content of the provided Python source file, parses it using the 'ast' module,
    and extracts imported modules using the 'Import' and 'ImportFrom' nodes. It returns a set containing
    the names of imported modules.

    Args:
        file_path (str): The path to the Python source file.

    Returns:
        set: A set containing the names of imported modules.
    """
    with open(file_path, "r") as file:
        content = file.read()

    # Parse the Python source code
    tree = ast.parse(content)

    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if node.module:
                    imported_modules.add(f"{node.module}.{alias.name}")
                else:
                    imported_modules.add(alias.name)

    return imported_modules

def find_imported_modules(root_dir):
    """
    Finds and returns a list of imported modules across Python files within a directory.

    This function recursively traverses through the provided root directory, identifying all
    Python files (with the ".py" extension) and extracting imported modules using the
    'get_imported_modules()' function. The resulting list contains the names of all imported
    modules found in the specified directory.

    Args:
        root_dir (str): The root directory to search for Python files.

    Returns:
        list: A list of imported module names across the Python files within the directory.
    """
    out = []
    imported_modules = set()
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                imported_modules.update(get_imported_modules(file_path))
    for module in imported_modules:
        out.append(module)
    return out
        
def get_modules_version(module_datas):        
    """
    Retrieves version information for a list of modules.

    This function takes a list of module data, where each data item is in the form of
    'module_name.submodule'. It uses the 'importlib.metadata' module to fetch the version
    information of each module and creates a dictionary with module names as keys and
    corresponding version numbers as values.

    Args:
        module_datas (list): A list of module data in the format 'module_name.submodule'.

    Returns:
        dict: A dictionary containing module names as keys and their version numbers as values.
    """
    module_versions = {}
    for name in module_datas:
        module_name = name.split(".")[0]
        try:
            # Use importlib.metadata to get the version information
            version = metadata.version(module_name)
            module_versions[module_name] = version
        except metadata.PackageNotFoundError:
            pass
    return module_versions

def shortcut_version(root_dir):
    """
    Retrieves version information for imported modules within a directory.

    This function combines the functionality of 'find_imported_modules()' and 'get_modules_version()'
    to quickly retrieve version information for all imported modules within a specified directory.

    Args:
        root_dir (str): The root directory to search for imported modules.

    Returns:
        dict: A dictionary containing module names as keys and their version numbers as values.
    """
    imported_modules = find_imported_modules(root_dir)
    versions = get_modules_version(imported_modules)
    return versions
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Getting App name of django >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def get_app_name():
    """
    Retrieves the Django app name based on the current project's manage.py file.

    This function looks for the 'manage.py' file in the current directory and reads its content
    to find the Django settings module. It then extracts and returns the name of the Django app.

    Returns:
        str: The name of the Django app extracted from the manage.py file.
    """
    root_directory = os.getcwd()
    file_names = os.listdir(root_directory)
    if 'manage.py' in file_names:
        manage_py_path = os.path.join(root_directory, 'manage.py')
        with open(manage_py_path, 'r') as fs:
            lines = fs.readlines()

        for line in lines:
            if 'DJANGO_SETTINGS_MODULE' in line:
                pattern = r"os\.environ\.setdefault\('DJANGO_SETTINGS_MODULE', '(.*?)'\)"
                match = re.search(pattern, line)
                if match:
                    django_settings_module = match.group(1)
                    return django_settings_module.split('.')[0]

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Createing the needed files to deployment >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Define the data as a dictionary
vercel_data_dict = {
    "version": 2,
    "builds": [
        {
            "src": f"{get_app_name()}/wsgi.py",
            "use": "@vercel/python",
            "config": {"maxLambdaSize": "15mb", "runtime": "python3.9"}
        },
        {
            "src": "build_files.sh",
            "use": "@vercel/static-build",
            "config": {
                "distDir": "staticfiles_build"
            }
        }
    ],
    "routes": [
        {
            "src": "/static/(.*)",
            "dest": "/static/$1"
        },
        {
            "src": "/(.*)",
            "dest": f"{get_app_name()}/wsgi.py"
        }
    ]
}
build_data = '''# build_files.sh
pip install -r requirements.txt
python3.9 manage.py collectstatic'''

def generate_files():
    """
    Generates specific files within the current directory for a Django project.

    This function creates certain files ('vercel.json', 'requirements.txt', 'build_files.sh', 'README.md')
    within the current directory for a Django project. It includes writing data to the 'vercel.json' and
    'build_files.sh' files, and generating a 'requirements.txt' file based on the imported module versions.

    Returns:
        None
    """
    files = ['vercel.json','requirements.txt','build_files.sh','README.md']
    # Get the current directory path
    current_directory = os.getcwd()
    # Get the list of file names in the current directory
    file_names = os.listdir(current_directory)
    vercel_data = json.dumps(vercel_data_dict, indent=2)
    if 'manage.py' in file_names:
        # create vercel file
        vercel_json = open(os.path.join(current_directory,files[0]),'w')
        vercel_json.write(vercel_data)
        vercel_json.close()
        print(f"The {blue('vercel.json')} are Created - {green('OK')}. ")
        # create build.sh file 
        build = open(os.path.join(current_directory,'build_files.sh'),'w')
        build.write(build_data)
        build.close()
        print(f"The {blue('build_files.sh')} are Created - {green('OK')}. ")
        # create requirements.txt
        req = open(os.path.join(current_directory,'requirements.txt'),'w')
        req_data = '\n'.join([ f'{i}=={j}' for i,j in shortcut_version(current_directory).items() ])
        req.write(req_data)
        req.close()
        print(f"The {blue('requirements.txt')} are Created - {green('OK')}. ")
    else:
        pass

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Edit Files >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> App SetUp >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def add_to_installed_apps(file_path, app_name):
    """
    Adds a Django app to the INSTALLED_APPS list in a settings file.

    This function reads the content of the specified settings file, checks if the provided app name
    is already in the INSTALLED_APPS list. If not, it adds the app name to the list. It uses regular
    expressions to find the INSTALLED_APPS list and adds the new app entry while preserving the
    existing formatting.

    Args:
        file_path (str): The path to the Django settings file.
        app_name (str): The name of the app to be added.

    Returns:
        None
    """
    # Read the content of the file
    with open(file_path, 'r') as f:
        content = f.read()

    # Check if the app name is already in INSTALLED_APPS
    if f"'{app_name}'" in content:
        print(f"{ yellow('Warning ') }: {yellow1(f' The app ')+yellow1(app_name)+yellow1(' is already in INSTALLED_APPS.')}")
        return

    # Define the new app to be added
    new_app = f"    '{app_name}',\n"

    # Use regular expression to find the INSTALLED_APPS list and add the new app
    pattern = r'INSTALLED_APPS\s*=\s*\[\s*[\s\S]*?\]'
    new_content = re.sub(pattern, lambda match: match.group()[:-2] + f"\n{new_app}]", content, count=1)

    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(new_content)

def set_allowed_hosts(file_path, desired_allowed_hosts):
    """
    Sets the ALLOWED_HOSTS value in a Django settings file.

    This function reads the content of the specified settings file and uses regular expressions
    to find the ALLOWED_HOSTS line. It then replaces the existing ALLOWED_HOSTS value with the
    desired value provided as an argument.

    Args:
        file_path (str): The path to the Django settings file.
        desired_allowed_hosts (str): The desired ALLOWED_HOSTS value to set.

    Returns:
        None
    """
    # Read the content of the file
    with open(file_path, 'r') as f:
        content = f.read()

    # Use regular expression to find the ALLOWED_HOSTS line and replace its value
    pattern = r'ALLOWED_HOSTS\s*=\s*\[[^\]]*\]'
    new_content = re.sub(pattern, f'ALLOWED_HOSTS = {desired_allowed_hosts}', content)

    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(new_content)

def comment_out_databases(file_path):
    """
    Comments out the DATABASES dictionary in a Django settings file.

    This function reads the content of the specified settings file and uses regular expressions
    to find the DATABASES dictionary. It then comments out the entire dictionary by adding
    triple single quotes (''') before and after the dictionary content.

    Args:
        file_path (str): The path to the Django settings file.

    Returns:
        None
    """
    # Read the content of the file
    with open(file_path, 'r') as f:
        content = f.read()
    pattern = r"'''(\s*DATABASES\s*=\s*{\s*[\s\S]*?\s*}\s*)'''"
    match = re.search(pattern, content)

    if not match:
        # Use regular expression to find the DATABASES dictionary and comment it out
        pattern = r'(DATABASES\s*=\s*\{[\s\S]*?\}\s})'
        new_content = re.sub(pattern, r"''' \1 '''", content)
        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.write(new_content)
    else:
        print(f"{ yellow('Warning ') }: {yellow1(f' The DATABASES ')+yellow1(' is already in Commentd.')}")

    
        
def update_static_settings(file_path):
    """
    Updates the static settings in a Django settings file.

    This function reads the content of the specified settings file and uses regular expressions
    to find the STATIC_URL setting. It then replaces the old string with new static settings
    content that includes STATICFILES_DIRS, STATIC_ROOT, MEDIA_ROOT, and MEDIA_URL.

    Args:
        file_path (str): The path to the Django settings file.

    Returns:
        None
    """
    # Read the content of the file
    with open(file_path, 'r') as f:
        content = f.read()

    # Define the new content to replace the old string
    new_content = """import os

STATIC_URL = 'static/'
STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'
"""

    # Use regular expression to find and replace the old string with the new content
    if new_content not in content:
        pattern = r'STATIC_URL\s*=\s*\'static/\''
        content = re.sub(pattern, new_content, content)
        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.write(content)
    else:
        print(f"{ yellow('Warning ') }: {yellow1('Static settings are up-to-date.')}")
        
def update_wsgi_file(file_path):
    """
    Updates the content of a WSGI file to include "app = application" if not present.

    This function reads the content of the specified WSGI file and checks if the line
    "app = application" exists. If not, it appends this line as the last line of the file.

    Args:
        file_path (str): The path to the WSGI file.

    Returns:
        None
    """
    # Read the content of the file
    with open(file_path, 'r') as f:
        content = f.read()

    # If the line "app = application" does not exist in the content, add it as the last line
    if 'app = application' not in content:
        content += '\napp = application\n'

    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(content)

def update_urlpatterns(file_path, content_to_add):
    """
    Updates the urlpatterns in a Django URL configuration file.

    This function reads the content of the specified URL configuration file and checks if
    the provided content is already present in the urlpatterns. If not, it appends the
    content to the end of the urlpatterns list.

    Args:
        file_path (str): The path to the Django URL configuration file.
        content_to_add (str): The content to add to the urlpatterns.

    Returns:
        None
    """
    check = '''urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)'''
    # Read the content of the file
    with open(file_path, 'r') as f:
        content = f.read()

    # Check if the content already exists in urlpatterns
    if re.search(re.escape(content_to_add), content):
        print(f"{ yellow('Warning ') }: {yellow1('Content already exists in urlpatterns.')}")
    else:
        with open(file_path, 'r') as f:
            content = f.read()
        obj=content
        if check not in obj:
            with open(file_path, 'a') as f:
                f.write(obj+content_to_add)
        print(f"In the '{blue('url.py')}' URL's are updated - {green('OK')}")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def base_edit_settings_file(settings_file_path):
    """
    Performs various edits to the base settings file of a Django project.

    This function is designed to apply several modifications to the base settings file of a Django project.
    It adds the app to INSTALLED_APPS, sets the desired ALLOWED_HOSTS value, and updates the static settings.
    After making these changes, it prints a success message.

    Args:
        settings_file_path (str): The path to the Django settings file.

    Returns:
        None
    """
    app_name = find_views_folder()  
    desired_allowed_hosts = "['127.0.0.1', '.vercel.app', '.now.sh']"  
    # Add the app to INSTALLED_APPS
    add_to_installed_apps(settings_file_path, app_name)
    # Set the desired ALLOWED_HOSTS
    set_allowed_hosts(settings_file_path, desired_allowed_hosts)
    
    update_static_settings(settings_file_path)
    print(f"Base Settings are updated in the {blue('settings.py')} - {green('OK')}")
    

# Function to edit the settings.py file
def edit_settings_file(settings_file_path):
    """
    Performs various edits to the settings file for Vercel hosting in a Django project.

    This function is designed to apply multiple modifications to the settings file of a Django project
    that is intended for Vercel hosting. It adds the app to INSTALLED_APPS, sets the desired ALLOWED_HOSTS value,
    comments out the DATABASES dictionary, and updates the static settings. After making these changes,
    it prints a success message.

    Args:
        settings_file_path (str): The path to the Django settings file.

    Returns:
        None
    """
    desired_allowed_hosts = "['127.0.0.1', '.vercel.app', '.now.sh']"  
    # Add the app to INSTALLED_APPS
    add_to_installed_apps(settings_file_path, find_views_folder())
    # Set the desired ALLOWED_HOSTS
    set_allowed_hosts(settings_file_path, desired_allowed_hosts)
    
    comment_out_databases(settings_file_path)
    
    update_static_settings(settings_file_path)
    print(f"Vercel Hosting Base Settings are updated in the"+blue('settings.py')+"-"+green('OK'))
    
# Function to edit the wsgi.py file
def edit_wsgi_file(wsgi_file_path):
    """
    Edits a WSGI file by updating it using the 'update_wsgi_file' function.

    This function simply calls the 'update_wsgi_file' function to perform the necessary edits on
    the specified WSGI file.

    Args:
        wsgi_file_path (str): The path to the WSGI file.

    Returns:
        None
    """
    update_wsgi_file(wsgi_file_path)

def edit_urls_file(file_path):
    """
    Edits a URLs file by updating it with additional content using the 'update_urlpatterns' function.

    This function generates additional content that needs to be added to a URLs file, particularly
    importing static URLs and adding patterns for media and static files. The 'update_urlpatterns'
    function is then called to apply these changes to the specified URLs file.

    Args:
        file_path (str): The path to the URLs file.

    Returns:
        None
    """
    content_to_add = f"""from django.conf.urls.static import static
from {get_app_name()} import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)"""
    update_urlpatterns(file_path, content_to_add)

def Change_the_files():
    """
    Performs a series of file edits and updates for a Django project.

    This function first obtains the root directory of the Django project using the 'get_app_name'
    function. If a valid name is obtained, it proceeds to update the 'settings.py', 'wsgi.py', and
    'urls.py' files by calling respective editing functions.

    Args:
        None

    Returns:
        None
    """
    # Get the root directory of your Django project
    Name = get_app_name()
    if Name:
        root_directory = os.path.join( os.getcwd(),Name)
        # Update the settings.py file
        settings_file_path = os.path.join(root_directory, 'settings.py')
        edit_settings_file(settings_file_path)
        # Update the wsgi.py file
        wsgi_file_path = os.path.join(root_directory, 'wsgi.py')
        edit_wsgi_file(wsgi_file_path)
        # Update the urls.py file
        urls_file_path = os.path.join(root_directory, 'urls.py')
        edit_urls_file(urls_file_path)
    else:
        print(f'''{red(f"The {blue('manage.py')}")}{red(' are not exist your current location')} - {green1('Please provide a name for your application')}''')
    

