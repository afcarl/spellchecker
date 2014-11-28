import nltk
import string
from nltk.util import ngrams
from collections import Counter
import enchant
enchant_dict = enchant.Dict("en_GB")

POS_WORDS = None
STUDENT_WORDS = None
last_notice_type = None

def calc_edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in
           string.ascii_lowercase if b]
   inserts    = [a + c + b     for a, b in splits for c in
           string.ascii_lowercase]
   return set(deletes + transposes + replaces + inserts)


def calc_edits2(word):
    return set(e2 for e1 in calc_edits1(word) for e2 in calc_edits1(e1))


def known(words):
    return set(w for w in words if w in POS_WORDS and POS_WORDS[w] > 1)


def closest_student_word(word):
   """Finds closest word in student data"""
   closest_word = None
   best_score = 0
   for student_word in STUDENT_WORDS:
       score = calc_heuristic(student_word, word)
       if score > best_score:
           best_score = score
           closest_word = student_word
   unique_letters = len(set(word))
   if best_score > unique_letters - 2:
       return set([closest_word])
   return set()


def calc_heuristic(word1, word2):
    """
    Scores similarity between word1 & word2 by counting common unique letters
    """
    return len(set(word1).intersection(set(word2)))


def correct(word):
    """Returns a corrected version of misspelled word"""
    edits1 = known(calc_edits1(word))
    edits2 = known(calc_edits2(word))
    data_words = set(word for word in edits1 if word in
            STUDENT_WORDS)
    if not data_words:
        data_words = set(word for word in edits2 if word in
                STUDENT_WORDS)
    if not data_words:
        data_words = closest_student_word(word)
    best_data_word = (data_words and max(data_words, key=STUDENT_WORDS.get))
    return (best_data_word or (edits1 and max(edits1, key=POS_WORDS.get)) or
        (edits2 and max(edits2, key=POS_WORDS.get)) or word)


def should_check_word(word):
    """Returns true if word should be checked for spelling"""
    # don't correct anything that has digits or capital letters beyond 1st
    # letter (prob acronyms or some weird words)
    return not (word.lower() in POS_WORDS or word[0].isdigit() or
            any(letter.isdigit() or letter in string.ascii_uppercase
                for letter in word[1:]))


def correct_notice(notice_type, notice_id):
    """
    Returns dict with misspelled words as keys and their corrections as values
    """
    global POS_WORDS
    global STUDENT_WORDS
    global last_notice_type
    if last_notice_type != notice_type:
        POS_WORDS = Counter(nltk.word_tokenize(file('big.txt').read()))
        STUDENT_WORDS = Counter(nltk.word_tokenize(file(
            '../transcriptions-notice%d/concatenated.txt'
            % notice_type).read().lower()))
        # Filter out uncommon words that aren't already in POS_WORDS
        for (word, cnt) in STUDENT_WORDS.items():
            if not enchant_dict.check(word) and cnt < 3:
                del STUDENT_WORDS[word]
        POS_WORDS += STUDENT_WORDS
        last_notice_type = notice_type
    student_response = (
        file('../transcriptions-notice%d/transcription_%s.txt'
            % (notice_type, notice_id)).read())
    student_response_words = nltk.word_tokenize(student_response)
    corrections = {}
    for word in student_response_words:
        if should_check_word(word):
            capitalized = word[0] in string.ascii_uppercase
            new_word = correct(word.lower())
            if new_word.lower() != word.lower():
                if capitalized:
                    new_word = new_word[0].upper() + new_word[1:]
                corrections[word] = new_word
    return corrections
