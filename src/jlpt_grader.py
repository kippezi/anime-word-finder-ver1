import os
from jlpt_tools import find_jlpt_rating

def re_grade_jlpt(original_grading):
    regraded = []

    for idx, line in enumerate(original_grading):
        word_normalized = line.split(",")[0]
        word_katakana = line.split(",")[1]
        word_count = line.split(",")[2]
        word_cat =  line.split(",")[4]
        word_dict =  {
            "word_normalized": word_normalized,
            "word_reading": word_katakana,
            }

        if idx % 100 == 0:
            print(f"Word {idx}/{len(original_grading)}")
        jlpt_rating_new = find_jlpt_rating(word_dict)

        word_dict["word_count"] = word_count
        word_dict["word_cat"] = word_cat
        word_dict["jlpt_rating"] = jlpt_rating_new

        regraded.append(word_dict)

    return regraded

def write_to_file(file, regraded_list):
    with open(file, "w", encoding="utf-8") as file:
        for word in regraded_list:
            csv_format = f"{word['word_normalized']};{word['word_reading']};{word['word_count']};{word['jlpt_rating']};{word['word_cat']}"
            csv_format = csv_format.strip()
            file.write(csv_format + "\n")

def read_file(file):
    with open(file, "r", encoding="utf-8") as file:
        lines_text = file.readlines()

    return lines_text

original_file = r"C:\Users\Nico\Downloads\Test\Gokushufudou_words.csv"
destination_file = r"C:\Users\Nico\Downloads\Test\Gokushufudou_words_regraded.txt"

original_list = read_file(original_file)
regraded_list = re_grade_jlpt(original_list)
write_to_file(destination_file, regraded_list)

