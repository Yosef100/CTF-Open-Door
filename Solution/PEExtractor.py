import os

# Path to the combined file (will need to be changed if run on different machine)
combined_file_path = r"C:\Users\tyber\source\repos\Yosef100\CTF-Open-Door\secure\Open Door.png"
extracted_image_path = r"C:\Users\tyber\source\repos\Yosef100\CTF-Open-Door\Solution\Extracted Files\extracted_image.png"
extracted_exe_path = r"C:\Users\tyber\source\repos\Yosef100\CTF-Open-Door\Solution\Extracted Files\extracted_exe.exe"

# Known PE signatures
pe_dos_signature = b'MZ'
pe_header_signature = b'PE\x00\x00'

# Read the combined file
with open(combined_file_path, "rb") as combined_file:
    combined_data = combined_file.read()

# Find PNG end marker
png_end_marker = b'IEND\xae\x42\x60\x82'
end_marker_index = combined_data.find(png_end_marker)
if end_marker_index == -1:
    print("PNG end marker not found.")
    exit()

# Start of padding and executable data
padding_start = end_marker_index + len(png_end_marker)

# Search for PE DOS signature in remaining data
dos_signature_index = combined_data.find(pe_dos_signature, padding_start)
if dos_signature_index == -1:
    print("PE DOS signature not found.")
    exit()

# Search for PE header signature following the DOS signature
pe_header_index = combined_data.find(pe_header_signature, dos_signature_index + len(pe_dos_signature))
if pe_header_index == -1:
    print("PE header signature not found.")
    exit()

# Extract image and executable data
img_data = combined_data[:padding_start]
exe_data = combined_data[dos_signature_index:]

# Save extracted files
with open(extracted_image_path, "wb") as img_file:
    img_file.write(img_data)
    
with open(extracted_exe_path, "wb") as exe_file:
    exe_file.write(exe_data)

# Verify executable
print(f"Extracted image saved as: {extracted_image_path}")
print(f"Extracted executable saved as: {extracted_exe_path}")
print(f"Size of extracted executable: {os.path.getsize(extracted_exe_path)} bytes")

# Check for PE DOS signature
with open(extracted_exe_path, "rb") as exe_file:
    exe_start = exe_file.read(2)
    if exe_start == pe_dos_signature:
        print("Executable appears to be a valid PE file.")
    else:
        print("Executable does not start with expected PE DOS signature.")