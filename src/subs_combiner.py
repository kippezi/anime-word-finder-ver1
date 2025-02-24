import os

def combine_sub_files(input_folder, output_file):
    # List of valid text file extensions
    extension = ".txt"

    # Open the output file in write mode
    with open(output_file, 'w', encoding='utf-8') as output:
        # Walk through the input folder
        for foldername, subfolders, filenames in os.walk(input_folder):
            for filename in filenames:
                # Check if the file has a valid extension
                if filename.lower().endswith(extension):
                    file_path = os.path.join(foldername, filename)

                    # Read the content of the text file and write it to the output file
                    with open(file_path, 'r', encoding='utf-8') as input_file:
                        output.write(f"\n\n########## {filename} ##########\n\n")
                        output.write(input_file.read())





folder_path_cleaned_subs = r"F:\Dropbox\NikonGo\Video Material\Anime\MobPsycho100\Written_Assets\SubsCleaned"
output_file_all_subs = r"F:\Dropbox\NikonGo\Video Material\Anime\MobPsycho100\Written_Assets_SUBS_COMBINED.txt"
combine_sub_files(folder_path_cleaned_subs, output_file_all_subs)