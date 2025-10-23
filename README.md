# Cryptography & Nullity Demonstration

## Project Description
This interactive application demonstrates **why singular matrices fail in cryptography** for Project 6 of the Linear Transformations and Rank/Nullity mini-projects. It provides a visual and mathematical explanation of how matrix properties affect encryption and decryption.

## How to Run
1. Make sure you have Python installed
2. Install required packages:
   ```
   pip install numpy matplotlib
   ```
3. Run the application:
   ```
   python main.py
   ```

## Files Included
- `main.py` - Entry point for the application
- `matrix_crypto.py` - Contains the matrix operations and cryptography logic
- `gui.py` - Implements the Tkinter user interface

## How to Use the Application

### Step 1: Choose a Matrix
- Select either **Invertible Matrix** (determinant ≠ 0) or **Singular Matrix** (determinant = 0)
- You can also create a custom matrix by entering values in the 3×3 grid

### Step 2: Enter a Message
- Type any message in the text field (letters A-Z and spaces)

### Step 3: Run Encryption
- Click the **Run Encryption** button
- Observe how the message is encrypted and whether it can be decrypted

### Step 4: Analyze Results
- The graph shows original, encrypted, and (if possible) decrypted values
- The results area explains whether decryption succeeded or failed
- Matrix properties show determinant, rank, nullity, and security assessment

## Key Concepts Demonstrated

### Singular vs. Non-singular Matrices
- **Non-singular Matrix**: Has a non-zero determinant and can be inverted
- **Singular Matrix**: Has a zero determinant and cannot be inverted

### The Rank-Nullity Theorem
For an n×n matrix:
- rank + nullity = n
- A full-rank matrix (rank = n) has nullity = 0 and is invertible
- A rank-deficient matrix (rank < n) has nullity > 0 and is singular

### Cryptographic Implications
- **Encryption**: Message is transformed by multiplying with the key matrix
- **Decryption**: Requires multiplying by the inverse of the key matrix
- **Singular Matrices**: Cannot be used for secure cryptography because:
  1. They have no inverse (making decryption mathematically impossible)
  2. They have non-zero nullity (causing information loss)
  3. Multiple different inputs map to the same output

## Project Goals
This demonstration helps viewers understand:
1. How matrix-based encryption works
2. Why invertible matrices are essential for cryptography
3. The relationship between matrix properties and information security
4. The practical implications of the Rank-Nullity Theorem

## References
- Strang, G. (2016). Introduction to Linear Algebra (5th ed.). Wellesley-Cambridge Press.
- Hoffstein, J., Pipher, J., & Silverman, J. H. (2014). An Introduction to Mathematical Cryptography. Springer.