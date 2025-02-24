import unicodedata

from sudachipy import tokenizer
from sudachipy import dictionary
import re
import regex

tokenizer_obj = dictionary.Dictionary(dict="full").create()  # sudachidict_full
mode = tokenizer.Tokenizer.SplitMode.B
#Mode C = keeps whole word intact, Mode A breaks the word as much as it can, B in the middle



'''------------------------------Utilities-------------------------------------'''

def hiragana_to_katakana(hiragana_text):
    # Create a translation table mapping hiragana to katakana
    hiragana_chars = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわをん"
    katakana_chars = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヲン"

    translation_table = str.maketrans(hiragana_chars, katakana_chars)

    # Use translate to convert hiragana to katakana
    katakana_text = hiragana_text.translate(translation_table)

    return katakana_text

def has_kanji(input_string):
    # Define the Unicode range for Kanji characters

    kanji_pattern = re.compile(r'[\u4E00-\u9FFF]+')

    # Check if the pattern matches the input string
    return bool(kanji_pattern.search(input_string))

def has_hiragana(input_string):
    # Define a regular expression pattern for matching Hiragana characters
    hiragana_pattern = re.compile(r'[\u3040-\u309F]+')

    # Use re.search() to check for a match
    match = hiragana_pattern.search(input_string)

    # Return True if a match is found, False otherwise
    return bool(match)


def contains_japanese_text(text):

    # Regular expression pattern to match Japanese hiragana, katakana, and kanji characters
    japanese_pattern = r'[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}]'

    if regex.search(japanese_pattern, text):
        return True
    else:
        return False

def word_cat_to_eng(cat_in_jpn):
    if cat_in_jpn == "代名詞":
        return "Pronoun"
    elif cat_in_jpn == "副詞":
        return "Adverb"
    elif cat_in_jpn == "動詞":
        return "Verb"
    elif cat_in_jpn == "名詞":
        return "Noun"
    elif cat_in_jpn == "形容詞":
        return "Adjective"
    elif cat_in_jpn == "形状詞":
        return "Adjectival Noun"
    elif cat_in_jpn == "感動詞":
        return "Interjection"
    elif cat_in_jpn == "接続詞":
        return "Conjunction"
    elif cat_in_jpn == "接頭辞":
        return "Prefix"
    elif cat_in_jpn == "連体詞":
        return "Adnominal Adjective"
    elif cat_in_jpn == "助詞":
        return "Postpositional particle"
    elif cat_in_jpn == "接尾辞":
        return "Suffix"
    elif cat_in_jpn == "助動詞":
        return "Auxiliary verb"
    else: return cat_in_jpn

'''-----------------------------Tokenizer methods--------------------------------'''


def nominalize_word(word):
    nominalized_word = tokenizer_obj.tokenize(word, mode)[0].normalized_form()
    return nominalized_word


def analyze_word_jlpt(word):
    words_raw_in_line = tokenizer_obj.tokenize(word, mode)
    if len(words_raw_in_line) == 1:
        word_normalized = words_raw_in_line[0].normalized_form()

        if has_kanji(word):
            return word
        else:
            return word_normalized
    else:
        word_transformed = ""
        if has_kanji(word) and word[0] != "お":
            return word
        else:
            for word in words_raw_in_line:
                word_transformed += word.normalized_form()
            return word_transformed


def get_word_normalizedform_jlpt(word):
    words_raw_in_line = tokenizer_obj.tokenize(word, mode)
    if len(words_raw_in_line) == 1:
        word_reading = words_raw_in_line[0].normalized_form()
        return word_reading
    else:
        word_combined = ""
        for word in words_raw_in_line:
            word_combined += word.normalized_form()
        return word_combined


def get_word_reading(word):
    word_reading = tokenizer_obj.tokenize(word, mode)[0].reading_form()
    return word_reading


def get_word_dictform(word):
    word_reading = tokenizer_obj.tokenize(word, mode)[0].dictionary_form()
    return word_reading


