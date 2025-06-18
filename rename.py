import os
import re

# Set your folder path
folder_path = 'static/album_covers'

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Only process files that match the pattern
    match = re.match(r'(album_covers)-\d+(_.+)', filename)
    if match:
        new_name = match.group(1) + match.group(2)  # removes the number
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_name)
        os.rename(src, dst)
        print(f'Renamed: {filename} → {new_name}')
