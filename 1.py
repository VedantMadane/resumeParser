# pip install pyresparser
# pip install spacy
# pip install nltk
# pip install tkinter

from tkinter import filedialog

from tkPDFViewer import tkPDFViewer as pdf
from pyresparser import ResumeParser

from nltk.corpus import stopwords
stop_words = stopwords.words('english')


import tkinter as tk
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
root = tk.Tk()
root.title("PDF Input Viewer")
root.geometry("600x800")

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Create button to open PDF
open_button = tk.Button(
    root, 
    text="Select PDF", 
    command=open_pdf_file()
)
open_button.pack()

root.mainloop()

def open_pdf_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]

    )
    if file_path:
        v1 = pdf.ShowPdf()
        v2 = v1.pdf_view(
            root,
            pdf_location=file_path,
            width=50,
            height=100
        )
        v2.pack()

data = ResumeParser(file_path).get_etracted_data()
