import csv
import japanese_handler
import os

from utilities import cut_from_video
from utilities import add_seconds_to_time

def add_seconds_to_time(time_str, seconds_to_add):
    # Convert the time string to a datetime object
    time_obj = datetime.strptime(time_str, '%H:%M:%S')

    # Add the specified number of seconds
    new_time_obj = time_obj + timedelta(seconds=seconds_to_add)

    # Format the new time as "hh:mm:ss"
    new_time_str = new_time_obj.strftime('%H:%M:%S')

    return new_time_str

def get_words_from_csv(csv_file):
    print("Getting words from the csv file...")
    words_to_find_list = []
    with open(csv_file, "r", encoding="utf-8") as file:
        words_to_find = csv.reader(file)
        for idx, word in enumerate(words_to_find):
            if idx != 0:
                words_to_find_list.append(word[0])
    return words_to_find_list

def get_sentences_from_sub(sub_file_path):
    episode = sub_file_path
    episode_lines = []
    with open(sub_file_path, "r", encoding="utf-8") as file:
        for line in file:
            time_text = line.split(";")
            time = time_text[0]
            text = time_text[1]
            episode_lines.append((time, text))
    return (episode, episode_lines)


def get_all_sentences_in_subs(subs_folder_path):
    # format = [
    #           (episode, episode_lines[(time, text)])
    #           (episode, episode_lines[(time, text)])
    #          ]
    episode_sentences = []
    for root, dirs, files in os.walk(subs_folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                print(f"Searching through: {file}...")
                episode_sentences.append(get_sentences_from_sub(file_path))

    return episode_sentences

def log_words_to_find_in_subs(words_to_find, sentences_in_subs):
    words_found_log = []
    for word_to_find in words_to_find:
        print(word_to_find)
        words_found_counter = 0
        for sentence_in_subs in sentences_in_subs:
            if words_found_counter == 3:
                break
            episode = sentence_in_subs[0]
            times_and_sentences = sentence_in_subs[1]
            for time_and_sentence in times_and_sentences:
                if words_found_counter == 3:
                    break
                time = time_and_sentence[0]
                sentence = time_and_sentence[1]
                separate_words = japanese_handler.get_words_in_line(sentence, post_process=True)
                for separate_word in separate_words:
                    if word_to_find == separate_word["word_normalized"]:
                        words_found_log.append((episode, time, word_to_find))
                        words_found_counter += 1
    return words_found_log

def cut_from_video(input_path, output_path, start_time, end_time):
    #ffmpeg -i input.mkv -ss 00:00:10 -to 00:00:20 -c:v libx264 -c:a aac -strict experimental output.mp4
    cmd_command = f"ffmpeg -i {input_path} -ss {start_time} -to {end_time} -c:v libx264 -c:a aac -strict experimental {output_path}"
    os.system(cmd_command)

def write_words_to_teach_to_file(log_file_destination, log_of_words):
    with open(log_file_destination, "w", encoding="utf-8") as file:
        for word in log_of_words:
            file.write(";".join(word) + "\n")


root_path = r"F:\Dropbox\NikonGo\Video Material\Anime\MobPsycho100\Written_Assets"
words_csv_file_path = f"{root_path}\SubWordsToFind.csv"
sub_cleaned_file_path = f"{root_path}\SubsCleaned"
#video_clips_cut = f"{root_path}\AnimeClips"
log_file_destination = f"{root_path}\WordsToTeachLocationSub.txt"

words_to_find = get_words_from_csv(words_csv_file_path)
all_sentences = get_all_sentences_in_subs(sub_cleaned_file_path)
log_of_words = log_words_to_find_in_subs(words_to_find, all_sentences)
write_words_to_teach_to_file(log_file_destination, log_of_words)

'''
time_variation = 5

for word in log_of_words:
    input_path = log_of_words[0]
    output_path = f"{input_path.split('.')[0]}.mp4"
    start_time_str = log_of_words[1]
    start_time_obj = datetime.strptime(start_time_str, '%H:%M:%S')
    start_time_obj_adj = start_time_obj + timedelta(seconds=time_variation)
    start_time =  start_time_obj_adj.strftime('%H:%M:%S')
    end_time = start_time_obj_adj + timedelta(seconds=5)
    cut_from_video(input_path, output_path, start_time, end_time)

'''

