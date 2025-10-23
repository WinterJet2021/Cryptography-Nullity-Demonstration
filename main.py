#!/usr/bin/env python3
"""
Cryptography & Nullity Demo
Main entry point to run the application demonstrating why singular matrices
fail in encoding/decoding messages in cryptography.
"""

import tkinter as tk
from gui import CryptographyDemoApp

def main():
    """Main entry point for the application"""
    root = tk.Tk()
    root.title("Cryptography & Nullity: Singular Matrices Demo")
    
    # Create and run the application
    app = CryptographyDemoApp(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()