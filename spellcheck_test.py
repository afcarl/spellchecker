import unittest
import spellcheck

class TestSpellChecker(unittest.TestCase):
    """Tests for Spellcheck"""

    notice0_ids  = ['1587', '1591', '1600', '1605', '1611', '1618', '1625',
            '1634', '1641', '1647', '1655', '1664', '1670', '1677', '1682',
            '1685', '1692', '1696', '1710', '1719', '1723', '1731', '1749',
            '1752', '1763', '1769', '1781', '1793']
    notice0_errors = {
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
            'participat': 'participate',
            'wl': 'who'
        },
        '1655': {
            'inofrming': 'informing',
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
    notice1_ids = ['2042', '2048', '2061', '2069', '2073', '2083', '2091',
    '2100', '2106', '2113', '2121', '2129', '2139', '2147', '2173', '2178',
    '2194', '2202', '2217', '2231', '2235', '2246', '2255', '2264', '2272']
    notice1_errors = {
            '2048': {
                'rebok':'Reebok'
            },
            '2061': {
                'occusion': 'occasion',
                'Rasha': 'Raksha'
            },
            '2069': {
                'feild': 'field',
                'Yhere': 'Where',
                'rebook': 'Reebok',
                'town-tirn': 'town-turn'
            },
            '2073': {
                'hodiay': 'holiday',
                'hoiday': 'holiday',
            },
            '2083': {
                'Yestaday': 'Yesterday'
            },
            '2091': {
                'wigh': 'white',
                'trite': 'treat'
            },
            '2100': {
                'Tun': 'Turn'
            },
            '2106': {
                'colourfull': 'colourful'
            },
            '2113': {
                'ocassion': 'occasion'
            },
            '2173': {
                'levove': 'leave',
                'near-by': 'nearby'
            },
            '2178': {
                'repica': 'replica',
                'guatiar': 'guitar'
            },
            '2217': {
                'eving': 'evening',
                'bak': 'back'
            },
            '2231': {
                'occassion': 'occasion',
                'Bhandhan': 'Bandhan'
            },
            '2235': {
                'occassion': 'occasion',
                'clases': 'classes'
            },
            '2255': {
                'playgoround': 'playground'
            }
    }
    notice_ids = [notice0_ids, notice1_ids]
    notice_errors = [notice0_errors, notice1_errors]

    def check_notice_correction(self, notice_type):
        corrected_words = 0
        incorrectly_corrected_words = 0
        unnecessarily_corrected_words = 0
        for notice_id in self.notice_ids[notice_type]:
            corrections = spellcheck.correct_notice(notice_type, notice_id)
            if notice_id not in self.notice_errors[notice_type] and corrections:
                for (word, new_word) in corrections.iteritems():
                    print(('Incorrectly changed already correct word %s to %s '
                            'in notice %s') % (word, new_word, notice_id))
                    unnecessarily_corrected_words += 1
            elif notice_id in self.notice_errors[notice_type]:
                errors = self.notice_errors[notice_type][notice_id]
                for (word, new_word) in corrections.iteritems():
                    if word not in errors:
                        print(
                            ('Incorrectly changed already correct word %s to '
                            '%s in notice %s') % (word, new_word, notice_id))
                        unnecessarily_corrected_words += 1
                    else:
                        if errors[word] == new_word:
                            corrected_words += 1
                        else:
                            print(('Incorrectly changed misspelled word %s '
                                'to %s in notice %s') %
                                (word, new_word, notice_id))
                            incorrectly_corrected_words += 1
                unchanged_mistakes = {word for word in errors.keys() if
                        word not in corrections}
                for word in unchanged_mistakes:
                    print('Did not correct misspelled word %s in notice %s' %
                            (word, notice_id))
                incorrectly_corrected_words += len(unchanged_mistakes)
        print(('Corrected words: %d, Incorrectly corrected words: %d,'
            ' Unnecessarily corrected words: %d') % (corrected_words,
            incorrectly_corrected_words, unnecessarily_corrected_words))

    def test_spell_check(self):
        self.check_notice_correction(0)
        self.check_notice_correction(1)

if __name__ == '__main__':
    unittest.main()