def get_word_dictform_jlpt(word):
    words_raw_in_line = tokenizer_obj.tokenize(word, mode)
    if len(words_raw_in_line) == 1:
        word_reading = words_raw_in_line[0].dictionary_form()
        return word_reading
    else:
        word_combined = ""
        for word in words_raw_in_line:
            word_combined += word.dictionary_form()
        return word_combined


def get_word_category(word):
    m = tokenizer_obj.tokenize(word, mode)[0]
    category = m.part_of_speech()
    return category


def words_in_line_test(line):
    line = remove_weird_characters(line)
    words_in_line = []

    # Go through words and find the ones we're looking for
    words_raw_in_line = tokenizer_obj.tokenize(line, mode)
    for word_idx, word_raw in enumerate(words_raw_in_line):

        word_as_is = word_raw.surface()
        print(f"WORD: {word_as_is}")

        word_dictform = word_raw.dictionary_form()
        print(f"\tdictionary form: {word_dictform}")

        word_reading = word_raw.reading_form()
        print(f"\treading {word_reading}")

        word_normalized = word_raw.normalized_form()
        print(f"\tnormalized: {word_normalized}")

        word_cat = word_raw.part_of_speech() # [0] main category [1] sub category
        print(f"\tcategory: {word_cat}\n")




'''-----------------------------Program related SudachiPy fixing methods--------------------------------'''



# Laughter not picked up by the language processor filter
def is_laughter(word, word_cat):
    if word_cat != "名詞" or has_kanji(word):
        return False

    laughter_starters = ["は", "ふ", "へ", "く", "ク", "ハ", "フ", "ヘ", "ほ", "ホ"]
    for laughter_starter in laughter_starters:
        if word == laughter_starter or word == laughter_starter + "ッ" or word == laughter_starter + "っ":
            return True

        if laughter_starter == "は":
            laughter_found = re.search(f"^({laughter_starter}|あ)((っ{laughter_starter})+|{laughter_starter}+)$", word)
        elif laughter_starter == "ハ":
            laughter_found = re.search(f"^({laughter_starter}|ア)((っ{laughter_starter})+|{laughter_starter}+)$", word)
        elif laughter_starter == "ふ":
            laughter_found = re.search(f"^({laughter_starter}|う)((っ{laughter_starter})+|{laughter_starter}+)$", word)
        elif laughter_starter == "フ":
            laughter_found = re.search(f"^({laughter_starter}|ウ)((っ{laughter_starter})+|{laughter_starter}+)$", word)
        elif laughter_starter == "へ":
            laughter_found = re.search(f"^({laughter_starter}|え)((っ{laughter_starter})+|{laughter_starter}+)$", word)
        elif laughter_starter == "ヘ":
            laughter_found = re.search(f"^({laughter_starter}|エ)((っ{laughter_starter})+|{laughter_starter}+)$", word)
        elif laughter_starter == "ほ":
            laughter_found = re.search(f"^({laughter_starter}|)お((っ{laughter_starter})+|{laughter_starter}+)$", word)
        elif laughter_starter == "ホ":
            laughter_found = re.search(f"^({laughter_starter}|オ)((っ{laughter_starter})+|{laughter_starter}+)$", word)
        else:
            laughter_found = re.search(
                f"^{laughter_starter}(({laughter_starter}*)|({laughter_starter}っ*)|({laughter_starter}ッ){laughter_starter})$", word)

        if laughter_found:
            return True

    return False


