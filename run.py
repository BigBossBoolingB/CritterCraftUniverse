import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from crittercraft import __main__

if __name__ == "__main__":
    __main__.main()
