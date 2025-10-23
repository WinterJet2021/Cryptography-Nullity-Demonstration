"""
Startup file for the Cryptography & Nullity demonstration application.
This file is the entry point for the modular Tkinter application.
"""

import tkinter as tk
from gui import CryptographyApp
from matrix_crypto import MatrixCrypto

def main():
    """
    Main function to start the application.
    """
    print("=" * 60)
    print("CRYPTOGRAPHY & NULLITY DEMONSTRATION")
    print("Why singular matrices fail in encoding/decoding messages")
    print("=" * 60)
    print("\nLaunching interactive demonstration...")
    print("- Try both invertible and singular matrices")
    print("- Enter your own message to encrypt")
    print("- Create custom matrices to test")
    print("- See how nullity affects information preservation")
    print("- Understand why singular matrices break cryptography")
    print("- Drag the borders between sections to resize them")
    print("=" * 60)
    
    # Create the crypto model
    crypto_model = MatrixCrypto()
    
    # Create the main window
    root = tk.Tk()
    root.title("Cryptography & Nullity Demonstration")
    
    # Set application icon (optional)
    try:
        root.iconbitmap("lock_icon.ico")  # You can add an icon file if available
    except tk.TclError:
        pass  # No icon available, continue without it
    
    # Initialize the application
    app = CryptographyApp(root, crypto_model)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()