def is_single_letter_or_pattern(word_normalized, word_cat):

    pointless_words = [
        'あ', 'い', 'う', 'え', 'お', 'ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ', 'っ',
        'か', 'が', 'き', 'ぎ', 'く', 'ぐ', 'け', 'げ', 'こ', 'ご', 'さ', 'ざ', 'し', 'じ', 'す', 'ず',
        'せ', 'ぜ', 'た', 'だ', 'ち', 'ぢ', 'つ', 'づ', 'て', 'で', 'と', 'ど', 'な', 'に', 'ぬ', 'ね', 'の',
        'は', 'ば', 'ぱ', 'ひ', 'び', 'ぴ', 'ふ', 'ぶ', 'ぷ', 'へ', 'べ', 'ぺ', 'ほ', 'ぼ', 'ま', 'み', 'む',
        'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'ん',
        'ア', 'イ', 'ウ', 'エ', 'オ', 'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ッ',
        'カ', 'ガ', 'キ', 'ギ', 'ク', 'グ', 'ケ', 'ゲ', 'コ', 'ゴ', 'サ', 'ザ', 'シ', 'ジ', 'ス', 'ズ',
        'セ', 'ゼ', 'タ', 'ダ', 'チ', 'ヂ', 'ツ', 'ヅ', 'テ', 'デ', 'ト', 'ド', 'ナ', 'ニ', 'ヌ', 'ネ', 'ノ',
        'ハ', 'バ', 'パ', 'ヒ', 'ビ', 'ピ', 'フ', 'ブ', 'プ', 'ヘ', 'ベ', 'ペ', 'ホ', 'ボ', 'マ', 'ミ', 'ム',
        'メ', 'モ', 'ヤ', 'ユ', 'ヨ', 'ラ', 'リ', 'ル', 'レ', 'ロ', 'ワ', 'ン',
    ]

    if word_cat != "名詞" or has_kanji(word_normalized):
        return False
    else:
        if (
                word_normalized in pointless_words
                or word_normalized + "ッ" in pointless_words
                or word_normalized + "っ" in pointless_words
        ):
            return True

        for p_w in pointless_words:
            p_w_found = re.search(fr"^{p_w}[{p_w}]?[{p_w}っッー]$", word_normalized)
            if p_w_found:
                return True
        return False





# Check that word is correct for the purpose of the program

def is_right_word_category(word_normalized, word_cat_main, word_cat_sub, prev_word_cat_main, prev_word_cat_sub, prev_word_cat_sub2, prev_word_cat_sub4):

    def is_accepteable_kandoushi(word_norm):

        if word_norm[:3] == "ごめん" or word_norm == "すいません" or word_norm == "さーせん" or word_norm == "サーセン"\
        or word_norm == "有り難う" or word_norm == "さようなら"\
        or word_norm == "はい" or word_norm == "うん" or word_norm == "否" or word_norm == "いいえ" or word_norm == "ううん" or word_norm == "ええ"\
        or word_norm == "今日は" or word_norm == "御早う" or word_norm == "ごきげんよう" or word_norm[:4] == "おやすみ" or word_norm[:4] == "おかえり":
            return True
        else:
            return False

    def is_nai_after_keiyoushi_or_ja():
        if word_normalized == "無い" and (prev_word_cat_main == "形容詞" or prev_word_cat_sub4 == "助動詞-ダ"):
            return True
        else:
            return False
        
    def is_suru_after_noun():
        if word_normalized == "為る" and prev_word_cat_sub2 == "サ変可能":
            return True
        else:
            return False
        
    def is_iru_after_te():
        if word_normalized == "居る" and prev_word_cat_sub == "接続助詞":
            return True
        else:
            return False
    def is_aru_after_ja():
        if word_normalized == "有る" and prev_word_cat_sub4 == "助動詞-ダ":
            return True
        else:
            return False

    if (
            (word_cat_main == "動詞" and not is_suru_after_noun() and not is_iru_after_te() and not is_aru_after_ja())
            or (word_cat_main == "形容詞" and not is_nai_after_keiyoushi_or_ja())
            or (word_cat_main == "名詞" and word_cat_sub != "固有名詞" and word_cat_sub != "数詞")
            or word_cat_main == "副詞"
            or (word_cat_main == "感動詞" and is_accepteable_kandoushi(word_normalized))
            or word_cat_main == "代名詞"
            or word_cat_main == "形状詞"
            or word_cat_main == "連体詞"
    ):
        return True
    else:
        return False




