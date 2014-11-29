import nltk
import string
from nltk.util import ngrams
from nltk.corpus import gutenberg
from collections import Counter
import enchant
enchant_dict = enchant.Dict("en_GB")

POS_WORDS = nltk.FreqDist([word.lower() for word in gutenberg.words()])
STUDENT_WORDS = None
STUDENT_TRIGRAMS = None
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
    return set(w for w in words if w and (w in POS_WORDS or
        enchant_dict.check(w)))


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


def check_trigrams(word1, word3):
    trigrams = [trigram for (trigram, cnt) in STUDENT_TRIGRAMS.items()
            if trigram[0] == word1 and trigram[2] == word3 and cnt > 1]
    return len(trigrams) > 0 and max(trigrams, key=STUDENT_TRIGRAMS.get)[1]


def correct(word, prev_word=None, next_word=None):
    """Returns a corrected version of misspelled word"""
    edits1 = known(calc_edits1(word))
    edits2 = known(calc_edits2(word))
    if prev_word and next_word:
        trigram_word = check_trigrams(prev_word, next_word)
        if trigram_word and trigram_word in edits1 or trigram_word in edits2:
            return trigram_word
    data_words = set(word for word in edits1 if word in
            STUDENT_WORDS)
    if not data_words:
        data_words = set(word for word in edits2 if word in
                STUDENT_WORDS)
    if not data_words:
        data_words = closest_student_word(word)
    best_data_word = (data_words and max(data_words, key=STUDENT_WORDS.get))
    best_edit1 = (edits1 and max(edits1, key=POS_WORDS.get))
    if best_edit1 and best_data_word:
        data_word_score = calc_heuristic(best_data_word, word)
        edit1_score = calc_heuristic(best_edit1, word)
        if edit1_score > data_word_score:
            return best_edit1
    return (best_data_word or best_edit1  or
        (edits2 and max(edits2, key=POS_WORDS.get)) or word)


def should_check_word(word):
    """Returns true if word should be checked for spelling"""
    # don't correct anything that has digits or capital letters beyond 1st
    # letter (prob acronyms or some weird words)
    return word.isalpha() and not (word in STUDENT_WORDS or
            enchant_dict.check(word) or enchant_dict.check(word.lower()))


def correct_notice(notice_type, notice_id):
    """
    Returns dict with misspelled words as keys and their corrections as values
    """
    global POS_WORDS
    global STUDENT_WORDS
    global STUDENT_TRIGRAMS
    global last_notice_type
    if last_notice_type != notice_type:
        student_tokens = nltk.word_tokenize(file(
            '../transcriptions-notice%d/concatenated.txt'
            % notice_type).read().lower())
        STUDENT_WORDS = Counter(student_tokens)
        # Filter out uncommon words that aren't already in POS_WORDS
        for (word, cnt) in STUDENT_WORDS.items():
            if enchant_dict.check(word) or cnt >= 3:
                if word in POS_WORDS:
                    POS_WORDS[word] += cnt
                else:
                    POS_WORDS[word] = cnt
            else:
                del STUDENT_WORDS[word]
        STUDENT_TRIGRAMS = Counter(ngrams(student_tokens, 3))
        last_notice_type = notice_type
    student_response = (
        file('../transcriptions-notice%d/transcription_%s.txt'
            % (notice_type, notice_id)).read())
    student_response_words = nltk.word_tokenize(student_response)
    corrections = {}
    for (ind, word) in enumerate(student_response_words):
        if should_check_word(word):
            capitalized = word[0] in string.ascii_uppercase
            new_word = correct(word.lower(), ind > 0 and
                    student_response_words[ind -1].lower(),
                    ind < len(student_response_words) - 1
                    and student_response_words[ind + 1].lower())
            if new_word.lower() != word.lower():
                if capitalized:
                    new_word = new_word[0].upper() + new_word[1:]
                corrections[word] = new_word
    return corrections
