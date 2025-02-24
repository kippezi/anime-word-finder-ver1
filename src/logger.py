
class Logger:
    def __init__(self, log_file):
        self.log_file = log_file

    def write_on_log_file(self, data_to_write):
        with open(self.log_file, 'a', encoding="utf-8") as file:
            file.write(data_to_write)

    def write_on_log_file_new(self, data_to_write):
        with open(self.log_file, 'w', encoding="utf-8") as file:
            file.write(data_to_write)
