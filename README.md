# Cryptography & Nullity Demonstration - Improved Version

This application demonstrates why singular matrices fail in cryptography through an interactive visualization.

## Files

- `main_improved.py` - The updated entry point for the application
- `gui_improved.py` - The enhanced Tkinter UI implementation with better responsiveness
- `matrix_crypto.py` - The cryptography logic implementation

## Improvements Made

The improved version of the application addresses several UI issues:

1. **Fixed Scrollbar Issues**:
   - Detailed results now properly show scrollbars
   - Used tkinter's ScrolledText widget for more reliable scrolling

2. **Better Responsive Layout**:
   - Switched from pack to grid layout manager for better control
   - Configured weight properties to make UI elements resize properly
   - Window elements now properly expand when resizing the window

3. **Improved Tab Visibility**:
   - Tabs are now more visible and accessible
   - Content properly expands to fill available space

4. **General UI Enhancements**:
   - Added better spacing and padding
   - Improved overall layout organization
   - Added scrolling capabilities to all text widgets

## How to Run the Improved Version

1. Make sure you have Python installed with tkinter, numpy, and matplotlib
2. Run: `python main_improved.py`

## Troubleshooting

If you encounter any issues with the improved version, you can still run the original version with:
`python main.py`

## Using the Application

1. Select a matrix type (Invertible, Singular, or Custom)
2. Enter a message to encrypt
3. Click "Run Encryption" to see the results
4. Explore both the graph and detailed results tabs
5. Try different matrices to see how they affect encryption/decryption

## Educational Value

This tool helps students understand:
- Why determinant and nullity matter in matrix operations
- The connection between linear algebra and cryptography
- How information preservation relates to matrix invertibility
- The practical implications of singular vs. non-singular matrices