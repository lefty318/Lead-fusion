#!/usr/bin/env python
"""Simple script to start the server and show any errors"""
import sys
import traceback

try:
    print("Starting OmniLead Backend Server...")
    print("=" * 50)

    # Import to check for errors
    print("\nImporting application...")
    from app.main import socket_app
    print("Application imported successfully")

    # Start server
    print("\nStarting server on http://0.0.0.0:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("   Health: http://localhost:8000/health")
    print("\n" + "=" * 50)
    print("Server is starting...\n")

    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8000, reload=True)

except Exception as e:
    print("\nERROR STARTING SERVER:")
    print("=" * 50)
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    print("\nFull Traceback:")
    print("-" * 50)
    traceback.print_exc()
    sys.exit(1)

