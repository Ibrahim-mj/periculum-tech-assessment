from utils import extract_data_from_pdf, align_content, extract_data

def main():
    # Path to the PDF file
    file_path = "home_inventory.pdf"
    extracted_data = extract_data_from_pdf(file_path)

    aligned_content = align_content(extracted_data)

    callback_response = extract_data(aligned_content)
    
    return callback_response

if __name__ == "__main__":
    print("Starting the PDF extraction process...")
    print(main())