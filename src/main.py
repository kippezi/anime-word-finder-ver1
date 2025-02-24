import math
import os
import regex

#Own
import subcleaner
import japanese_handler
from jlpt_tools import find_jlpt_rating
from utilities import convertTuple, count_series_time, combine_sub_files


#Loggers
from logger_extracted import Logger_extracted
from logger_subs import Logger_subs
from logger_not_extracted import Logger_not_extracted

'''OTHER 
------------------------------------------------------------------------
'''

def __find_first_last_index_japanese(file_path):

    # Regular expression pattern to match Japanese hiragana, katakana, and kanji characters
    japanese_pattern = r'[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}]'

    with open(file_path, "r", encoding="utf-8") as file:
        f_lines = file.readlines()
        for idx, line in enumerate(f_lines):
            if regex.search(japanese_pattern, line):
                first_line_w_jap = idx
                break
        for idx, line in enumerate(reversed(f_lines)):
            if regex.search(japanese_pattern, line):
                last_line_w_jap = (idx * -1) - 1
                break
    return (first_line_w_jap, last_line_w_jap)


'''STATISTIC 
------------------------------------------------------------------------
'''


def get_word_stats(word_list):
    print("\nGetting word stats...\n")
    line_count = len(word_list)
    words_info = []
    for word_idx, word_count in enumerate(word_list):
        if math.remainder(word_idx, 100) == 0:
            print(f"Processing word: {word_idx + 1}/{line_count}")

        word = word_count[0]
        count = word_count[1]
        jlpt_rating = find_jlpt_rating(word)

        word_cat_eng = japanese_handler.word_cat_to_eng(word["word_cat"])
        words_info.append((word["word_normalized"], word["word_reading"], count, jlpt_rating, word_cat_eng))

    return words_info

'''
MAIN
------------------------------------------------------------------------
'''


"""Walks through a folder, reads subtitle files, cleans them leaving only important data,
and stores contents in a new file and new folder with _Cleaned as the ending."""
def filewalk_and_clean_subs(input_folder_path, output_folder_path, logger_subs):
    print("Cleaning subs...\n")
    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            if file.endswith('.srt') or file.endswith('.vtt') or file.endswith('.ssa') or file.endswith('.ass'):
                file_path = os.path.join(root, file)
                output_file_content = subcleaner.process_file(file_path, logger_subs)
                output_file_name = file.split(".")[-2] + "_Cleaned" + ".txt"
                output_file_path = os.path.join(output_folder_path, output_file_name)
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    for line in output_file_content:
                        file.write(convertTuple(line) + "\n")

'''Takes a cleaned subtitle file, takes only the text in the subtitle line, uses japanese_handler to get seperate word from it,
which it adds to a list that is returned from the function'''
def __get_separate_words_from_file(cleaned_sub_file_path, logger, logger_not_extract):
    episode = cleaned_sub_file_path.split("\\")[-1].split("_")[0]
    logger.log_episode(episode)
    with open(cleaned_sub_file_path, 'r', encoding='utf-8') as file:
        print("Getting separate words...")
        words = []
        line_extracted_amount = 0
        line_amount = 0
        for row_idx, line in enumerate(file):
            line_amount += 1
            text = line.split(";")[1]
            words_in_line = japanese_handler.get_words_in_line(text, logger_not_extract, episode, row_idx)
            if len(words_in_line) != 0:
                words.extend(words_in_line)
                line_extracted_amount += 1
        logger.log_subs_initial_line_count(line_amount)
        print(f"Lines read: {line_extracted_amount}")
        print(f"Words found: {len(words)}\n")
        logger.log_subs_extracted_from_episode(line_extracted_amount)
        logger.log_words_extracted_from_episode(len(words))

        return words

'''Takes all the separate words and combines same words with a number of how many there were'''
def __combine_words_with_count(word_list):
    print("Combining words...\n")
    word_list_with_count = []

    for idx, word in enumerate(word_list):
        word_count = len(word_list)
        if idx + 1 % 1000 == 0:
            print(f"Combined {idx + 1}/{word_count}")
        word_found = False

        for idx_wordlist_count, (word_in_list, count) in enumerate(word_list_with_count):

            if (
                word["word_normalized"] == word_in_list["word_normalized"]
                and word["word_reading"] == word_in_list["word_reading"]
            ):
                word_list_with_count[idx_wordlist_count] = (word_in_list, count + 1)
                word_found = True
                break

        if not word_found:
            word_list_with_count.append((word, 1))

    return word_list_with_count