def remove_weird_characters(input_string):

    # Remove symbols that lead to a crash (bug probably)
    if "…" in input_string:
        input_string = input_string.replace("…", "。")

    # Use unicodedata to remove non-printable Unicode characters
    cleaned_chars = [char for char in input_string if unicodedata.category(char) != 'Cf']
    cleaned_string = ''.join(cleaned_chars)

    return cleaned_string

# The reading that comes from sudachipy is conjugated word reading
def get_unconjugated_word_reading(word_normalized, word_dictform):

    if not has_kanji(word_normalized):
        return hiragana_to_katakana(word_normalized)
    if not has_kanji(word_dictform):
        return hiragana_to_katakana(word_dictform)
    else:
        return get_word_reading(word_normalized)

# remove nobashibou and ee lengthenings in adjectives, return appropriate dict_form
def remove_inappropriate_lenthenings(word_normalized, word_dictform, word_cat_main):

    kana_syllable_to_vowel = {
        # Hiragana
        'あ': 'あ', 'い': 'い', 'う': 'う', 'え': 'え', 'お': 'う',
        'か': 'あ', 'き': 'い', 'く': 'う', 'け': 'え', 'こ': 'う',
        'さ': 'あ', 'し': 'い', 'す': 'う', 'せ': 'え', 'そ': 'う',
        'た': 'あ', 'ち': 'い', 'つ': 'う', 'て': 'え', 'と': 'う',
        'な': 'あ', 'に': 'い', 'ぬ': 'う', 'ね': 'え', 'の': 'う',
        'は': 'あ', 'ひ': 'い', 'ふ': 'う', 'へ': 'え', 'ほ': 'う',
        'ま': 'あ', 'み': 'い', 'む': 'う', 'め': 'え', 'も': 'う',
        'や': 'あ', 'ゆ': 'う', 'よ': 'う',
        'ら': 'あ', 'り': 'い', 'る': 'う', 'れ': 'え', 'ろ': 'う',

        # Daku-on syllables (Hiragana)
        'が': 'あ', 'ぎ': 'い', 'ぐ': 'う', 'げ': 'え', 'ご': 'う',
        'ざ': 'あ', 'じ': 'い', 'ず': 'う', 'ぜ': 'え', 'ぞ': 'う',
        'だ': 'あ', 'ぢ': 'い', 'づ': 'う', 'で': 'え', 'ど': 'う',
        'ば': 'あ', 'び': 'い', 'ぶ': 'う', 'べ': 'え', 'ぼ': 'う',
        'ぱ': 'あ', 'ぴ': 'い', 'ぷ': 'う', 'ぺ': 'え', 'ぽ': 'う',

        # Small Kana (Hiragana)
        'ゃ': 'あ', 'ゅ': 'う', 'ょ': 'う',

        # Katakana
        'ア': 'あ', 'イ': 'い', 'ウ': 'う', 'エ': 'え', 'オ': 'う',
        'カ': 'あ', 'キ': 'い', 'ク': 'う', 'ケ': 'え', 'コ': 'う',
        'サ': 'あ', 'シ': 'い', 'ス': 'う', 'セ': 'え', 'ソ': 'う',
        'タ': 'あ', 'チ': 'い', 'ツ': 'う', 'テ': 'え', 'ト': 'う',
        'ナ': 'あ', 'ニ': 'い', 'ヌ': 'う', 'ネ': 'え', 'ノ': 'う',
        'ハ': 'あ', 'ヒ': 'い', 'フ': 'う', 'ヘ': 'え', 'ホ': 'う',
        'マ': 'あ', 'ミ': 'い', 'ム': 'う', 'メ': 'え', 'モ': 'う',
        'ヤ': 'あ', 'ユ': 'う', 'ヨ': 'う',
        'ラ': 'あ', 'リ': 'い', 'ル': 'う', 'レ': 'え', 'ロ': 'う',

        # Daku-on syllables (Katakana)
        'ガ': 'あ', 'ギ': 'い', 'グ': 'う', 'ゲ': 'え', 'ゴ': 'う',
        'ザ': 'あ', 'ジ': 'い', 'ズ': 'う', 'ゼ': 'え', 'ゾ': 'う',
        'ダ': 'あ', 'ヂ': 'い', 'ヅ': 'う', 'デ': 'え', 'ド': 'う',
        'バ': 'あ', 'ビ': 'い', 'ブ': 'う', 'ベ': 'え', 'ボ': 'う',
        'パ': 'あ', 'ピ': 'い', 'プ': 'う', 'ペ': 'え', 'ポ': 'う',

        # Small Kana (Katakana)
        'ャ': 'あ', 'ュ': 'う', 'ョ': 'う',
    }

    if ("ー" not in word_dictform and word_cat_main != "形容詞"
    or ("ー" in word_dictform and not has_hiragana(word_normalized))
    ):
        return word_dictform

    if (
            word_dictform == "形容詞" and
            ("え" in word_dictform[-1] or "エ" in word_dictform[-1])
    ):
        word_dictform = get_word_reading(word_normalized)


    elif word_dictform[-1] != "ー":
        word_dictform == word_dictform.replace("ー", "")

    elif word_dictform[-1] == "ー" and word_cat_main == "名詞":
        word_dictform = get_word_reading(word_normalized)

    elif word_dictform[-1] == "ー" and word_cat_main != "名詞":
        word_dictform = word_dictform.replace("ー", kana_syllable_to_vowel[word_dictform[-2]])

    return word_dictform


