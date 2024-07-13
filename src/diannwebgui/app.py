import streamlit as st
import pandas as pd
import numpy as np

def input():
     st.title("THIS PAGE IS NO LONGER BEING USED")
     fileupload1 = st.file_uploader(label="Raw", type=[".raw", ".wiff", ".mzML", ".dia"])
     fileupload2 = st.file_uploader(label=".d (DIA)", type=".d")

     fileupload3 = st.file_uploader(label="Spectral library", type=[".txt", ".csv", ".tsv", ".xls", ".speclib", ".sptxt", ".msp"])
     fileupload4 = st.file_uploader(label="Add FASTA", type=[".fasta", ".fa", ".speclib"], accept_multiple_files=True)

     checkbox1 = st.checkbox("Reannotate", value=False)
     checkbox2 = st.checkbox("Contaminants", value=False)

     fileupload5 = st.file_uploader(label="DIA-NN.exe", type=".exe")
     text1 = st.text_input("Path (Optional):", value="diann.exe")

def output():
     st.title("Output")
     checkbox1 = st.checkbox("Use existing .quant files when available", value=False)
     fileupload1 = st.file_uploader(label="Main output", type=".tsv")
     text1 = st.text_input("Path (Optional):", value="C:\DIA-NN\\1.9\\report.tsv")
     fileupload2 = st.file_uploader(label="Temp/.dia dir", type=".d")
     text2 = st.text_input("Path (Optional):")

     checkbox2 = st.checkbox("Generate spectral library", value=False)
     checkbox3 = st.checkbox("Quantities matrices", value=True)

     fileupload3 = st.file_uploader(label="Output library", type=".tsv")

     checkbox4 = st.checkbox("Generate Prosit input from FASTA or spectral library", value=False)
     number1 = st.number_input("Precursor FDR (%):", min_value=0, max_value=100, value=1)
     number2 = st.number_input("Threads:", min_value=0, max_value=100, value=4)
     number3 = st.number_input("Log level:", min_value=0, max_value=100, value=1)

     checkbox5 = st.checkbox("PDF", value=False)
     checkbox6 = st.checkbox("XICs", value=False)

     text3 = st.text_input("Additional options:")

def precursor_ion_generation():
     st.title("Precursor Ion Generation")

     checkbox1 = st.checkbox("FASTA digest for library-free search / library generation", value=False)
     checkbox2 = st.checkbox("Deep learning-based spectra, RTs, and IMs prediction", value=False)

     dropdown1 = st.selectbox("Protease:", options=["Trypsin/P", "Trypsin", "Lys-C", "Chymotrypsin", "AspN", "GluC"])

     number1 = st.number_input("Missed cleavages:", min_value=0, max_value=100, value=1)
     number2 = st.number_input("Maximum number of variable modifications:", min_value=0, max_value=100, value=0)

     checkbox3 = st.checkbox("N-term M excision", value=True)
     checkbox4 = st.checkbox("C carbamidomethylation", value=True)
     checkbox5 = st.checkbox("Ox(M)", value=False)
     checkbox6 = st.checkbox("Ac(N-term)", value=False)
     checkbox7 = st.checkbox("Phospho", value=False)
     checkbox8 = st.checkbox("K-GG", value=False)

def algorithm():
     st.title("Algorithm")

     number1 = st.number_input("Mass accuracy:", min_value=0, max_value=100, value=0)
     number2 = st.number_input("MS1 accuracy:", min_value=0, max_value=100, value=0)
     number3 = st.number_input("Scan window:", min_value=0, max_value=100, value=0)

     checkbox1 = st.checkbox("Unrelated runs", value=False)
     checkbox2 = st.checkbox("Peptidoforms", value=False)
     checkbox3 = st.checkbox("MBR", value=False)

     checkbox4 = st.checkbox("Heuristic protein interface", value=True)
     checkbox5 = st.checkbox("No shared spectra", value=True)

     dropdown1 = st.selectbox("Protein inference:", options=["Genes", "Isoform IDs", "Protein names (from FASTA)", "Genes (species-specific)", "Off"])
     dropdown1 = st.selectbox("Neural network classifier:", options=["Single-pass mode", "Off", "Double-pass mode"])

if __name__ == "__main__":
    input()
    output()
    precursor_ion_generation()
    algorithm()

# tabs = ["Input", "Output", "Precursor Ion Generation", "Algorithm"]
#
# selected_tab = st.sidebar.selectbox("Select a Tab:", tabs)
#
# if selected_tab == "Input":
#      input()
#
# elif selected_tab == "Output":
#      output()
#
# elif selected_tab == "Precursor Ion Generation":
#      precursor_ion_generation()
#
# elif selected_tab == "Algorithm":
#      algorithm()

