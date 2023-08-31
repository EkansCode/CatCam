import os

merged_folder = "./merged"

# List all files in the merged folder
file_list = os.listdir(merged_folder)

# Delete files with the .h264 extension
for filename in file_list:
    if filename.endswith(".h264"):
        file_path = os.path.join(merged_folder, filename)
        os.remove(file_path)
        print(f"Deleted: {filename}")

print("Deletion of .h264 files completed.")

catcam_output_folder = "./catcamoutput"

# List all files in the catcamoutput folder
file_list = os.listdir(catcam_output_folder)

# Delete all files
for filename in file_list:
    file_path = os.path.join(catcam_output_folder, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted: {filename}")

print("Deletion of all files in catcamoutput folder completed.")