def fix_common_w_processor_problems(word_cat_main, word_normalized):

    # Check for adverbs such as ぐっと
    if word_cat_main == "副詞" and word_normalized[-1] == "っ":
        word_normalized = str(word_normalized) + "と"

    return word_normalized

'''----------------------------------MAIN RELATED CODE------------------------------------------------'''


def get_words_in_line(line, logger_not_extract=None, episode=None, row_idx=None):
    line = remove_weird_characters(line)
    words_in_line = []

    # Go through words and find the ones we're looking for
    words_raw_in_line = tokenizer_obj.tokenize(line, mode)
    for word_idx, word_raw in enumerate(words_raw_in_line):
        if word_raw is None:
            continue

        word_dictform = word_raw.dictionary_form()
        word_normalized = word_raw.normalized_form()
        word_cat_main = word_raw.part_of_speech()[0]
        word_cat_sub = word_raw.part_of_speech()[1]

        prev_word_cat_main = None
        prev_word_cat_sub = None
        prev_word_cat_sub2 = None
        prev_word_cat_sub4 = None

        
        if word_idx > 0:
            prev_word_cat_main = words_raw_in_line[word_idx - 1].part_of_speech()[0]
            prev_word_cat_sub = words_raw_in_line[word_idx - 1].part_of_speech()[1]
            prev_word_cat_sub2 = words_raw_in_line[word_idx - 1].part_of_speech()[2]
            prev_word_cat_sub4 = words_raw_in_line[word_idx - 1].part_of_speech()[4]


        # Check that word is a category we're looking for
        if (is_right_word_category(word_normalized, word_cat_main, word_cat_sub, prev_word_cat_main, prev_word_cat_sub, prev_word_cat_sub2, prev_word_cat_sub4)
            and not is_laughter(word_normalized, word_cat_main)
            and not is_single_letter_or_pattern(word_normalized, word_cat_main)
        ):

            word_normalized = fix_common_w_processor_problems(word_cat_main, word_normalized)
            word_dictform = remove_inappropriate_lenthenings(word_normalized, word_dictform, word_cat_main)
            word_reading = get_unconjugated_word_reading(word_normalized, word_dictform)
            words_in_line.append({"word_normalized": str(word_normalized), "word_reading": str(word_reading), "word_cat": str(word_cat_main), "word_dictform": str(word_dictform)})


        # If word discarded, log it
        else:
            if logger_not_extract is None:
                pass
            elif word_cat_main != "補助記号" and word_cat_main != "空白" and word_cat_main != "記号":
                logger_not_extract.add_line_not_extracted_from({"word": word_dictform, "episode": episode, "row": row_idx + 1, "word_cat": word_cat_to_eng(word_cat_main)})

    return words_in_line







