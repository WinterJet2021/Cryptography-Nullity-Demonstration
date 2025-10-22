"""
MatrixCrypto module for the Cryptography & Nullity demonstration.
This module handles all the matrix operations and cryptography logic.
"""

import numpy as np

class MatrixCrypto:
    """
    Class that handles matrix operations and cryptography functions.
    """
    
    def __init__(self):
        """
        Initialize the MatrixCrypto class with default matrices and mappings.
        """
        # Define the good matrix (invertible, determinant ≠ 0)
        self.good_matrix = np.array([
            [2, 1, 1],
            [1, 2, 0],
            [0, 1, 2]
        ])
        
        # Define the bad matrix (singular, determinant = 0)
        self.bad_matrix = np.array([
            [1, 2, 3],
            [2, 4, 6],
            [0, 1, 2]
        ])
        
        # Current matrix selection
        self.current_matrix = self.good_matrix
        
        # Character mappings for encryption/decryption
        self.char_to_num = {' ': 0}
        self.num_to_char = {0: ' '}
        for i in range(26):
            self.char_to_num[chr(65+i)] = i+1  # A=1, B=2, etc.
            self.num_to_char[i+1] = chr(65+i)  # 1=A, 2=B, etc.
    
    def set_matrix(self, matrix_type):
        """
        Set the current matrix to use for encryption/decryption.
        
        Args:
            matrix_type (str): 'good' for invertible or 'bad' for singular
        """
        if matrix_type.lower() == 'good':
            self.current_matrix = self.good_matrix
        else:
            self.current_matrix = self.bad_matrix
        
        return self.current_matrix
    
    def get_matrix_properties(self):
        """
        Calculate and return the properties of the current matrix.
        
        Returns:
            dict: Dictionary containing matrix properties
        """
        matrix = self.current_matrix
        det = np.linalg.det(matrix)
        rank = np.linalg.matrix_rank(matrix)
        nullity = matrix.shape[0] - rank
        is_singular = abs(det) < 1e-10
        
        return {
            'matrix': matrix,
            'determinant': det,
            'rank': rank,
            'nullity': nullity,
            'is_singular': is_singular,
            'is_invertible': not is_singular
        }
    
    def encrypt_message(self, message):
        """
        Encrypt a message using the current matrix.
        
        Args:
            message (str): Message to encrypt
        
        Returns:
            dict: Dictionary containing encryption results
        """
        # Process the message
        message = message.upper()
        original_message = message
        matrix_size = self.current_matrix.shape[0]
        
        # Pad message if needed
        if len(message) % matrix_size != 0:
            message = message + ' ' * (matrix_size - len(message) % matrix_size)
        
        # Convert to numbers
        message_nums = [self.char_to_num.get(char, 0) for char in message]
        
        # Group into vectors
        message_vectors = np.array(message_nums).reshape(-1, matrix_size)
        
        # Encrypt
        encrypted_vectors = np.zeros_like(message_vectors, dtype=float)
        for i in range(message_vectors.shape[0]):
            encrypted_vectors[i] = np.dot(self.current_matrix, message_vectors[i])
        
        # Create result dictionary
        result = {
            'original_message': original_message,
            'padded_message': message,
            'message_nums': message_nums,
            'message_vectors': message_vectors,
            'encrypted_vectors': encrypted_vectors,
            'encrypted_values': encrypted_vectors.flatten()
        }
        
        # Try to decrypt
        try:
            # Calculate inverse
            matrix_inverse = np.linalg.inv(self.current_matrix)
            
            # Decrypt
            decrypted_vectors = np.zeros_like(encrypted_vectors)
            for i in range(encrypted_vectors.shape[0]):
                decrypted_vectors[i] = np.round(np.dot(matrix_inverse, encrypted_vectors[i]))
            
            # Convert back to text
            decrypted_message = ""
            for row in decrypted_vectors:
                for num in row:
                    decrypted_message += self.num_to_char.get(int(num), '?')
            
            result['decryption_success'] = True
            result['decrypted_vectors'] = decrypted_vectors
            result['decrypted_values'] = decrypted_vectors.flatten()
            result['decrypted_message'] = decrypted_message
            
        except np.linalg.LinAlgError as e:
            result['decryption_success'] = False
            result['error_message'] = f"DECRYPTION FAILED: {e}"
        
        return result
    
    def get_custom_matrix(self, matrix_values):
        """
        Create a custom matrix from provided values.
        
        Args:
            matrix_values (list): List of 9 values for a 3x3 matrix
        
        Returns:
            numpy.ndarray: The custom matrix
        """
        try:
            # Convert to floats and reshape to 3x3
            values = [float(val) for val in matrix_values]
            matrix = np.array(values).reshape(3, 3)
            return matrix
        except:
            # Return the good matrix as a fallback
            return self.good_matrix