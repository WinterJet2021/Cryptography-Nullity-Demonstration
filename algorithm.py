#!/usr/bin/env python3
"""
Algorithm module for the Cryptography & Nullity Demo
Contains the mathematical operations and algorithms for the Hill cipher
and matrix operations demonstrations.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving plots

class MatrixCrypto:
    """Class handling matrix operations and Hill cipher cryptography"""
    
    @staticmethod
    def is_singular(matrix):
        """Check if a matrix is singular by calculating its determinant."""
        return np.abs(np.linalg.det(matrix)) < 1e-10
    
    @staticmethod
    def encrypt_message(message, key_matrix):
        """
        Encrypt a message using the Hill cipher with a given key matrix.
        
        Args:
            message (str): The plaintext message to encrypt
            key_matrix (numpy.ndarray): The key matrix for encryption
            
        Returns:
            str: The encrypted message
        """
        # Convert message to numbers (A=0, B=1, ..., Z=25)
        message = message.upper()
        
        # Store the original message and positions of spaces for later reference
        original_message = message
        space_positions = [i for i, char in enumerate(message) if char == ' ']
        
        # Remove spaces and non-alphabetic characters for encryption
        message_nums = [ord(char) - ord('A') for char in message if char.isalpha()]
        
        # Pad message if necessary
        matrix_size = key_matrix.shape[0]
        if len(message_nums) % matrix_size != 0:
            message_nums += [0] * (matrix_size - len(message_nums) % matrix_size)
        
        # Reshape message into column vectors
        message_vectors = np.array(message_nums).reshape(-1, matrix_size)
        
        # Encrypt each vector
        cipher_vectors = []
        for vector in message_vectors:
            cipher_vector = np.dot(key_matrix, vector) % 26
            cipher_vectors.append(cipher_vector)
        
        # Convert encrypted numbers back to letters
        cipher_text = ''
        for vector in cipher_vectors:
            for num in vector:
                cipher_text += chr(int(num) + ord('A'))
        
        return cipher_text, space_positions, original_message
    
    @staticmethod
    def decrypt_message(cipher_text, key_matrix, space_positions=None, original_message=None):
        """
        Decrypt a message that was encrypted with the Hill cipher.
        
        Args:
            cipher_text (str): The encrypted message
            key_matrix (numpy.ndarray): The key matrix used for encryption
            space_positions (list, optional): Positions of spaces in the original message
            original_message (str, optional): The original message before encryption
            
        Returns:
            str: The decrypted message or an error message
        """
        # Try to calculate the inverse of the key matrix
        try:
            # For the modular inverse, we need to work in Z26
            det = round(np.linalg.det(key_matrix))
            det_mod_26 = det % 26
            
            # Check if determinant has a multiplicative inverse in Z26
            # This is only true if gcd(det_mod_26, 26) = 1
            if np.gcd(det_mod_26, 26) != 1:
                return "DECRYPTION ERROR: Key matrix is not invertible in Z26"
            
            # Calculate the modular multiplicative inverse of det_mod_26
            det_inv = 0
            for i in range(1, 26):
                if (det_mod_26 * i) % 26 == 1:
                    det_inv = i
                    break
            
            # Calculate the adjugate matrix
            matrix_size = key_matrix.shape[0]
            adjugate = np.zeros((matrix_size, matrix_size))
            
            for i in range(matrix_size):
                for j in range(matrix_size):
                    # Calculate the minor by removing row i and column j
                    minor = np.delete(np.delete(key_matrix, i, axis=0), j, axis=1)
                    adjugate[j, i] = (((-1)**(i+j)) * round(np.linalg.det(minor))) % 26
            
            # Calculate the modular inverse
            key_matrix_inv = (det_inv * adjugate) % 26
            
            # Convert cipher text to numbers
            cipher_text = cipher_text.upper()
            cipher_nums = [ord(char) - ord('A') for char in cipher_text if char.isalpha()]
            
            # Reshape cipher text into column vectors
            matrix_size = key_matrix.shape[0]
            cipher_vectors = np.array(cipher_nums).reshape(-1, matrix_size)
            
            # Decrypt each vector
            message_vectors = []
            for vector in cipher_vectors:
                message_vector = np.dot(key_matrix_inv, vector) % 26
                message_vectors.append(message_vector)
            
            # Convert decrypted numbers back to letters
            decrypted_message = ''
            for vector in message_vectors:
                for num in vector:
                    decrypted_message += chr(int(round(num)) % 26 + ord('A'))
            
            # Reinsert spaces if provided
            if space_positions and original_message:
                # Only insert spaces up to the length of the decrypted message
                # to avoid index errors if the decryption is not exact
                result_chars = list(decrypted_message)
                
                # Calculate how many alphabet characters are in the original message
                alpha_count = sum(1 for char in original_message if char.isalpha())
                
                # Only use spaces that would fall within the decrypted text
                valid_spaces = [pos for pos in space_positions if pos < alpha_count]
                
                # Insert spaces
                offset = 0
                for pos in valid_spaces:
                    if pos + offset < len(result_chars):
                        result_chars.insert(pos + offset, ' ')
                        offset += 1
                
                decrypted_message = ''.join(result_chars)
            
            return decrypted_message
        
        except np.linalg.LinAlgError:
            return "DECRYPTION ERROR: Matrix is singular (not invertible)"
        except Exception as e:
            return f"DECRYPTION ERROR: {str(e)}"
    
    @staticmethod
    def visualize_matrix_transformation(matrix, filename="matrix_transformation.png"):
        """
        Visualize how a matrix transforms a unit square in 2D space.
        
        Args:
            matrix (numpy.ndarray): The 2x2 transformation matrix
            filename (str): The filename to save the plot to
            
        Returns:
            str: The path to the saved plot
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        
        # Create a grid of points
        x = np.linspace(-1, 1, 11)
        y = np.linspace(-1, 1, 11)
        X, Y = np.meshgrid(x, y)
        
        # Plot the original grid
        ax1.set_title("Original Space")
        ax1.set_xlim(-2, 2)
        ax1.set_ylim(-2, 2)
        ax1.grid(True)
        ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        ax1.scatter(X, Y, color='blue', s=10)
        
        # Highlight unit square
        square_x = np.array([0, 1, 1, 0, 0])
        square_y = np.array([0, 0, 1, 1, 0])
        ax1.plot(square_x, square_y, 'r-', linewidth=2)
        
        # Apply the transformation to each point
        X_transformed = np.zeros_like(X)
        Y_transformed = np.zeros_like(Y)
        
        for i in range(len(x)):
            for j in range(len(y)):
                point = np.array([X[j, i], Y[j, i]])
                transformed = matrix @ point
                X_transformed[j, i] = transformed[0]
                Y_transformed[j, i] = transformed[1]
        
        # Transform the unit square
        square_points = np.vstack((square_x, square_y))
        transformed_square = matrix @ square_points
        
        # Plot the transformed grid
        det_value = np.linalg.det(matrix)
        ax2.set_title(f"Transformed Space (Det={det_value:.2f})")
        ax2.set_xlim(-2, 2)
        ax2.set_ylim(-2, 2)
        ax2.grid(True)
        ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        ax2.scatter(X_transformed, Y_transformed, color='green', s=10)
        ax2.plot(transformed_square[0], transformed_square[1], 'r-', linewidth=2)
        
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        
        return filename
    
    @staticmethod
    def check_matrix_properties(matrix):
        """
        Check the properties of a matrix for use in cryptography.
        
        Args:
            matrix (numpy.ndarray): The matrix to check
            
        Returns:
            dict: A dictionary of matrix properties
        """
        properties = {}
        
        # Calculate determinant
        determinant = np.linalg.det(matrix)
        properties['determinant'] = determinant
        
        # Check if matrix is singular
        properties['is_singular'] = MatrixCrypto.is_singular(matrix)
        
        # Check invertibility in Z26 (for Hill cipher)
        det_mod_26 = round(determinant) % 26
        properties['det_mod_26'] = det_mod_26
        
        # Check if the determinant has an inverse in Z26
        if det_mod_26 == 0:
            properties['invertible_mod_26'] = False
            properties['gcd'] = 0
        else:
            gcd = np.gcd(det_mod_26, 26)
            properties['gcd'] = gcd
            properties['invertible_mod_26'] = (gcd == 1)
        
        return properties
    
    @staticmethod
    def get_explanation():
        """
        Get a detailed explanation of why singular matrices fail in cryptography.
        
        Returns:
            str: A multiline explanation
        """
        explanation = """
WHY SINGULAR MATRICES FAIL IN CRYPTOGRAPHY
==========================================

1. MATHEMATICAL EXPLANATION:
   - A singular matrix has a determinant of zero.
   - Without a non-zero determinant, the matrix doesn't have an inverse.
   - In cryptography, we need the inverse matrix to decrypt messages.
   - Encryption: C = K × P (where C=ciphertext, K=key matrix, P=plaintext)
   - Decryption: P = K⁻¹ × C (requires K⁻¹, the inverse of K)
   - If K is singular, K⁻¹ doesn't exist, and decryption is impossible.

2. INFORMATION THEORY PERSPECTIVE:
   - Singular transformations compress higher-dimensional spaces into lower dimensions.
   - This creates an irreversible loss of information.
   - Multiple different messages would encrypt to the same ciphertext.
   - This violates a fundamental principle of encryption: uniqueness of decryption.

3. GEOMETRIC INTERPRETATION:
   - A matrix transformation can be visualized as mapping points in space.
   - A non-singular matrix maps the space to itself in a one-to-one manner.
   - A singular matrix collapses the space (e.g., maps a square to a line or a point).
   - Points that were distinct before encryption become indistinguishable.
   - In the visualization, a singular matrix flattens the grid pattern.

4. HILL CIPHER ADDITIONAL CONSTRAINT:
   - The Hill cipher works in modular arithmetic (modulo 26 for English alphabet).
   - Even if a matrix is non-singular (det ≠ 0), it needs a multiplicative inverse in Z26.
   - This is only possible when gcd(det mod 26, 26) = 1.
   - If the determinant shares any factors with 26 (which is 2 × 13), decryption fails.
   - Examples of problematic determinants: 2, 4, 13, 26 (any multiple of 2 or 13).

5. SUMMARY:
   - For a matrix to work in the Hill cipher:
     a) It must be non-singular (det ≠ 0)
     b) Its determinant must be coprime with 26 (gcd(det mod 26, 26) = 1)
   - These constraints ensure the encryption is properly reversible.
   - Singular matrices create a "many-to-one" mapping that destroys information.
        """
        return explanation