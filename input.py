import os
from pypdf import PdfReader
sample_program = "D:\\Python\\Python313\\lab 5.py" #Change this to your program path

def get_code_from_file(file_path):
    # Check if the file actually exists
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."

    # Get the file extension (e.g., '.pdf', '.py', '.txt')
    file_extension = os.path.splitext(file_path)[1].lower()

    # Case 1: If the file is a PDF
    if file_extension == ".pdf":
        try:
            reader = PdfReader(file_path)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() + "\n"
            return full_text
        except Exception as e:
            return f"Error reading PDF: {e}"

    # Case 2: For regular code files (.py, .js, .txt, etc.)
    else:
        try:
            # Open and read the file content as plain text
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except UnicodeDecodeError:
            # Fallback if utf-8 encoding fails
            with open(file_path, "r", encoding="latin-1") as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {e}"
def get_query_from_user():
    # Prompt the user for a query
    user_query = input("Please enter your query about the code: ")
    return user_query
query = get_query_from_user()
# --- Example Usage ---
if __name__ == "__main__":
    # Test with a python file or pdf file path
    sample_file = "/content/(1&2)lab programs.docx (2).pdf"  # Change this to your file path
    

    code_text = get_code_from_file(sample_program)
    

    print("--- Extracted Code Text ---")
    print(code_text)