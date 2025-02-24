import re


from japanese_handler import contains_japanese_text
'''------------------------------------Utilities--------------------------------------------------'''

def __remove_brackets(text):
    # Replace FULLWIDTH LEFT PARENTHESIS and FULLWIDTH RIGHT PARENTHESIS with normal parentheses
    text = text.replace('（', '(').replace('）', ')')

    # Use regular expressions to find and remove nested parentheses
    while re.search(r'\([^()]*\)', text):
        text = re.sub(r'\([^()]*\)', '', text)

    # Remove any remaining normal parentheses
    text = text.replace('(', '').replace(')', '')

    return text


'''------------------------------------------Subtitle Extracters--------------------------------------------------'''

def __extract_subtitles_ssa(input_text):
    subtitles = []
    lines = input_text.split('\n')
    i = 0
    while i < len(lines):

        description_time = lines[i].split(" ")
        description = description_time[0]

        if re.search(r"\\blur\d", lines[i]) or len(lines[i].split(",,")) < 3 or lines[i].split(",,")[2] == "" or description != "Dialogue:":
            is_sub = False
        else:
            is_sub = True

        if  not is_sub:
            i += 1
            continue
        else:
            time = description_time[1].split(",")[1]
            text = lines[i].split(",,")[2].strip()
            subtitles.append((time, text))
            i += 1

    return subtitles

def __extract_subtitles_ass(input_text, logger):
    subtitles = []
    lines = input_text.split('\n')
    i = 0

    lines_with_japanese_count = 0
    lines_with_japanese_not_cleaned = []

    lines_extracted = 0

    while i < len(lines):

        description_time = lines[i].split(" ")
        description = description_time[0]

        if description != "Dialogue:":
            if contains_japanese_text(lines[i]):
                lines_with_japanese_not_cleaned.append((i, lines[i]))
                lines_with_japanese_count += 1
            is_sub = False
        else:
            is_sub = True

        if  not is_sub:
            i += 1
            continue
        else:
            time = description_time[1].split(",")[1]
            time_formatted = f"0{time[:-3]}"
            text = lines[i].split(",,")[-1].strip()
            subtitles.append((time_formatted, text))
            lines_extracted += 1
            lines_with_japanese_count = 0
            i += 1

    logger.log_lines_cleaned(lines_extracted)
    logger.log_lines_with_japanese(lines_with_japanese_count, lines_with_japanese_not_cleaned)
    return subtitles


def __extract_subtitles_srt(input_text, logger):
    subtitles = []
    lines = input_text.split('\n')
    i = 0

    lines_with_japanese_count = 0
    lines_with_japanese_not_cleaned = []

    lines_extracted = 0

    while i < len(lines):
        line_has_japanese = contains_japanese_text(lines[i])
        if lines[i].strip() == '' or not re.findall(" --> ", lines[i]):
            if line_has_japanese:
                lines_with_japanese_not_cleaned.append((i, lines[i]))
                lines_with_japanese_count += 1
            i += 1
            continue

        # Extract the time range before " --> " and remove any leading/trailing spaces
        time_range = lines[i].split(" --> ")[0].strip()
        time_range = time_range.split(",")[0]
        i += 1

        # Extract the text until an empty line or the end of the input
        text = []
        while i < len(lines) and not lines[i].strip().isdigit():
            if lines[i].strip() == '':
                i += 1
                continue
            line = lines[i]
            line = line.replace("&lrm;", "")
            line = line.replace("{\\an8}", "")
            line = line.strip()
            text.append(line)
            lines_with_japanese_count += 1
            i += 1

        # Combine the time range and text as a tuple and add it to the list if the text has content
        if len(text) != 0:
            lines_extracted += len(text)
            subtitles.append((time_range, '、'.join(text)))

    logger.log_lines_cleaned(lines_extracted)
    logger.log_lines_with_japanese(lines_with_japanese_count, lines_with_japanese_not_cleaned)

    return subtitles
# Netflix
def __extract_subtitles_vtt(input_text, logger):
    subtitles = []
    lines = input_text.split('\n')
    i = 0

    lines_with_japanese_count = 0
    lines_with_japanese_not_cleaned = []
    lines_extracted = 0

    while i < len(lines):
        if lines[i].strip() == '' or not re.findall(" --> ", lines[i]):
            line_has_japanese = contains_japanese_text(lines[i])
            if line_has_japanese:
                lines_with_japanese_not_cleaned.append((i, lines[i]))
                lines_with_japanese_count += 1

            i += 1
            continue

        # Extract the time range before " --> " and remove any leading/trailing spaces
        time_range = lines[i].split(" --> ")[0].strip()
        time_range = time_range.split(".")[0]
        i += 1

        # Extract the text until an empty line or the end of the input
        text = []
        while i < len(lines) and not lines[i].strip().isdigit():
            line_has_japanese = contains_japanese_text(lines[i])
            if lines[i].strip() == '':
                i += 1
                continue
            line = lines[i]
            line = re.sub("</?c.(j|J)apanese>", "", line)
            line = re.sub("</?c.bg_transparent>", "", line)
            line = re.sub("&lrm;", "", line)
            line = line.strip()
            if line != "":
                text.append(line)
            i += 1

        # Combine the time range and text as a tuple and add it to the list if the text has content
        if text and len(text) != 0:
            lines_extracted += len(text)
            lines_with_japanese_count += len(text)
            subtitles.append((time_range, '、'.join(text)))

    logger.log_lines_cleaned(lines_extracted)
    logger.log_lines_with_japanese(lines_with_japanese_count, lines_with_japanese_not_cleaned)
    return subtitles

'''---------------------------------------¨Main Tool-----------------------------------------------------------'''

def process_file(input_file_path, logger=None):
    # Read the input file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()

    episode = input_file_path.split("\\")[-1]
    logger.log_episode_cleaned(episode)

    cleaned_text = __remove_brackets(input_text)
    file_type = input_file_path.split(".")[-1]
    if file_type == "vtt":
        time_and_subtitles = __extract_subtitles_vtt(cleaned_text, logger)
    elif file_type== "srt":
        time_and_subtitles = __extract_subtitles_srt(cleaned_text, logger)
    elif file_type== "ssa":
        time_and_subtitles = __extract_subtitles_ssa(cleaned_text)
    elif file_type == "ass":
        time_and_subtitles = __extract_subtitles_ass(cleaned_text, logger)

    lines_found_count = len(time_and_subtitles)
    episode = input_file_path.split("\\")[-1].split(".")[0]

    return time_and_subtitles
