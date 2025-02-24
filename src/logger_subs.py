from logger import Logger

class Logger_subs(Logger):
    def __init__(self, log_file):
        Logger.__init__(self, log_file)

    '''---------------------Sub cleaning------------------------'''

    def log_subs_clean_start(self):
        data_to_write = f"Subtitle Cleaning Log:"
        self.write_on_log_file_new(data_to_write)

    def log_episode_cleaned(self, episode):
        data_to_write = f"\n\n{episode}\n"
        self.write_on_log_file(data_to_write)

    def log_lines_cleaned(self, count):
        data_to_write = f"\tLines cleaned: {count}\n"
        self.write_on_log_file(data_to_write)

    def log_lines_with_japanese(self, count, lines):
        data_to_write_first = f"\tlines with Japanese: {count}\n"

        if lines:
            data_to_write_second = "\tLines with japanese not cleaned:"
            for line in lines:
                line_number = line[0]
                line_text = line[1]
                data_to_write_second = data_to_write_second + f"\n\t\t{line_number}: " + f"{line_text}"
            data_to_write = data_to_write_first + data_to_write_second
        else:
            data_to_write_second = "\tNO LINES W/ JAPANESE THAT WERE NOT CLEANED!"
            data_to_write = data_to_write_first + data_to_write_second
        self.write_on_log_file(data_to_write)