'''Write all the words found in the series to a file'''
def __write_all_words_to_file(words_with_count_and_stats, output_filepath, logger):
    count_all = 0
    with open(output_filepath, 'w', encoding='utf-8') as file:
        for word_reading_count_jlpt_cat in words_with_count_and_stats:
            word = word_reading_count_jlpt_cat[0]
            word_reading = word_reading_count_jlpt_cat[1]
            count = word_reading_count_jlpt_cat[2]
            jlpt_rating = word_reading_count_jlpt_cat[3]
            word_cat = word_reading_count_jlpt_cat[4]
            count_all += count
            file.write(f"{word};{word_reading};{count};{jlpt_rating};{word_cat}\n")
    logger.log_words_extracted_altogether(count_all)

def filewalk_and_find_words_in_whole_series(folder_path_cleaned_subs, logger,  logger_not_extract):
    """Walks through a folder, reads text files, and stores contents in a list."""
    all_words_in_series = []
    logger.log_subs_extracting_start()
    for root, dirs, files in os.walk(folder_path_cleaned_subs):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                words_in_episode = __get_separate_words_from_file(file_path, logger, logger_not_extract)
                all_words_in_series.extend(words_in_episode)

    return all_words_in_series



def main():

    '''------------------------------------VARIABLES------------------------------------------------'''
    root_path = r''
    series_name = root_path.split("\\")[-1]

    # Subs
    logger_subs_path = f'{root_path}\\Written_Assets\\Logs\\{series_name}_logSubs.txt'
    logger_subs = Logger_subs(logger_subs_path)
    input_folder_path_orig_subs = f'{root_path}\\Written_Assets\\Subs'
    folder_path_cleaned_subs = f'{root_path}\\Written_Assets\\SubsCleaned'

    # Logger Extracted
    logger_path = f'{root_path}\\Written_Assets\\Logs\\{series_name}_logExtracted.txt'
    logger = Logger_extracted(logger_path)

    # Logger NOT Extracted
    logger_path_words_not_extract = f'{root_path}\\Written_Assets\\Logs\\{series_name}_logNotExtractedLines.txt'
    logger_words_not_extract = Logger_not_extracted(logger_path_words_not_extract)

    # Words
    output_file_path_words = f'{root_path}\\Written_Assets\\{series_name}_WordsPerEpisodes.txt'
    output_file_all_subs = f'{root_path}\\Written_Assets\\{series_name}_SUBS_COMBINED.txt'

    '''------------------------------------STEPS------------------------------------------------'''
    #1　Clean subtitle files and write to separate files that have season and episode written on them with filewalk_and_clean()
    logger_subs.log_subs_clean_start()
    filewalk_and_clean_subs(input_folder_path_orig_subs, folder_path_cleaned_subs, logger_subs)

    #2 Use Use filewalk_and_find_words_in_whole_series to go through these files
    all_words_in_series = filewalk_and_find_words_in_whole_series(folder_path_cleaned_subs, logger, logger_words_not_extract)
    words_combined_and_counted = __combine_words_with_count(all_words_in_series)
    words_combined_and_counted_sorted = sorted(words_combined_and_counted, key=lambda x:x[1], reverse=True)

    #3 Count same words together and write to file in CSV format (;)
    words_with_count_and_stats = get_word_stats(words_combined_and_counted_sorted)
    __write_all_words_to_file(words_with_count_and_stats, output_file_path_words, logger)

    #4 Find length of the whole series from subtitles (last subtitle time w/ jap - first subtitle time w/ jap  * episodes in the series) and log it
    time_altogether_where_jap_words = count_series_time(folder_path_cleaned_subs)
    logger.log_series_time(time_altogether_where_jap_words)

    #5 Log the lines where no japanese was extracted from
    logger_words_not_extract.log_words_not_extracted()

    # Write all the subs on a single file
    combine_sub_files(folder_path_cleaned_subs, output_file_all_subs)


    print("\nProgram completed succesfully!")

if __name__ == "__main__":
    main()
