import json

import nltk
from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
from string import punctuation
from datetime import datetime
from random import randint

stemmer = LancasterStemmer()

class App:

    def __init__(self):
        self.template_filename = "templates\\base.json"
        self.context = {}
        self.__responses = self.load_responses ()

    def load_template (self):
        raw = {}
        try:
            with open (self.template_filename, "r") as file:
                intents = json.load (file)["intents"]
                for intent in intents:
                    class_name = intent['name']
                    raw[class_name] = []
                    for sentence in intent['sentences']:
                        for word in word_tokenize(sentence):
                            if word not in punctuation:
                                raw[class_name].append (stemmer.stem(word.lower()))
        except Exception:
            raise Exception("An error occured while trying to load template file: ", self.template_filename)

        finally:
            return raw

    @staticmethod
    def get_moment():
        """
        Used to generate appropriate salutation. Returns 'morning', 'afternoon' 
        or 'evening', based on the actual system time
        """
        hour = datetime.now().hour
        if hour >= 5 and hour <= 12:
            moment = "morning"
        elif hour > 12 and hour <= 18:
            moment = "afternoon"
        else:
            moment = "evening"
        return moment

    def load_responses (self):
        responses = []
        try:
            with open (self.template_filename, "r") as file:
                for resp in json.load (file)["responses"]:
                    responses.append ( { resp["type"]: resp["answers"] })
        except Exception as e: 
            print ("An error occured while trying to load responses from file [", self.template_filename, "]\n\t", e)
        finally:
            return responses

    def execute (self, doc):
        intent = doc._.intent
        moment = self.get_moment()
        r = str()
        for resp in self.__responses:
            if intent in resp:
                r = resp[intent][ randint( 0, len(resp[intent])-1 ) ]
                break
        # print (intent)
        if intent == "greetings":
            return {
                "message": r.format(m=moment),
                "state": 1
                }
        else:
            return {
                "message": r,
                "state": 1
                }

