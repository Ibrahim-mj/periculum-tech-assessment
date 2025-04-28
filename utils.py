import re

import pdfplumber
import camelot

from models import Inventory, OwnerInfo


def extract_data_from_pdf(file_path: str) -> list:
    """
    Extracts data from a PDF file and returns it as a list of tables.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        list: A list of tables extracted from the PDF.
    """
    extracted_tables = []

    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages

        plumber_tables = []
        camelot_tables = []
        count = 0
        while count < len(pages):
            # if count == len(pages):
            #     break
            print("Page: ", count)
            # tables = pages[count].extract_tables() # extract tables with pdfplumber
            tables = camelot.read_pdf(
                "home_inventory.pdf", pages=str(count + 1), flavor="stream"
            )
            if len(tables) > 0:
                print(f"Tables found on page {count + 1}:{len(tables)}")
                for table in tables:
                    plumber_tables.append(table)
            else:
                print(f"No tables found on page {count + 1}, extracting with camelot")
                tables = camelot.read_pdf(
                    "home_inventory.pdf", pages=str(count + 1), flavor="stream"
                )
                if len(tables) > 0:
                    print(f"Tables found on page {count + 1}:{len(tables)}")
                    for table in tables:
                        camelot_tables.append(table.df.values.tolist())
                else:
                    print(f"No tables found on page {count + 1} with camelot")
            count += 1

        extracted_tables.extend(plumber_tables)
        extracted_tables.extend(camelot_tables)

        return [table.df.values.tolist() for table in extracted_tables]


def align_content(content: list) -> str:
    """
    Aligns the content of the extracted tables into a formatted string.

    Args:
        content (list): The extracted content from the PDF.

    Returns:
        str: The aligned content as a formatted string.
    """
    formatted_text = ""
    for table in content:
        for row in table:
            formatted_text += " ".join([str(cell) for cell in row]) + "\n"
        formatted_text += "\n"

    return formatted_text.strip()


def extract_data(aligned_content: str) -> dict:

    lines = aligned_content.splitlines()

    # owner info - initialization
    owner_name = ""
    owner_address = ""
    owner_telephone = ""

    # owner information - extraction
    for line in lines:
        if line.startswith("Name"):
            owner_name = line.replace("Name", "").strip()
        elif line.startswith("Address"):
            owner_address = line.replace("Address", "").strip()
        elif line.startswith("Phone Number"):
            owner_telephone = line.replace("Phone Number", "").strip()

    owner_info = OwnerInfo(owner_name, owner_address, owner_telephone)

    pattern = r"""
    (\d+)
    \s+([A-Za-z\s]+)
    \s+([A-Za-z\s]+)
    \s+([A-Za-z]+)
    \s+(\d{2}/\d{2}/\d{4})
    \s+([A-Za-z]+)
    \s+([A-Z0-9]+)
    \s*\n\$\s*([\d,]+\.\d{2})    
    """

    match = re.findall(pattern, aligned_content, re.VERBOSE)

    inventory_list = []

    for item in match:
        inventory_item = Inventory(
            purchase_date=item[4].strip(),
            serial_number=item[6].strip(),
            description=item[2].strip(),
            source_style_area={
                "source": item[3],
                "area": item[1],
                "style": item[5],
            }, # not sure if this is the expected format or not. Could be like this too: {f"{item[3]}_{item[1]}_{item[5]}"}
            value=float(item[7].replace(",", "")), # not sure if I should include the '$' sign or not.
        )
        inventory_list.append(inventory_item)

    return {
        "owner_info": owner_info.to_dict(),
        "data": [inv.to_dict() for inv in inventory_list],
    }