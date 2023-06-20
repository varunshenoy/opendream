import os
import importlib.util

EXTENSIONS_TO_IGNORE = []

def gather_extensions(directory):
    # Add directory to Python path
    os.sys.path.append(directory)

    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename not in EXTENSIONS_TO_IGNORE:
            # Remove file extension to get the module name
            module_name = os.path.splitext(filename)[0]
            file_path = os.path.join(directory, filename)

            # Load and execute the module
            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"Successfully executed {file_path}")
            except Exception as e:
                print(f"Error running {file_path}: {e}")

directory_path = "./opendream/extensions/"
gather_extensions(directory_path)