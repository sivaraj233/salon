import sys
import os
from app import app  # Import your Flask app

# Add project directory to PythonAnywhere path
path = '/home/srilakshmim/salon'
if path not in sys.path:
    sys.path.append(path)

# Run the application
application = app
