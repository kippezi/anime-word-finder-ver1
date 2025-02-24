from utilities import convertTuple, remove_spaces
from japanese_handler import has_kanji, hiragana_to_katakana, analyze_word_jlpt

# JLPT LISTS RAW
N1_words_RAW = r"F:\Dropbox\NikonGo\GeneralAssets\JLPTWordLists\N1ListRaw.txt"
N2_words_RAW = r"F:\Dropbox\NikonGo\GeneralAssets\JLPTWordLists\N2ListRaw.txt"
N3_words_RAW = r"F:\Dropbox\NikonGo\GeneralAssets\JLPTWordLists\N3ListRaw.txt"
N4_words_RAW = r"F:\Dropbox\NikonGo\GeneralAssets\JLPTWordLists\N4ListRaw.txt"
N5_words_RAW = r"F:\Dropbox\NikonGo\GeneralAssets\JLPTWordLists\N5ListRaw.txt"

# JLPT LISTS STANDARDIZED
N1_words = r"F:\Dropbox\NikonGo\GeneralAssets\JLPTWordLists\Standardized\N1ListStandardized.txt"
N2_words = r"F:\Dropbox\NikonGo\GeneralAssets\JLPTWordLists\Standardized\N2ListStandardized.txt"
N3_words = r"F:\Dropbox\NikonGo\GeneralAssets\JLPTWordLists\Standardized\N3ListStandardized.txt"
N4_words = r"F:\Dropbox\NikonGo\GeneralAssets\JLPTWordLists\Standardized\N4ListStandardized.txt"
N5_words = r"F:\Dropbox\NikonGo\GeneralAssets\JLPTWordLists\Standardized\N5ListStandardized.txt"

word_lists_raw = [N5_words_RAW, N4_words_RAW, N3_words_RAW, N2_words_RAW, N1_words_RAW]
word_lists_standard = [N5_words, N4_words, N3_words, N2_words, N1_words]

def find_jlpt_rating(word):

    def compare_to_list(word_to_check, list_path):
        word_to_check_has_kanji = has_kanji(word_to_check["word_normalized"])
        in_list = False
        with open(list_path, 'r', encoding="utf-8") as file:
            for line in file:
                jlpt_list_line = line.split(";")

                jlpt_kanji = jlpt_list_line[0]
                jlpt_reading = jlpt_list_line[1]
                jlpt_kanji_alternatives = jlpt_kanji.split("/")
                jlpt_reading_alternatives = jlpt_reading.split("/")

                matches_kanji = False
                for jlpt_kanji_alternative in jlpt_kanji_alternatives:

                    # If the word has no kanji (for children etc) check the normalized form agains reading form
                    if not word_to_check_has_kanji:
                        for jlpt_reading_alternative in jlpt_reading_alternatives:
                            if hiragana_to_katakana(word_to_check["word_normalized"]) == jlpt_reading_alternative:
                                matches_kanji = True
                                break
                    # In other case check both normalized to normalized AND reading form to reading form
                    elif (word_to_check["word_normalized"] == jlpt_kanji_alternative
                        or (jlpt_kanji_alternative[0] == "御" and word_to_check["word_normalized"] == jlpt_kanji_alternative[1:])
                        or (word_to_check["word_normalized"][0] == "御" and word_to_check["word_normalized"][1:] == jlpt_kanji_alternative)
                    ):
                        matches_kanji = True
                        break

                # Finally if nothing was found mark it as not matching and check next
                if not matches_kanji:
                    continue

                #If was a match also check that the reading alternatives match
                matches_reading = False
                for jlpt_reading_alternative in jlpt_reading_alternatives:
                    if(
                    word_to_check["word_reading"] == jlpt_reading_alternative
                    or (jlpt_kanji_alternative[0] == "御" and word_to_check["word_reading"] == jlpt_reading_alternative[1:])
                    or (word_to_check["word_normalized"][0] == "御" and word_to_check["word_reading"][1:] == jlpt_reading_alternative)
                    ):
                        matches_reading = True
                        break

                if matches_kanji and matches_reading:
                    in_list = True
                    return in_list
            return in_list


    for idx, word_list in enumerate(word_lists_standard):
        if compare_to_list(word, word_list) == True:
            if idx == 0:
                return "N5"
            elif idx == 1:
                return "N4"
            elif idx == 2:
                return "N3"
            elif idx == 3:
                return "N2"
            elif idx == 4:
                return "N1"

    return "N0"

def jlpt_standardizer():

    output_folder = r"F:\Dropbox\NikonGo\GeneralAssets\JLPTWordLists\Standardized"

    def combine_analyzed_words(word_array):
        kanjis_comb = ""
        reading_comb = ""
        print(type(word_array))
        for word in word_array:
            kanjis_comb += word["word_normalized"]
            reading_comb += word["word_reading"]
        return (kanjis_comb, reading_comb)

    all_jlpt = [N5_words_RAW, N4_words_RAW, N3_words_RAW, N2_words_RAW, N1_words_RAW]
    for jlpt in all_jlpt:
        words_stand = []
        with open(jlpt, "r", encoding="utf-8") as file:
            for line in file:
                japanese_english = line.split("-")
                if len(japanese_english) >= 2:
                    english = japanese_english[1].strip()
                    japanese = remove_spaces(japanese_english[0])

                    # If there is Kanji and hiragana on the row
                    if "," in japanese:
                        kanji_hiragana = japanese.split(",")
                        word_hiragana = kanji_hiragana[1]
                        word_reading = hiragana_to_katakana(word_hiragana)
                        word_kanji = kanji_hiragana[0]
                        kanji_converted = analyze_word_jlpt(word_kanji).strip()
                        new_form = (kanji_converted, word_reading, english)
                    # If there is only hiragana/katakana on the row
                    else:
                        word_reading =  hiragana_to_katakana(japanese)
                        kanji_converted = analyze_word_jlpt(japanese).strip()
                        new_form = (kanji_converted, word_reading, english)
                    words_stand.append(new_form)

        new_path_ending = jlpt.split("\\")[-1].replace("Raw", "Standardized")
        new_path = output_folder + "\\" + new_path_ending
        with open(new_path, "w", encoding="utf-8") as file:
            for word in words_stand:
                file.write(convertTuple(word)+ "\n")

def __compare_raw_and_stand():
    with open(N5_words_RAW, "r", encoding="utf-8") as file:
        lines_raw = file.readlines()

    with open(N5_words, "r", encoding="utf-8") as file:
        lines_standard = file.readlines()
    i = 0
    while i < len(lines_raw) - 1 and i < len(lines_standard) - 1:
        if lines_raw[i][0] != lines_standard[i][0] or lines_raw[i][1] != lines_standard[i][1] and  lines_standard[i][1] !=";":
            print(f"Difference in lines!\n\tline in raws: {lines_raw[i]}\n\tline in standardized: {lines_standard[i]}")
        i += 1

#jlpt_standardizer()

#compare_raw_and_stand()

#print(find_jlpt_rating({"word_normalized": "姉ちゃん", "word_reading": "ネエチャン", "word_cat": "名詞"}))

def __check_that_only_one_word_per_line():
    partitions_supposed_tobe = 3
    word_list_names = ["N5", "N4", "N3", "N2", "N1"]
    for word_list_idx, word_list in enumerate(word_lists_standard):
        word_list_name = word_list_names[word_list_idx]
        with open(word_list, "r", encoding="utf-8") as file:
            for line_idx, line in enumerate(file):
                partitions = line.split(";")
                if len(partitions) != partitions_supposed_tobe:
                    print(f"List: {word_list_name}\n\tline: {line_idx + 1}\n\tcontent: {line}")

