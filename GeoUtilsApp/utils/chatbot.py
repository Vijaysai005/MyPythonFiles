# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 22:00:00 2018

@author: Vijayasai
"""
from chatterbot import ChatBot

class ChatBox(ChatBot):

    def __init__(self):
        ChatBot.__init__(self, "Hearty", storage_adapter="chatterbot.storage.MongoDatabaseAdapter", trainer="chatterbot.trainers.ChatterBotCorpusTrainer")
        self.train('chatterbot.corpus.english')

    def get_output(self, input_text):
        answer = self.get_response(input_text)
        data  = str(answer)
        return "{}".format(data)

    def do_train(self, query, response):
        self.train_me(query,response)  

if __name__ == "__main__":
    pass

