from nltk.corpus import stopwords
stop_words = stopwords.words('english')

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *

from tkPDFViewer import tkPDFViewer as pdf
from pyresparser import ResumeParser
import warnings
from tkinter import ttk  # Add this at the top of your script
from tkinter import Tk, filedialog, messagebox
from tkinter import (
    Tk, 
    ttk,           # For Progressbar and other themed widgets
    filedialog,    # For file dialogs
    messagebox,    # For message boxes
    simpledialog   # For simple input dialogs
)
import tkinter as tk
from tkinter import ttk
from tkinter import HORIZONTAL  # Add this import

class ResumeParserApp:
    def __init__(self, root):
        self.frame = tk.Frame(root)  # Create frame first
        self.frame.pack()
        
        # Correct Progressbar initialization
        loading = ttk.Progressbar(
            self.frame, 
            orient=HORIZONTAL, 
            length=100, 
            mode='determinate'
        )
        loading.pack()

# Now you can use Progressbar
loading = ttk.Progressbar(self.frame, orient=HORIZONTAL, length=100, mode='determinate')

class ResumeParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Parser")
        self.root.geometry("800x600")
        
        # PDF File Path Variable
        self.pdf_path = tk.StringVar()
        
        # Create Layout
        self.create_widgets()
    
    def create_widgets(self):
        # File Selection Frame
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)
        
        # PDF Path Entry
        self.pdf_entry = tk.Entry(file_frame, textvariable=self.pdf_path, width=50)
        self.pdf_entry.pack(side=tk.LEFT, padx=5)
        
        # Browse Button
        browse_btn = tk.Button(
            file_frame, 
            text="Browse PDF", 
            command=self.open_pdf_file()
        )
        browse_btn.pack(side=tk.LEFT)
        
        # Scan Button
        scan_btn = tk.Button(
            file_frame, 
            text="Scan Resume", 
            command=self.scan_resume
        )
        scan_btn.pack(side=tk.LEFT, padx=5)
        
        # Results Display
        self.results_text = tk.Text(
            self.root, 
            height=15, 
            width=80
        )
        self.results_text.pack(pady=10)
    
    def open_pdf_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if file_path:
            self.pdf_path.set(file_path)
            
            # Optional: PDF Preview
            v1 = pdf.ShowPdf()
            v2 = v1.pdf_view(
                self.root, 
                pdf_location=file_path, 
                width=50, 
                height=100
            )
            v2.pack()
    
    def scan_resume(self):
        # Suppress warnings
        warnings.filterwarnings("ignore", category=UserWarning)
        
        pdf_file = self.pdf_path.get()
        
        if not pdf_file:
            messagebox.showerror("Error", "Please select a PDF file")
            return
        
        try:
            # Parse Resume
            data = ResumeParser(pdf_file).get_extracted_data()
            
            # Clear Previous Results
            self.results_text.delete(1.0, tk.END)
            
            # Display Results
            result_text = f"""
Resume Parsing Results:
---------------------
Name: {data.get('name', 'N/A')}
Email: {data.get('email', 'N/A')}
Skills: {', '.join(data.get('skills', ['N/A']))}
Total Experience: {data.get('total_experience', 'N/A')}
"""
            
            self.results_text.insert(tk.END, result_text)
        
        except Exception as e:
            messagebox.showerror("Error", f"Resume parsing failed: {str(e)}")

def main():
    root = tk.Tk()
    app = ResumeParserApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
