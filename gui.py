#!/usr/bin/env python3
"""
GUI module for the Cryptography & Nullity Demo
Contains the Tkinter interface for demonstrating why singular matrices 
fail in encoding/decoding messages in cryptography.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import os
import numpy as np
from algorithm import MatrixCrypto

class CryptographyDemoApp:
    """Main application class for the Cryptography & Nullity Demo"""
    
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root (tk.Tk): The root Tkinter window
        """
        self.root = root
        self.root.geometry('950x750')
        self.root.configure(padx=20, pady=20)
        
        # Add scrollbar to the main window
        main_container = ttk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas with scrollbar
        main_canvas = tk.Canvas(main_container)
        main_scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=main_canvas.yview)
        
        # Configure the canvas
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        main_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a frame inside the canvas
        self.scrollable_frame = ttk.Frame(main_canvas)
        scrollable_window = main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure the scrollable_frame to expand to fill canvas width
        def configure_scroll_region(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        
        def configure_window_size(event):
            main_canvas.itemconfig(scrollable_window, width=event.width)
            
        self.scrollable_frame.bind("<Configure>", configure_scroll_region)
        main_canvas.bind("<Configure>", configure_window_size)
        
        # Make mouse wheel work for scrolling
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Matrix crypto algorithm instance
        self.matrix_crypto = MatrixCrypto()
        
        # Set up the UI components
        self._setup_ui()
        
        # Initialize with default matrix
        self.update_matrix()
    
    def _setup_ui(self):
        """Set up the user interface components"""
        # Title
        title_label = ttk.Label(
            self.scrollable_frame, 
            text="Cryptography & Nullity: Why Singular Matrices Fail", 
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Main container frame
        main_frame = ttk.Frame(self.scrollable_frame)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Matrix selection and properties
        left_frame = ttk.LabelFrame(main_frame, text="Matrix Selection")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Matrix input frame
        matrix_frame = ttk.Frame(left_frame)
        matrix_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Labels for matrix
        ttk.Label(matrix_frame, text="Enter 2x2 Matrix:").pack(anchor=tk.W)
        
        # Matrix entry widgets
        matrix_entry_frame = ttk.Frame(matrix_frame)
        matrix_entry_frame.pack(pady=10)
        
        self.matrix_entries = []
        for i in range(2):
            row_entries = []
            for j in range(2):
                entry = ttk.Entry(matrix_entry_frame, width=8)
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)
        
        # Set default matrix values [3 5; 1 2]
        default_values = [[3, 5], [1, 2]]
        for i in range(2):
            for j in range(2):
                self.matrix_entries[i][j].insert(0, str(default_values[i][j]))
        
        # Matrix properties output
        ttk.Label(left_frame, text="Matrix Properties:").pack(anchor=tk.W, padx=10)
        properties_frame = ttk.Frame(left_frame)
        properties_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Add scrollbars to properties text
        prop_v_scroll = ttk.Scrollbar(properties_frame, orient=tk.VERTICAL)
        prop_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.properties_text = scrolledtext.ScrolledText(
            properties_frame, 
            width=40, 
            height=8, 
            wrap=tk.WORD,
            yscrollcommand=prop_v_scroll.set
        )
        self.properties_text.pack(fill=tk.BOTH, expand=True)
        prop_v_scroll.config(command=self.properties_text.yview)
        
        # Preset matrix buttons
        presets_frame = ttk.LabelFrame(left_frame, text="Preset Matrices")
        presets_frame.pack(pady=10, padx=10, fill=tk.X)
        
        preset_buttons = [
            ("Good Matrix", [[3, 5], [1, 2]]),
            ("Singular Matrix", [[1, 2], [2, 4]]),
            ("Not Invertible in Z26", [[2, 1], [3, 4]])
        ]
        
        for label, matrix in preset_buttons:
            button = ttk.Button(
                presets_frame,
                text=label,
                command=lambda m=matrix: self.load_preset(m)
            )
            button.pack(fill=tk.X, pady=5, padx=10)
        
        # Update matrix button
        update_button = ttk.Button(
            left_frame,
            text="Update Matrix",
            command=self.update_matrix
        )
        update_button.pack(fill=tk.X, pady=10, padx=10)
        
        # Right panel - Encryption and visualization
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Encryption panel
        encrypt_frame = ttk.LabelFrame(right_frame, text="Message Encryption/Decryption")
        encrypt_frame.pack(pady=(0, 10), fill=tk.X)
        
        # Message input
        ttk.Label(encrypt_frame, text="Enter Message (A-Z only):").pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.message_entry = ttk.Entry(encrypt_frame)
        self.message_entry.pack(fill=tk.X, padx=10, pady=5)
        self.message_entry.insert(0, "HELLO")
        
        # Encrypt/decrypt button
        encrypt_button = ttk.Button(
            encrypt_frame,
            text="Encrypt & Attempt to Decrypt",
            command=self.process_message
        )
        encrypt_button.pack(fill=tk.X, padx=10, pady=10)
        
        # Encryption results
        results_frame = ttk.Frame(encrypt_frame)
        results_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Add scrollbars to results text
        results_v_scroll = ttk.Scrollbar(results_frame, orient=tk.VERTICAL)
        results_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame, 
            width=40, 
            height=8, 
            wrap=tk.WORD,
            yscrollcommand=results_v_scroll.set
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        results_v_scroll.config(command=self.results_text.yview)
        
        # Visualization panel
        viz_frame = ttk.LabelFrame(right_frame, text="Matrix Transformation Visualization")
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            viz_frame, 
            text="This visualization shows how the matrix transforms a unit square in 2D space:",
            wraplength=400
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Create a frame with scrollbars for the visualization
        viz_scroll_frame = ttk.Frame(viz_frame)
        viz_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add vertical scrollbar
        viz_v_scroll = ttk.Scrollbar(viz_scroll_frame, orient=tk.VERTICAL)
        viz_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add horizontal scrollbar
        viz_h_scroll = ttk.Scrollbar(viz_scroll_frame, orient=tk.HORIZONTAL)
        viz_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Canvas for the visualization
        self.viz_canvas = tk.Canvas(
            viz_scroll_frame,
            bg='white',
            height=300,
            yscrollcommand=viz_v_scroll.set,
            xscrollcommand=viz_h_scroll.set
        )
        self.viz_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Configure the scrollbars
        viz_v_scroll.config(command=self.viz_canvas.yview)
        viz_h_scroll.config(command=self.viz_canvas.xview)
        
        # Explanation section
        explanation_frame = ttk.LabelFrame(self.scrollable_frame, text="Why Singular Matrices Fail in Cryptography")
        explanation_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        explanation_scroll_frame = ttk.Frame(explanation_frame)
        explanation_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add scrollbars
        explanation_v_scroll = ttk.Scrollbar(explanation_scroll_frame, orient=tk.VERTICAL)
        explanation_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        explanation_h_scroll = ttk.Scrollbar(explanation_scroll_frame, orient=tk.HORIZONTAL)
        explanation_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.explanation_text = scrolledtext.ScrolledText(
            explanation_scroll_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=10,
            yscrollcommand=explanation_v_scroll.set,
            xscrollcommand=explanation_h_scroll.set
        )
        self.explanation_text.pack(fill=tk.BOTH, expand=True)
        explanation_v_scroll.config(command=self.explanation_text.yview)
        explanation_h_scroll.config(command=self.explanation_text.xview)
        
        self.explanation_text.insert(tk.END, MatrixCrypto.get_explanation())
        self.explanation_text.config(state=tk.DISABLED)  # Make it read-only
    
    def load_preset(self, matrix):
        """
        Load a preset matrix into the entry fields.
        
        Args:
            matrix (list): A 2D list representing the matrix
        """
        # Clear the entries
        for i in range(2):
            for j in range(2):
                self.matrix_entries[i][j].delete(0, tk.END)
                self.matrix_entries[i][j].insert(0, str(matrix[i][j]))
        
        self.update_matrix()
    
    def update_matrix(self):
        """Update the matrix and all associated displays"""
        try:
            # Get matrix values from entries
            matrix = np.zeros((2, 2))
            for i in range(2):
                for j in range(2):
                    matrix[i, j] = float(self.matrix_entries[i][j].get())
            
            # Store the matrix
            self.current_matrix = matrix
            
            # Update matrix properties
            self._update_properties()
            
            # Update visualization
            self._update_visualization()
            
            # If there's a message, re-process it with the new matrix
            if self.message_entry.get():
                self.process_message()
                
        except ValueError:
            self.properties_text.delete(1.0, tk.END)
            self.properties_text.insert(tk.END, "Error: Please enter valid numbers for all matrix elements.")
    
    def _update_properties(self):
        """Update the matrix properties display"""
        properties = MatrixCrypto.check_matrix_properties(self.current_matrix)
        
        # Clear the text box
        self.properties_text.delete(1.0, tk.END)
        
        # Format the matrix
        matrix_str = f"[ {self.current_matrix[0,0]:.1f}  {self.current_matrix[0,1]:.1f} ]\n"
        matrix_str += f"[ {self.current_matrix[1,0]:.1f}  {self.current_matrix[1,1]:.1f} ]\n\n"
        
        # Add properties
        props_str = f"Determinant: {properties['determinant']:.2f}\n"
        props_str += f"Determinant mod 26: {properties['det_mod_26']}\n"
        
        # Add status indicators
        if properties['is_singular']:
            props_str += "\n⚠️ SINGULAR MATRIX ⚠️\n"
            props_str += "This matrix cannot be inverted!\n"
            props_str += "Decryption will be impossible.\n"
        elif not properties['invertible_mod_26']:
            props_str += f"\n⚠️ NOT INVERTIBLE IN Z26 ⚠️\n"
            props_str += f"GCD(det mod 26, 26) = {properties['gcd']} ≠ 1\n"
            props_str += "This matrix won't work with the Hill cipher.\n"
        else:
            props_str += "\n✅ VALID FOR HILL CIPHER ✅\n"
            props_str += "This matrix is invertible and works in Z26.\n"
        
        self.properties_text.insert(tk.END, matrix_str + props_str)
    
    def _update_visualization(self):
        """Update the matrix transformation visualization"""
        # Generate the visualization
        filename = "matrix_transformation.png"
        MatrixCrypto.visualize_matrix_transformation(self.current_matrix, filename)
        
        # Load and display the image
        if os.path.exists(filename):
            img = Image.open(filename)
            
            # Create the PhotoImage
            self.viz_photo = ImageTk.PhotoImage(img)
            
            # Clear canvas and display image
            self.viz_canvas.delete("all")
            self.viz_canvas.create_image(0, 0, image=self.viz_photo, anchor=tk.NW)
            
            # Configure the canvas scrolling region
            self.viz_canvas.config(
                scrollregion=self.viz_canvas.bbox("all"),
                width=min(600, self.viz_photo.width()),
                height=min(300, self.viz_photo.height())
            )
    
    def process_message(self):
        """Encrypt and attempt to decrypt the message with the current matrix"""
        message = self.message_entry.get().upper()
        if not message:
            return
        
        # Clear results
        self.results_text.delete(1.0, tk.END)
        
        try:
            # Encrypt message
            encrypted = MatrixCrypto.encrypt_message(message, self.current_matrix)
            
            # Try to decrypt
            decrypted = MatrixCrypto.decrypt_message(encrypted, self.current_matrix)
            
            # Display results
            results = f"Original message: {message}\n\n"
            results += f"Encrypted message: {encrypted}\n\n"
            results += f"Attempted decryption: {decrypted}\n\n"
            
            # Add interpretation
            if "ERROR" in decrypted:
                if "singular" in decrypted:
                    results += "Decryption failed because the matrix is singular (det = 0).\n"
                elif "Z26" in decrypted:
                    results += "Decryption failed because the matrix is not invertible in Z26.\n"
                else:
                    results += "Decryption failed. See error message above.\n"
            elif decrypted == message:
                results += "✅ Decryption successful! Original message recovered.\n"
            else:
                results += "⚠️ Decryption produced a different message than the original.\n"
                
            self.results_text.insert(tk.END, results)
            
        except Exception as e:
            self.results_text.insert(tk.END, f"Error processing message: {str(e)}")