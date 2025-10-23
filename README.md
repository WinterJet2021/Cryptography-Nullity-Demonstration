# Cryptography & Nullity: Singular Matrices Demo

This application demonstrates why singular matrices fail in encoding/decoding messages in cryptography, particularly in the context of the Hill cipher.

## Features

- **Interactive Matrix Selection**: Try different matrices and see their properties
- **Encryption/Decryption Demo**: See how different matrices affect message encryption
- **Visual Transformation**: Understand the geometric interpretation of matrix transformations
- **Comprehensive Explanation**: Learn the mathematical and information-theoretic reasons behind the failure

## Files

- **main.py**: Entry point for the application
- **algorithm.py**: Contains the mathematical operations and cryptographic algorithms
- **gui.py**: Tkinter-based graphical user interface

## Recent Updates

- Added comprehensive scrolling support throughout the interface
- Fixed issues with content being cut off at the bottom of the window
- Added mouse wheel scrolling for easier navigation
- Improved visualization resizing and display

## How to Use

1. Run the application with:
   ```
   python main.py
   ```

2. The main window now has scrollbars to access all content
3. Try different matrices using the preset buttons or by entering your own values
4. Enter messages to encrypt/decrypt and observe the results
5. Use the scrollbars to navigate through all sections of the application

## Key Concepts Demonstrated

1. **Singular Matrices**: Matrices with determinant = 0
   - Cannot be inverted, making decryption impossible
   - Visually collapse space into lower dimensions

2. **Hill Cipher Requirements**:
   - Matrices must have non-zero determinants
   - Determinant must be coprime with the modulus (26 for English alphabet)
   - Otherwise encryption or decryption will fail

3. **Information Theory**:
   - Singular transformations lose information
   - Multiple inputs map to the same output
   - This violates the one-to-one mapping needed for encryption

## Technical Notes

The application requires:
- Python 3.x
- Tkinter (for GUI)
- NumPy (for matrix operations)
- Matplotlib (for visualization)
- PIL/Pillow (for image handling)