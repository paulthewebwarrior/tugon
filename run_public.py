"""
Script to run the Flask app with a public ngrok tunnel.
"""
from flask import Flask
import os
from pyngrok import ngrok
import sys

# Import the app from the main application file
sys.path.insert(0, os.path.dirname(__file__))
from app import app

def run_with_ngrok():
    """Run the Flask app with ngrok tunnel."""
    # Set port
    port = 5000
    
    # Open ngrok tunnel
    public_url = ngrok.connect(port)
    print("\n" + "="*60)
    print(f"🌐 Public URL: {public_url}")
    print("="*60)
    print("\nShare this URL to allow public access to your site!")
    print("Press CTRL+C to stop the server and close the tunnel.\n")
    
    # Run the Flask app
    app.run(port=port, debug=False)

if __name__ == "__main__":
    run_with_ngrok()