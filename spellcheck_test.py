import unittest
import spellcheck

class TestSpellChecker(unittest.TestCase):
    """Tests for Spellcheck"""

    notice_nums = ['1587', '1591', '1600', '1605', '1611', '1618', '1625',
            '1634', '1641', '1647', '1655', '1664', '1670', '1677', '1682',
            '1685', '1692', '1696', '1710', '1719', '1723', '1731', '1749',
            '1752', '1763', '1769', '1781', '1793']
    errors = {
        '1600': {
            'plase': 'please'
        },
        '1605': {
            'Semptember': 'September'
        },
        '1618': {
            'competion': 'competition',
            'Jantra': 'Janta'
        },
        '1625': {
            'seceratory': 'secretary'
        },
        '1641': {
            'intreasted': 'interested'
        },
        '1647': {
            'participat': 'participate'
        },
        '1655': {
            'inofrming': 'informed',
            'deparnment': 'department'
        },
        '1677': {
            'parcipate': 'participate',
            'porogram': 'program'
        },
        '1685': {
            'futhur': 'further'
        },
        '1692': {
            'intrested': 'interested',
            'Septmber': 'September',
            'subbmited': 'submitted',
            'Agust': 'August',
            'secuatry': 'secretary',
            'fore': 'for',
            'undersing': 'undersign',
            'competation': 'competition'
        },
        '1696': {
            'Copettion': 'Competition',
            'Maida': 'Maidan',
            'stember': 'September'
        },
        '1719': {
            'sheduled': 'scheduled'
        },
        '1731': {
            'shool': 'school',
            'participat': 'participate',
            'secreatary': 'secretary'
        },
        '1752': {
            'Naintal': 'National',
            'Nainatal': 'National',
            'competiotion': 'competition'
        }
    }

    def test_spell_check(self):
        corrected_words = 0
        incorrectly_corrected_words = 0
        unnecessarily_corrected_words = 0
        for notice_num in self.notice_nums:
            corrections = spellcheck.correct_notice(notice_num)
            if notice_num not in self.errors and corrections:
                for (word, new_word) in corrections.iteritems():
                    print(('Incorrectly changed already correct word %s to %s '
                            'in notice %s') % (word, new_word, notice_num))
                    unnecessarily_corrected_words += 1
            elif notice_num in self.errors:
                notice_errors = self.errors[notice_num]
                for (word, new_word) in corrections.iteritems():
                    if word not in notice_errors:
                        print(
                            ('Incorrectly changed already correct word %s to '
                            '%s in notice %s') % (word, new_word, notice_num))
                        unnecessarily_corrected_words += 1
                    else:
                        if notice_errors[word] == new_word:
                            corrected_words += 1
                        else:
                            print(('Incorrectly changed misspelled word %s '
                                'to %s in notice %s') %
                                (word, new_word, notice_num))
                            incorrectly_corrected_words += 1
                unchanged_mistakes = {word for word in notice_errors.keys() if
                        word not in corrections}
                for word in unchanged_mistakes:
                    print('Did not correct misspelled word %s in notice %s' %
                            (word, notice_num))
                incorrectly_corrected_words += len(unchanged_mistakes)
        print(('Corrected words: %d, Incorrectly corrected words: %d,'
            ' Unnecessarily corrected words: %d') % (corrected_words,
            incorrectly_corrected_words, unnecessarily_corrected_words))

if __name__ == '__main__':
    unittest.main()
