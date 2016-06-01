import glob
import re


class ProfanityChecker:
    def __init__(self):
        self.files=glob.glob("./profanityDictionaries/words_*.txt")
        self.words_list = set()

        self._load_words()

    def _load_words(self):
        """
        Loads all words from all files
        :return:
        """
        for filename in self.files:
            self.words_list.update([line.rstrip('\n').lower() for line in open(filename)])

    def validate(self, input_text):
        """
        Searches for a match in the string or substring
        :param input_text: string
        :return: boolean
        """
        split_string = re.findall(r"[\w']+", input_text.lower())

        for word in split_string:
            if word in self.words_list:
                return word

        return False

