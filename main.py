import json

from utils import extract_data_from_pdf, align_content, extract_data

def main():
    # Path to the PDF file
    file_path = "home_inventory.pdf"
    extracted_data = extract_data_from_pdf(file_path)
    print(extracted_data)

    aligned_content = align_content(extracted_data)

    callback_response = json.dumps(extract_data(aligned_content), indent=4)
    print("Data extraction completed successfully.")
    
    return callback_response

if __name__ == "__main__":
    print("Starting the PDF extraction process...")
    print(main())