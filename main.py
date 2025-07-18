#!/usr/bin/env python3
"""
Real Estate Investment Management System
Main application entry point
"""

import sys
import os
from PyQt6.QtWidgets import QApplication

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Real Estate Investment Manager")
    app.setApplicationVersion("1.0.0")
    
    # TODO: Import and initialize main window
    # from real_estate_app.gui.main_window import MainWindow
    # window = MainWindow()
    # window.show()
    
    print("Real Estate Investment Management System - Starting...")
    print("Project structure created. Ready for development.")
    
    # For now, just exit gracefully
    return 0

if __name__ == "__main__":
    sys.exit(main())