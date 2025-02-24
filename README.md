# Japanese Subtitle Processor

This project takes as input a certain folder structure, scans all the Japanese subtitle files found there, and processes them to extract meaningful words. The program reads various subtitle formats, standardizes them to a common format, and then tokenizes the lines to extract nouns, adjectives, adverbs, and verbs (the main meaning-giving words). It normalizes and provides readings for each extracted word, combines the same words with counts, and adds the JLPT (Japanese Language Proficiency Test) level. The results are written to a CSV file for further processing in Excel or Google Sheets. Additionally, the program logs various details about the process, including the words that weren't included and information about the subtitles themselves.

## Files in the Project

### `japanese_handler`
Handles Japanese word-related processes, including word normalization and readings.

### `jlpt_grader`
Handles the JLPT grading for words based on their frequency and usage.

### `jlpt_tools`
Handles miscellaneous JLPT-related tasks.

### `logger`
A base class for logging, inherited by other specialized loggers.

### `logger_extracted`
Logs information about the words that were successfully extracted.

### `logger_not_extracted`
Logs information about words that weren't included in the extraction process.

### `logger_subs`
Logs information related to the subtitles being processed.

### `subcleaner`
Handles subtitle cleaning and management tasks.

### `subs_combiner`
Combines multiple subtitle files for easier manual inspection.

### `utilities`
Contains miscellaneous utility functions used throughout the project.

### `word_finder`
Finds specific words in subtitle files and can be used separately for word extraction after the processing.

## Requirements

To run the project, you need to install the following Python packages:

- `regex==2024.11.6`
- `SudachiDict-full==20241021`
- `SudachiPy==0.6.10`

## How It Works

1. **Input**: The program scans a given folder structure containing subtitle files.
2. **Standardization**: The program reads multiple subtitle formats and standardizes them to a single format.
3. **Tokenization**: Each line of the subtitles is tokenized, and the meaningful words (verbs, adverbs, nouns, adjectives) are extracted.
4. **Normalization**: The extracted words are normalized and their readings are obtained.
5. **JLPT Grading**: Each word is assigned a JLPT level based on its frequency and use.
6. **CSV Output**: The processed words are combined, their frequencies counted, and the results are written to a CSV file.
7. **Logging**: Information about both included and excluded words, as well as subtitle details, is logged for later review.

## Future Plans

The project is highly personalized for my current setup, and thus is hard to be used by anyone else, nor is that the purpose. I am working on a version 2 that will include:
- Translations of the extracted words.
- Expressions and sayings (now just single words)
- An SQL-based implementation of the entire application.
- online hosting for the results of the analysis with possibilities to see frequencies of words and expressions not only in a single series but also across genres etc. 

