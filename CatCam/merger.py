import os
import shutil

catcam_output_folder = "./catcamoutput"
merged_folder = "./merged"

# Create the merged folder if it doesn't exist
if not os.path.exists(merged_folder):
    os.makedirs(merged_folder)

# List all the numbered folders
numbered_folders = [name for name in os.listdir(catcam_output_folder) if name.startswith("20")]

# Move files from numbered folders to the merged folder
for folder in numbered_folders:
    folder_path = os.path.join(catcam_output_folder, folder)
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            # Handle duplicate filenames
            new_item_path = os.path.join(merged_folder, item)
            filename, extension = os.path.splitext(item)
            counter = 1
            while os.path.exists(new_item_path):
                new_filename = f"{filename}_{counter}{extension}"
                new_item_path = os.path.join(merged_folder, new_filename)
                counter += 1

            shutil.move(item_path, new_item_path)

    # Optionally, you can remove the emptied numbered folder
    os.rmdir(folder_path)

print("Merging completed.")

