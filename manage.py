#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import string
import spacy
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

def spacy_tokenizer(sentence):
    punctuations = string.punctuation

    nlp = spacy.load('en_core_web_sm')
    stop_words = STOP_WORDS

    parser = English()

    mytokens = parser(nlp(sentence))
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
    mytokens = [ word for word in mytokens if word not in stop_words and word not in punctuations ]

    return mytokens

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
