# import pymupdf
import pdfplumber
import camelot

class OwnerInfo():
    def __init__(self, owner_name, owner_address, owner_telephone):
        self.owner_name = owner_name
        self.owner_address = owner_address
        self.owner_telephone = owner_telephone
    

class Inventory():
    def __init__(self, purchase_date, serial_number, description, source_style_area, value):
        self.purchase_date = purchase_date
        self.serial_number = serial_number
        self.description = description
        self.source_style_area = source_style_area
        self.value = value


# def get_data_from_pdf(file_path):
#     doc = pymupdf.open(file_path)
#     page = doc[0]
#     blocks = page.get_text("blocks")
#     doc.close()

#     return blocks

# def align_content(blocks):
#     sorted_blocks = sorted(blocks, key=lambda b: (round(b[1], 1), b[0]))

#     formatted_text = ""
#     for block in sorted_blocks:
#         # formatted_text += block[4].strip() + "\n"
#         formatted_text += f"{block[4].strip()}\n"

#     return formatted_text


# extracted_text = get_data_from_pdf('home_inventory.pdf')

# print("Extracted Text:")
# print(extracted_text)
# print("====================================================")
# print("Formatted Text:")
# formatted_text = align_content(extracted_text)
# print(formatted_text)

    # # Split the text into lines
    # lines = text.split('\n')

    # # Extract owner information
    # owner_name = lines[0].strip()
    # owner_address = lines[1].strip()
    # owner_telephone = lines[2].strip()
    
    # # Create an OwnerInfo object
    # owner_info = OwnerInfo(owner_name, owner_address, owner_telephone)

    # # Extract inventory information
    # inventory_list = []
    # for line in lines[3:]:
    #     if line.strip():  # Ignore empty lines
    #         parts = line.split(',')
    #         purchase_date = parts[0].strip()
    #         serial_number = parts[1].strip()
    #         description = parts[2].strip()
    #         source_style_area = parts[3].strip()
    #         value = float(parts[4].strip())
            
    #         # Create an Inventory object and add it to the list
    #         inventory_item = Inventory(purchase_date, serial_number, description, source_style_area, value)
    #         inventory_list.append(inventory_item)

    # return owner_info, inventory_list


# with pdfplumber.open('home_inventory.pdf') as pdf:
#     # print(pdf.pages[0].extract_text())
#     all_doc = pdf.pages
#     table_data_list = []
#     for page in all_doc:
#         tables = page.find_tables()
        
#         for table in tables:
#             table_data = table.extract()
#             table_data_list.append(table_data)
#     table_data_list = table_data_list
#     print(len(table_data_list))
#     second_table = table_data_list[2]
#     # for row in second_table[1]:
#     #     print(row)
#     # for table_data in table_data_list:
#     second_page = all_doc[1]
#     print(second_page.find_tables())
            # text = ''
            # for row in table_data:
            #     text += ' '.join([str(cell) for cell in row]) + '\n'
            # print(text)

    # first_table = pdf.pages[0].find_tables()[0].extract()
    # print(first_table)
    # for row in first_table:
    #     print(row)

# def get_data_from_pdf(file_path):
#     with pdfplumber.open(file_path) as pdf:
#         tables = []
#         for page in pdf.pages:
#             tables.extend(page.find_tables())
#         for table in tables:
#             table_data = table.extract()
#             print(table_data)
#             text = ''
#             for row in table_data:
#                 text += ' '.join([str(cell) for cell in row]) + '\n'
#         return text

# print(get_data_from_pdf('home_inventory.pdf'))

# def align_content(raw_text):
#     text = raw_text.replace('\n', ' ').replace('  ', ' ').strip()
#     text = list(text)
#     for table in text:
#         print(table)
            
#     print(type(text))
#     return text


    
    
    
    # print(raw_text)
    # for table in raw_text:
    #     for row in table.extract():
    #         for cell in row:
    #             print(cell)

# print('')


# print(align_content(get_data_from_pdf('home_inventory.pdf')))

# tables = camelot.read_pdf('home_inventory.pdf', pages='all', flavor='stream')

# # print(len(tables))
# # print(type(tables))
# # print(tables)
# # print(tables[0].df.values.tolist())

# if len(tables) > 0:
#     for i, table in enumerate(tables):
#         print(f"Table {i+1}:")
#         print(table.df.values.tolist())
extracted_tables = []

with pdfplumber.open('home_inventory.pdf') as pdf:
    pages = pdf.pages
    
    plumber_tables = []
    camelot_tables = []
    count = 0
    while count < len(pages):
        # if count == len(pages):
        #     break
        print("Page: ", count)
        # tables = pages[count].extract_tables() # extract tables with pdfplumber
        tables = camelot.read_pdf('home_inventory.pdf', pages=str(count+1), flavor='stream')
        if len(tables) > 0:
            print(f"Tables found on page {count + 1}:{len(tables)}")
            for table in tables:
                plumber_tables.append(table)
        else:
            print(f"No tables found on page {count + 1}, extracting with camelot")
            tables = camelot.read_pdf('home_inventory.pdf', pages=str(count+1), flavor='stream')
            if len(tables) > 0:
                print(f"Tables found on page {count + 1}:{len(tables)}")
                for table in tables:
                    camelot_tables.append(table.df.values.tolist())
            else:
                print(f"No tables found on page {count + 1} with camelot")
        count += 1
    
    extracted_tables.extend(plumber_tables)
    extracted_tables.extend(camelot_tables)
    
print(f"Total tables extracted: {len(extracted_tables)}")
# ==========================================================
print("Extracted Tables:", extracted_tables)

for table in extracted_tables:
    print(type(table))
    print("Table:")
    for row in table.df.values.tolist():
        print(row)


#     extracted_tables.extend(plumber_tables)
#     if len(tables) < len(pages):
#         tables = camelot.read_pdf('home_inventory.pdf', pages='all', flavor='stream')
#         extracted_tables.extend(tables.df.values.tolist())

# print(len(extracted_tables))