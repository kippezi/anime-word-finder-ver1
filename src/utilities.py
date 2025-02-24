from datetime import datetime, timedelta
import os


def convertTuple(tup):
    if isinstance(tup[1], int):
        string = f"{tup[0]};{str(tup[1])}"
        return string
    else:
        string = ';'.join(tup)
        return string

def remove_spaces(input_string):
    return input_string.replace(" ", "")

def cut_from_video(input_path, output_path, start_time, end_time):
    #ffmpeg -i input.mkv -ss 00:00:10 -to 00:00:20 -c:v libx264 -c:a aac -strict experimental output.mp4
    cmd_command = f"ffmpeg -i {input_path} -ss {start_time} -to {end_time} -c:v libx264 -c:a aac -strict experimental {output_path}"
    os.system(cmd_command)

def add_seconds_to_time(time_str, seconds_to_add):
    # Convert the time string to a datetime object
    time_obj = datetime.strptime(time_str, '%H:%M:%S')

    # Add the specified number of seconds
    new_time_obj = time_obj + timedelta(seconds=seconds_to_add)

    # Format the new time as "hh:mm:ss"
    new_time_str = new_time_obj.strftime('%H:%M:%S')

    return new_time_str

def count_series_time(folder_path_cleaned_subs):
    time_altogether = timedelta(days=0, hours=0, minutes=0, seconds=0)

    for filename in os.listdir(folder_path_cleaned_subs):
        whole_file_path = os.path.join(folder_path_cleaned_subs, filename)
        if os.path.isfile(whole_file_path):
            first_idx_w_jap, last_idx_w_jap = __find_first_last_index_japanese(whole_file_path)
            with open(whole_file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                first_time = lines[first_idx_w_jap].split(";")[0]
                last_time = lines[last_idx_w_jap].split(";")[0]
                first_time_splitted = first_time.split(":")
                last_time_splitted = last_time.split(":")

                first_time_delta = timedelta(hours=int(first_time_splitted[0]), minutes=int(first_time_splitted[1]), seconds=int(first_time_splitted[2]))
                last_time_delta = timedelta(hours=int(last_time_splitted[0]), minutes=int(last_time_splitted[1]), seconds=int(last_time_splitted[2]))

                time_difference = last_time_delta - first_time_delta
                time_altogether += time_difference

    return time_altogether


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


