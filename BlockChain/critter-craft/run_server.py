"""
Web Server Entry Point.

Use this script to run the Flask development server.
"""

# We need to make sure the 'src' directory is in the Python path
# so that the application can be imported correctly.
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from api.app import app

if __name__ == '__main__':
    # It's good practice to allow host and port to be configured via environment variables
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))

    # The 'debug=True' mode should be used only for development.
    # A production deployment would use a proper WSGI server like Gunicorn or uWSGI.
    app.run(host=host, port=port, debug=True)
