"""
GUI module for the Cryptography & Nullity demonstration.
This module handles the Tkinter interface and visualization.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class CryptographyApp:
    """
    Main application class that handles the UI.
    """

    def __init__(self, root, crypto_model):
        """
        Initialize the application.

        Args:
            root (tk.Tk): The root Tkinter window
            crypto_model (MatrixCrypto): The matrix crypto model
        """
        self.root = root
        self.crypto = crypto_model

        # Set window size and properties
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # Create the main frame
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create UI elements
        self.create_title_section()
        self.create_matrix_section()
        self.create_message_section()
        self.create_results_section()

        # Initially run with default settings
        self.update_matrix_display()
        self.run_encryption()

    # -------------------------------------------------------------------------
    # UI Construction Sections
    # -------------------------------------------------------------------------

    def create_title_section(self):
        """Create the title and description section."""
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=10)

        ttk.Label(
            title_frame,
            text="Why Singular Matrices Fail in Cryptography",
            font=("Arial", 18, "bold")
        ).pack()

        ttk.Label(
            title_frame,
            text="This demonstration explores how matrix properties affect cryptographic security",
            font=("Arial", 12, "italic")
        ).pack(pady=5)

        ttk.Separator(self.main_frame, orient='horizontal').pack(fill=tk.X, pady=10)

    def create_matrix_section(self):
        """Create the matrix selection and visualization section."""
        matrix_frame = ttk.Frame(self.main_frame)
        matrix_frame.pack(fill=tk.X, pady=10)

        # Matrix selection
        control_frame = ttk.LabelFrame(matrix_frame, text="Matrix Selection")
        control_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)

        self.matrix_type = tk.StringVar(value="good")

        ttk.Radiobutton(
            control_frame,
            text="Invertible Matrix (Good for Encryption)",
            variable=self.matrix_type,
            value="good",
            command=self.update_matrix_display
        ).pack(anchor=tk.W, pady=5)

        ttk.Radiobutton(
            control_frame,
            text="Singular Matrix (Bad for Encryption)",
            variable=self.matrix_type,
            value="bad",
            command=self.update_matrix_display
        ).pack(anchor=tk.W, pady=5)

        # NEW: Custom matrix option
        ttk.Radiobutton(
            control_frame,
            text="Custom Matrix (Use the 3×3 below)",
            variable=self.matrix_type,
            value="custom",
            command=self.update_matrix_display
        ).pack(anchor=tk.W, pady=5)

        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        ttk.Label(control_frame, text="Custom 3x3 Matrix:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)

        # Create a frame for the matrix input fields
        matrix_input_frame = ttk.Frame(control_frame)
        matrix_input_frame.pack(pady=5)

        # Create 3x3 grid of entry fields
        self.matrix_entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = ttk.Entry(matrix_input_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

        # Add apply button
        ttk.Button(
            control_frame,
            text="Apply Custom Matrix",
            command=self.apply_custom_matrix
        ).pack(pady=10)

        # Matrix visualization
        visual_frame = ttk.LabelFrame(matrix_frame, text="Matrix Visualization")
        visual_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        self.matrix_fig = Figure(figsize=(4, 4))
        self.matrix_ax = self.matrix_fig.add_subplot(111)
        self.matrix_canvas = FigureCanvasTkAgg(self.matrix_fig, visual_frame)
        self.matrix_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Matrix properties
        props_frame = ttk.LabelFrame(matrix_frame, text="Matrix Properties")
        props_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        self.props_text = tk.Text(props_frame, width=30, height=15, wrap=tk.WORD)
        self.props_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_message_section(self):
        """Create the message input section."""
        message_frame = ttk.LabelFrame(self.main_frame, text="Message Settings")
        message_frame.pack(fill=tk.X, pady=10)

        ttk.Label(message_frame, text="Message to encrypt:").pack(side=tk.LEFT, padx=5)

        self.message_var = tk.StringVar(value="HELLO WORLD")
        ttk.Entry(
            message_frame,
            textvariable=self.message_var,
            width=40
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            message_frame,
            text="Run Encryption",
            command=self.run_encryption
        ).pack(side=tk.LEFT, padx=20)

    def create_results_section(self):
        """Create the results visualization section."""
        results_frame = ttk.LabelFrame(self.main_frame, text="Encryption Results")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.result_fig = Figure(figsize=(10, 6))
        self.result_ax = self.result_fig.add_subplot(111)
        self.result_canvas = FigureCanvasTkAgg(self.result_fig, results_frame)
        self.result_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        text_frame = ttk.Frame(self.main_frame)
        text_frame.pack(fill=tk.X, pady=5)
        self.result_text = tk.Text(text_frame, height=5, wrap=tk.WORD)
        self.result_text.pack(fill=tk.X, expand=True, padx=5)

    # -------------------------------------------------------------------------
    # Logic & Event Handlers
    # -------------------------------------------------------------------------

    def update_matrix_display(self):
        """Update the matrix visualization based on current selection."""
        # NEW: Only set from presets if not custom
        if self.matrix_type.get() in ("good", "bad"):
            matrix = self.crypto.set_matrix(self.matrix_type.get())
        else:
            matrix = self.crypto.current_matrix

        props = self.crypto.get_matrix_properties()

        self.matrix_ax.clear()
        cmap = plt.cm.coolwarm
        im = self.matrix_ax.imshow(matrix, cmap=cmap)

        for i in range(3):
            for j in range(3):
                value = matrix[i, j]
                self.matrix_ax.text(
                    j, i, f"{value:.1f}",
                    ha="center", va="center",
                    color="white" if abs(value) > 1.5 else "black"
                )

        if props['is_invertible']:
            self.matrix_ax.set_title("Invertible Matrix (Good for Encryption)")
        else:
            self.matrix_ax.set_title("Singular Matrix (Bad for Encryption)")

        self.matrix_canvas.draw()
        self.update_properties_display(props)

        # Update custom entry boxes
        for i in range(3):
            for j in range(3):
                self.matrix_entries[i][j].delete(0, tk.END)
                self.matrix_entries[i][j].insert(0, f"{matrix[i, j]}")

    def update_properties_display(self, props):
        """Update the matrix properties display."""
        self.props_text.delete(1.0, tk.END)
        self.props_text.tag_configure("title", font=("Arial", 10, "bold"))
        self.props_text.tag_configure("good", foreground="green")
        self.props_text.tag_configure("bad", foreground="red")
        self.props_text.tag_configure("normal", font=("Arial", 10))

        self.props_text.insert(tk.END, "Matrix Properties:\n", "title")
        self.props_text.insert(tk.END, f"Determinant: {props['determinant']:.4f}\n", "normal")
        self.props_text.insert(tk.END, f"Rank: {props['rank']}\n", "normal")
        self.props_text.insert(tk.END, f"Nullity: {props['nullity']}\n", "normal")

        if props['is_invertible']:
            self.props_text.insert(tk.END, "Invertible: Yes\nSingular: No\n", "good")
        else:
            self.props_text.insert(tk.END, "Invertible: No\nSingular: Yes\n", "bad")

        self.props_text.insert(tk.END, "\nSecurity Assessment:\n", "title")

        if props['is_invertible']:
            self.props_text.insert(tk.END, "✓ SECURE - Can encrypt and decrypt\n", "good")
            self.props_text.insert(tk.END, "✓ No information loss\n", "good")
            self.props_text.insert(tk.END, "✓ Each output uniquely identifies input\n", "good")
        else:
            self.props_text.insert(tk.END, "❌ NOT SECURE - Cannot decrypt\n", "bad")
            self.props_text.insert(tk.END, "❌ Information is lost\n", "bad")
            self.props_text.insert(tk.END, "❌ Multiple inputs map to same output\n", "bad")

        self.props_text.insert(tk.END, "\nMathematical Process:\n", "title")

        if props['is_invertible']:
            self.props_text.insert(tk.END,
                "Encryption: Y = MX\nDecryption: X = M⁻¹Y\nMatrix is invertible.\n",
                "normal")
        else:
            self.props_text.insert(tk.END,
                "Encryption: Y = MX\nDecryption: X = M⁻¹Y (IMPOSSIBLE)\nMatrix has no inverse.\n",
                "normal")

    def apply_custom_matrix(self):
        """Apply a custom matrix from the entry fields."""
        try:
            values = []
            for i in range(3):
                for j in range(3):
                    value = float(self.matrix_entries[i][j].get())
                    values.append(value)

            custom_matrix = np.array(values).reshape(3, 3)
            self.crypto.current_matrix = custom_matrix

            # NEW: select custom mode so display won't overwrite
            self.matrix_type.set("custom")
            self.update_matrix_display()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for all matrix elements.")

    def run_encryption(self):
        """Run the encryption process and update the results."""
        message = self.message_var.get()
        result = self.crypto.encrypt_message(message)

        self.result_ax.clear()
        x = np.arange(len(result['message_nums']))
        self.result_ax.plot(x, result['message_nums'], 'o-', label='Original')
        self.result_ax.plot(x, result['encrypted_values'], 'o-', label='Encrypted')

        if result.get('decryption_success', False):
            self.result_ax.plot(x, result['decrypted_values'], 'o-', label='Decrypted')

        self.result_ax.set_xlabel('Character Position')
        self.result_ax.set_ylabel('Value')
        self.result_ax.grid(True)
        self.result_ax.legend()

        if result.get('decryption_success', False):
            self.result_ax.set_title("Encryption Results - DECRYPTION SUCCESSFUL", color="green")
        else:
            self.result_ax.set_title("Encryption Results - DECRYPTION FAILED", color="red")

        self.result_fig.tight_layout()
        self.result_canvas.draw()

        # Text result output
        self.result_text.delete(1.0, tk.END)
        self.result_text.tag_configure("good", foreground="green")
        self.result_text.tag_configure("bad", foreground="red")

        self.result_text.insert(tk.END, f"Original message: {result['original_message']}\n")

        encrypted_str = ", ".join([f"{val:.1f}" for val in result['encrypted_values'][:6]])
        if len(result['encrypted_values']) > 6:
            encrypted_str += ", ..."
        self.result_text.insert(tk.END, f"Encrypted values: {encrypted_str}\n")

        if result.get('decryption_success', False):
            self.result_text.insert(tk.END, f"Decrypted message: {result['decrypted_message']}\n", "good")
            self.result_text.insert(tk.END, "\nExplanation: The matrix is invertible (det ≠ 0). Information is preserved.")
        else:
            self.result_text.insert(tk.END, f"{result.get('error_message', 'Decryption failed')}\n", "bad")
            self.result_text.insert(tk.END, "\nExplanation: The matrix is singular (det = 0). Nullity > 0 ⇒ information lost.")