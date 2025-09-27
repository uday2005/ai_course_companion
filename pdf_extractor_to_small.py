import os
from pypdf import PdfReader, PdfWriter

# --- 1. CONFIGURE YOUR SCRIPT HERE ---

# The path to your large, single PDF file.
INPUT_PDF_PATH = "Deep_Learning_book.pdf"  # <-- Make sure this filename is correct!

# The directory where you want to save the split chapter PDFs.
OUTPUT_DIRECTORY = "data/book"

# !!! IMPORTANT !!!
# You MUST fill this list out by looking at your PDF's table of contents.
# The format is: ( "Name for the output file", start_page, end_page )
# Page numbers are INCLUSIVE. Use the numbers you see in your PDF viewer.
CHAPTERS = [
    ("01_Introduction", 27, 80),
    ("02_From_Model_to_Production", 81, 116),
    ("03_Data_Ethics", 117 , 152),
    ("04_Under the Hood: Training a Digit Classifier", 157 , 208),
    ("05_Image_Classification" , 209 , 241),
    ("06_Other_Computer_vision_problems" , 243, 262),
    ("07_Training_A_State_of_Art_Model" , 263 , 276),
    ("08_Collaborative_Filtering_Deep_Dive" , 277 , 300),
    ("09_Tabular_Modelling_Deep_Dive" , 301 , 351),
    ("10_NLP_Deep_dives: RNNs" , 353 , 378),
    ("11_Data_Munging_with_fastai's Mid Level API" , 379 , 393),
    ("12_A_Language_Model_from_scratch" ,397 , 426),
    ("13_Convolutional_Neural_Network" , 427 , 464),
    ("14_ResNets" , 465 , 481),
    ("15_Application Architectures Deep Dive" , 483 , 494),
    ("16_The_training_process" ,495 , 514),
    ("17_A_Neural_Network_from_foundations" , 517 , 541),
    ("18_CNN Interpretation with CAM" ,543 , 549),
    ("19_A fastai Learner from Scratch " , 551 , 568),

    



    # ("04_The_Training_Process", 92, 120),  <-- ADD THE REST OF YOUR CHAPTERS HERE
]


# --- 2. THE SCRIPT LOGIC (You don't need to change this) ---

def split_pdf_by_chapters():
    """
    Reads a large PDF and splits it into multiple smaller PDFs based on the
    chapter definitions in the CHAPTERS list.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    print(f"Output directory '{OUTPUT_DIRECTORY}' is ready.")

    try:
        # Open the source PDF file
        with open(INPUT_PDF_PATH, "rb") as infile:
            reader = PdfReader(infile)
            print(f"Successfully opened '{INPUT_PDF_PATH}'. It has {len(reader.pages)} pages.")

            # Process each chapter defined in the list
            for name, start_page, end_page in CHAPTERS:
                writer = PdfWriter()
                output_filename = os.path.join(OUTPUT_DIRECTORY, f"{name}.pdf")

                print(f"  -> Processing '{name}' (Pages {start_page}-{end_page})...")

                # Add pages from the source PDF to the new PDF
                for page_num in range(start_page - 1, end_page):
                    # pypdf is 0-indexed, so we subtract 1 from the page numbers
                    if page_num < len(reader.pages):
                        writer.add_page(reader.pages[page_num])
                    else:
                        print(f"      Warning: Page {page_num + 1} is out of range. Skipping.")

                # Save the new PDF file
                with open(output_filename, "wb") as outfile:
                    writer.write(outfile)
                
                print(f"  ✅ Saved '{output_filename}'")

        print("\nAll chapters have been successfully extracted!")

    except FileNotFoundError:
        print(f"ERROR: The file '{INPUT_PDF_PATH}' was not found.")
        print("Please make sure the path is correct and the file exists.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # This check ensures you have the necessary library installed.
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("Error: The 'pypdf' library is not installed.")
        print("Please install it by running: pip install pypdf")
    else:
        split_pdf_by_chapters()