from logger import Logger

class Logger_not_extracted(Logger):

    def __init__(self, log_file):
        Logger.__init__(self, log_file)
        self.lines_not_extracted = []

    def add_line_not_extracted_from(self, line):
        self.lines_not_extracted.append(line)

    def __combine_words(self):
        words_combined = []

        for word_dict in self.lines_not_extracted:
            word = word_dict["word"]
            episode = word_dict["episode"]
            row = word_dict["row"]
            word_cat = word_dict["word_cat"]

            for d in words_combined:
                if word == d["word"] and word_cat == d["word_cat"]:
                    d["count"] += 1
                    if len (d["location"])<5:
                        d["location"].append((episode, row))
                    break
            else:
                new_entry = {
                    "word": word,
                    "count": 1,
                    "location": [(episode, row)],
                    "word_cat": word_cat
                }
                words_combined.append(new_entry)

        words_combined_sorted = sorted(words_combined, key=lambda x: x['word_cat'], reverse=True)

        return words_combined_sorted

    def __format_word_to_log(self, word):
        starting_line = "\n--------------------------"
        formatted_string = f"\n{word['word']} count: {word['count']}\n\t"
        for location in word["location"]:
            formatted_string += f"| episode: {location[0]}, row: {location[1]}"

        return formatted_string

    def log_words_not_extracted(self):
        lines_not_extracted = self.__combine_words()

        data_to_write = f"WORDS NOT EXTRACTED COUNT: {len(self.lines_not_extracted)}\n\nLINES NOT EXTRACTED: \n\n"
        for idx, word in enumerate(lines_not_extracted):

            if idx == 0 or lines_not_extracted[idx - 1]["word_cat"] != word["word_cat"]:
                data_to_write += f"\n\n{(str(word['word_cat'])).upper()}:\n-----------------------------------------------------------------------------\n"

            data_to_write += self.__format_word_to_log(word)
        self.write_on_log_file_new(data_to_write)