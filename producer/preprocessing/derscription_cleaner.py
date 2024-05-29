import re
import nltk
from nltk.corpus import stopwords


class TextCleaner:
    def __init__(self, text: str) -> None:
        """
        Constructor for the text cleaner
        Params:
            test (str): text representing the description of a financial record
        """
        self.text = text.lower()
        self.stop_words = self.get_stop_words()

    def get_stop_words(self) -> set:
        """
        Get the stop words, downloading them if necessary.
        Returns:
            set with the stopwords
        """
        try:
            return set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords')
            return set(stopwords.words('english'))

    def remove_undesirable_characters(self) -> None:
        """
        Removes special characters and punctuation
        """
        # special character removal
        self.text = re.sub(r'[^a-z0-9\s]', '', self.text)
        # Insert space between letters and digits
        self.text = re.sub(r'(?<=\D)(?=\d)', ' ', self.text)

    def remove_stop_words(self) -> None:
        """
        Removes the stopwords
        """
        self.text = ' '.join([word for word in self.text.split() if word not in self.stop_words])

    def clean_description(self) -> str:
        """
        Computes all the previous cleaning steps
        """
        self.remove_undesirable_characters()
        self.remove_stop_words()
        return self.text


    


    

    

    