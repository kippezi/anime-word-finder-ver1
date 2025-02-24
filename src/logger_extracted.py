from logger import Logger

class Logger_extracted(Logger):

    def __init__(self, log_file):
        Logger.__init__(self, log_file)
        self.words_extracted = 0
        self.initial_lines = 0
        self.lines_extracted_from = 0

    def log_subs_extracting_start(self):
        data_to_write = f"Extraction Log:\n"
        self.write_on_log_file_new(data_to_write)

    def log_episode(self, episode):
        data_to_write = f"\n\tEpisode: {episode}\n"
        self.write_on_log_file(data_to_write)

    def log_subs_initial_line_count(self, line_count):
        data_to_write = f"\tInitial line count: {line_count}\n"
        self.initial_lines += line_count
        self.write_on_log_file(data_to_write)

    def log_subs_extracted_from_episode(self, lines_found_count):
        data_to_write = f"\tLines extracted from: {lines_found_count}\n"
        self.lines_extracted_from += lines_found_count
        self.write_on_log_file(data_to_write)

    def log_words_extracted_from_episode(self, word_count):
        data_to_write = f"\tWords found: {word_count}\n"
        self.words_extracted += word_count
        self.write_on_log_file(data_to_write)

    def log_words_extracted_altogether(self, word_count):
        data_to_write = f''' \nALTOGETHER:
                            \n\tInitial lines altogether: {self.initial_lines}
                            \n\tLines extracted from altogether: {self.lines_extracted_from}
                             \n\tWords extracted altogether: {self.words_extracted}
                            \n\tWords in final list altogether: {word_count}'''

        self.write_on_log_file(data_to_write)

    def log_series_time(self, series_time):
        data_to_write = f'\n\n\tThe complete time where Japanese words appear: {series_time}'
        self.write_on_log_file(data_to_write)