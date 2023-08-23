from anonymizer import liste_pays, textAnonyms, anonymiser_mot
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from pydantic import BaseModel
from faker import Faker
import os
import pandas as pd
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')

def initialiser():
    csv_file_path = "words.csv"

    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
        print(f"Fichier CSV '{csv_file_path}' supprimé.")

    empty_dataframe = pd.DataFrame(columns=["original", "anonymous"])

    empty_dataframe.to_csv(csv_file_path, index=False)

    print(f"Fichier CSV '{csv_file_path}' vidé et initialisé.")




def anonymiser_paragraphe(paragraphe):

    phrase = paragraphe
    phrase = phrase.replace(".", ". ")
    phrase = phrase.replace(",", ", ")

    tokens = word_tokenize(phrase, language="french")
    tags = pos_tag(tokens )
    entites_nommees = []

    stop_words = set(stopwords.words('french'))
    pronoms_possessifs = ["mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses", "notre", "votre", "leur", "leurs","merci","alors","fh","intervention"]
    stop_words.update(pronoms_possessifs)

    for word, tag in tags:

        if word.lower() in liste_pays:
            entites_nommees.append(("COUNTRY", word))
        elif tag == "NNP" and "DS" in word :
            entites_nommees.append(("NUMBER", word))
        elif tag == "NNP" and word.isupper() and word.lower() not in stop_words:
            entites_nommees.append(("ORGANIZATION", word))
        elif tag == "NNP" and word.lower() not in stop_words:
            entites_nommees.append(("PERSON", word))
        elif tag == "CD" and "/" in word :
            entites_nommees.append(("DATE", word))
        elif tag == "CD":
            entites_nommees.append(("NUMBER", word))
        elif tag == "NNP" and word.lower() not in stop_words:
            entites_nommees.append(("LOCATION", word))
    print("Entités nommées :", entites_nommees)


    for entity_type, entity_value in entites_nommees:
        text = textAnonyms(originalText=entity_value, textFormat=entity_type)
        paragraphe = paragraphe.replace(entity_value, anonymiser_mot(text))

    return paragraphe

def desanonymiser_paragraphe(anonymous_paragraphe):
    anonymisedData = pd.read_csv("words.csv", dtype={"original": str, "anonymous": str})
    for index, row in anonymisedData.iterrows():

        anonymous_paragraphe = anonymous_paragraphe.replace(row["anonymous"],row["original"])
    return anonymous_paragraphe
