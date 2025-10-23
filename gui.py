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
        self.root.minsize(900, 700)
        
        # Make the window resizable
        self.root.resizable(True, True)

        # Create the main frame with a weight-based layout
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Make rows and columns resizable
        self.main_frame.rowconfigure(0, weight=0)  # Title section (fixed)
        self.main_frame.rowconfigure(1, weight=0)  # Separator (fixed)
        self.main_frame.rowconfigure(2, weight=1)  # Matrix section (can expand)
        self.main_frame.rowconfigure(3, weight=0)  # Message section (fixed)
        self.main_frame.rowconfigure(4, weight=4)  # Results section (expands most)
        self.main_frame.rowconfigure(5, weight=1)  # Summary section (can expand)
        self.main_frame.columnconfigure(0, weight=1)
        
        # Add a PanedWindow for flexible resizing
        self.main_paned = ttk.PanedWindow(self.main_frame, orient=tk.VERTICAL)
        self.main_paned.grid(row=0, column=0, rowspan=6, sticky="nsew")

        # Create UI elements
        self.create_title_section()
        self.create_matrix_section()
        self.create_message_section()
        self.create_results_section()
        self.create_summary_section()

        # Initially run with default settings
        self.update_matrix_display()
        self.run_encryption()

    # -------------------------------------------------------------------------
    # UI Construction Sections
    # -------------------------------------------------------------------------

    def create_title_section(self):
        """Create the title and description section."""
        title_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(title_frame, weight=0)

        ttk.Label(
            title_frame,
            text="Why Singular Matrices Fail in Cryptography",
            font=("Arial", 18, "bold")
        ).pack(pady=(5, 0))

        ttk.Label(
            title_frame,
            text="This demonstration explores how matrix properties affect cryptographic security",
            font=("Arial", 12, "italic")
        ).pack(pady=5)

        ttk.Separator(title_frame, orient='horizontal').pack(fill=tk.X, pady=5)

    def create_matrix_section(self):
        """Create the matrix selection and visualization section."""
        matrix_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(matrix_frame, weight=1)
        
        # Add a horizontal paned window for adjustable panels
        matrix_paned = ttk.PanedWindow(matrix_frame, orient=tk.HORIZONTAL)
        matrix_paned.pack(fill=tk.BOTH, expand=True, pady=5)

        # Matrix selection
        control_frame = ttk.LabelFrame(matrix_paned, text="Matrix Selection")
        matrix_paned.add(control_frame, weight=0)

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

        # Custom matrix option
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
        visual_frame = ttk.LabelFrame(matrix_paned, text="Matrix Visualization")
        matrix_paned.add(visual_frame, weight=1)

        self.matrix_fig = Figure(figsize=(4, 4))
        self.matrix_ax = self.matrix_fig.add_subplot(111)
        self.matrix_canvas = FigureCanvasTkAgg(self.matrix_fig, visual_frame)
        self.matrix_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Matrix properties
        props_frame = ttk.LabelFrame(matrix_paned, text="Matrix Properties")
        matrix_paned.add(props_frame, weight=1)
        
        # Add scrollbar to properties text
        props_scroll = ttk.Scrollbar(props_frame)
        props_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.props_text = tk.Text(props_frame, width=30, height=15, wrap=tk.WORD,
                                  yscrollcommand=props_scroll.set)
        self.props_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        props_scroll.config(command=self.props_text.yview)

    def create_message_section(self):
        """Create the message input section."""
        message_frame = ttk.LabelFrame(self.main_paned, text="Message Settings")
        self.main_paned.add(message_frame, weight=0)

        message_inner_frame = ttk.Frame(message_frame)
        message_inner_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        message_inner_frame.columnconfigure(1, weight=1)  # Make entry expand
        
        ttk.Label(message_inner_frame, text="Message to encrypt:").grid(row=0, column=0, padx=5, pady=5)

        self.message_var = tk.StringVar(value="HELLO WORLD")
        ttk.Entry(
            message_inner_frame,
            textvariable=self.message_var,
            width=40
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(
            message_inner_frame,
            text="Run Encryption",
            command=self.run_encryption
        ).grid(row=0, column=2, padx=5, pady=5)

    def create_results_section(self):
        """Create the results visualization section."""
        results_frame = ttk.LabelFrame(self.main_paned, text="Encryption Results")
        self.main_paned.add(results_frame, weight=4)  # This pane gets more space
        
        # Create a notebook for tabbed results display
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Graph visualization
        graph_tab = ttk.Frame(self.results_notebook)
        self.results_notebook.add(graph_tab, text="Graph Visualization")
        
        self.result_fig = Figure(figsize=(10, 6))
        self.result_ax = self.result_fig.add_subplot(111)
        self.result_canvas = FigureCanvasTkAgg(self.result_fig, graph_tab)
        self.result_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Tab 2: Detailed text results with proper scrolling
        text_tab = ttk.Frame(self.results_notebook)
        self.results_notebook.add(text_tab, text="Detailed Results")
        
        # Add scrollbar to the text widget
        result_scroll = ttk.Scrollbar(text_tab)
        result_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(text_tab, wrap=tk.WORD, yscrollcommand=result_scroll.set)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        result_scroll.config(command=self.result_text.yview)
        
        # Configure text tags
        self.result_text.tag_configure("header", font=("Arial", 12, "bold"))
        self.result_text.tag_configure("subheader", font=("Arial", 10, "bold"))
        self.result_text.tag_configure("good", foreground="green")
        self.result_text.tag_configure("bad", foreground="red")
        self.result_text.tag_configure("data", font=("Courier", 10))

    def create_summary_section(self):
        """Create an expandable summary section at the bottom."""
        summary_frame = ttk.LabelFrame(self.main_paned, text="Summary")
        self.main_paned.add(summary_frame, weight=1)  # This can be expanded by user
        
        # Add scrollbar to summary text
        summary_scroll = ttk.Scrollbar(summary_frame)
        summary_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.summary_text = tk.Text(summary_frame, height=4, wrap=tk.WORD,
                                   yscrollcommand=summary_scroll.set)
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        summary_scroll.config(command=self.summary_text.yview)
        
        # Add resize handle hint (visual indicator)
        resize_hint = ttk.Label(summary_frame, text="↕ Drag to resize", font=("Arial", 7, "italic"))
        resize_hint.place(relx=0.5, rely=0, anchor="n")

    # -------------------------------------------------------------------------
    # Logic & Event Handlers
    # -------------------------------------------------------------------------

    def update_matrix_display(self):
        """Update the matrix visualization based on current selection."""
        # Only set from presets if not custom
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
            self.run_encryption()  # Automatically run encryption with new matrix

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for all matrix elements.")

    def run_encryption(self):
        """Run the encryption process and update the results."""
        message = self.message_var.get()
        result = self.crypto.encrypt_message(message)

        # Update graph visualization
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

        # Update detailed text results
        self.result_text.delete(1.0, tk.END)
        
        # Original message section
        self.result_text.insert(tk.END, "ORIGINAL MESSAGE DETAILS\n", "header")
        self.result_text.insert(tk.END, f"Message: {result['original_message']}\n")
        self.result_text.insert(tk.END, f"Padded message: {result['padded_message']}\n")
        self.result_text.insert(tk.END, "Numeric representation: \n", "subheader")
        
        # Format message vectors nicely
        for i, vector in enumerate(result['message_vectors']):
            vector_str = ', '.join([f"{int(val):2d}" for val in vector])
            self.result_text.insert(tk.END, f"Vector {i+1}: [{vector_str}]\n", "data")
        
        # Encryption section
        self.result_text.insert(tk.END, "\nENCRYPTION DETAILS\n", "header")
        self.result_text.insert(tk.END, "Encryption formula: Y = MX where M is the matrix\n")
        self.result_text.insert(tk.END, "Encrypted vectors:\n", "subheader")
        
        # Format encrypted vectors nicely
        for i, vector in enumerate(result['encrypted_vectors']):
            vector_str = ', '.join([f"{val:5.2f}" for val in vector])
            self.result_text.insert(tk.END, f"Vector {i+1}: [{vector_str}]\n", "data")
            
        # Decryption section
        self.result_text.insert(tk.END, "\nDECRYPTION ATTEMPT\n", "header")
        
        if result.get('decryption_success', False):
            self.result_text.insert(tk.END, "DECRYPTION SUCCESSFUL\n", "good")
            self.result_text.insert(tk.END, "Decryption formula: X = M⁻¹Y where M⁻¹ is the matrix inverse\n")
            self.result_text.insert(tk.END, "Decrypted vectors:\n", "subheader")
            
            # Format decrypted vectors
            for i, vector in enumerate(result['decrypted_vectors']):
                vector_str = ', '.join([f"{int(val):2d}" for val in vector])
                self.result_text.insert(tk.END, f"Vector {i+1}: [{vector_str}]\n", "data")
                
            self.result_text.insert(tk.END, f"\nDecrypted message: {result['decrypted_message']}\n", "good")
            
        else:
            self.result_text.insert(tk.END, f"{result.get('error_message', 'DECRYPTION FAILED')}\n", "bad")
            self.result_text.insert(tk.END, "\nExplanation: A singular matrix (determinant = 0) cannot be inverted.\n")
            self.result_text.insert(tk.END, "When a matrix has nullity > 0, information is lost during encryption.\n")
            self.result_text.insert(tk.END, "Multiple inputs map to the same output, making decryption impossible.\n")

        # Update summary text
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.tag_configure("good", foreground="green")
        self.summary_text.tag_configure("bad", foreground="red")
        
        summary = f"Original message: {result['original_message']}\n"
        
        encrypted_str = ", ".join([f"{val:.1f}" for val in result['encrypted_values'][:6]])
        if len(result['encrypted_values']) > 6:
            encrypted_str += ", ..."
        summary += f"Encrypted values: {encrypted_str}\n"

        if result.get('decryption_success', False):
            summary += f"Decrypted message: {result['decrypted_message']}\n"
            self.summary_text.insert(tk.END, summary)
            self.summary_text.insert(tk.END, "✓ Matrix is invertible. Encryption is secure and reversible.", "good")
        else:
            self.summary_text.insert(tk.END, summary)
            self.summary_text.insert(tk.END, "❌ Matrix is singular. Decryption is impossible due to information loss.", "bad")