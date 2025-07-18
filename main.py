#!/usr/bin/env python3
"""
Real Estate Investment Management System
Main application entry point
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main application entry point"""
    try:
        # Initialize logging first
        from real_estate_app.config.logging_config import setup_logging
        logger = setup_logging()
        
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("Real Estate Investment Manager")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Real Estate Tools")
        
        # Set application attributes (PyQt6 has different attribute names)
        try:
            app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
            app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        except AttributeError:
            # These attributes may not exist in all PyQt6 versions
            pass
        
        # Import and initialize main window
        from real_estate_app.gui.main_window import MainWindow
        
        logger.info("Initializing main window...")
        window = MainWindow()
        
        # Show the main window
        window.show()
        
        logger.info("Application started successfully")
        
        # Run the application
        return app.exec()
        
    except ImportError as e:
        error_msg = f"Import error: {e}\n\nPlease ensure all dependencies are installed:\npip install -r requirements.txt"
        print(error_msg)
        
        # Try to show error dialog if PyQt6 is available
        try:
            if 'app' in locals():
                QMessageBox.critical(None, "Import Error", error_msg)
            else:
                app = QApplication(sys.argv)
                QMessageBox.critical(None, "Import Error", error_msg)
        except:
            pass
        
        return 1
        
    except Exception as e:
        error_msg = f"Application error: {e}"
        print(error_msg)
        
        # Try to log the error
        try:
            if 'logger' in locals():
                logger.exception("Application startup failed")
        except:
            pass
        
        # Try to show error dialog
        try:
            if 'app' in locals():
                QMessageBox.critical(None, "Application Error", error_msg)
            else:
                app = QApplication(sys.argv)
                QMessageBox.critical(None, "Application Error", error_msg)
        except:
            pass
        
        return 1

if __name__ == "__main__":
    sys.exit(main())