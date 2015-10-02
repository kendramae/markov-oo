from sys import argv
from random import choice


class SimpleMarkovGenerator(object):

    def read_files(self, file_names):
        """Given a list of files, returns list of content as text string for each file"""
        text_string_list = []
        for file_name in file_names:
            file_text = open(file_name).read()
            text_string_list.append(file_text)
        
        self.text_string_list = text_string_list
        self.make_chains() #calling make chains so we don't have to call both separately

    def make_chains(self):
        """Takes input text as string list; stores chains."""
        
        chains = {}
        for text_string in self.text_string_list:
            words = text_string.split()
            for i in range(len(words) - 2):
                key = (words[i], words[i+1])
                value = words[i+2]

                if key not in chains:
                    chains[key] = []

                chains[key].append(value)

        self.chains = chains

    def make_text_list(self):
        """Takes dictionary of markov chains; returns random text in a list."""

        chains = self.chains

        key = choice(chains.keys())
        while not key[0].istitle():
            key = choice(chains.keys())
        
        words = [key[0], key[1]]
        while key in chains:

        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

            word = choice(chains[key])
            words.append(word)
            key = (key[1], word)

        self.text_list = words


    def make_text(self, max_chars=None):
        """ This calls make_text_list to receive a string of text as a list 
        and returns string of text at or under max characters
        ending with punction."""

        self.make_text_list()
        text_list = self.text_list

        words_to_use = []

        # Controlling for max characters.
        if max_chars:
            length_of_text = 0
            while length_of_text < max_chars:
                for word in text_list:
                    length_of_text += len(word) + 1
                    if length_of_text > max_chars:
                        break
                    words_to_use.append(word)
                break
        else:
            words_to_use = text_list

        # Controlling for punctuation.
        text_to_print = " ".join(words_to_use)
        x = len(text_to_print) - 1
        while x > 0:
            if text_to_print[x] == "?":
                break
            elif text_to_print[x] == ".":
                break
            elif text_to_print[x] == "'":
                break
            elif text_to_print[x] == "!":
                break
            elif text_to_print == "\"":
                break
            else:
                x -= 1

        text_to_print = text_to_print[:x+1]

        return text_to_print



class TweetableMarkovGenerator(SimpleMarkovGenerator):
        max_chars = 140
        def tweet(self):
            return super(TweetableMarkovGenerator, self).make_text(self.max_chars)



if __name__ == "__main__": # if this .py is the main program running, 
                           # the code below this point will start automatically
    # we should get list of filenames from sys.argv
    # we should make an instance of the class
    # we should call the read_files method with the list of filenames
    # we should call the make_text method 5x
    file_names = argv[1:]
    markov_machine = SimpleMarkovGenerator()
    markov_machine.read_files(file_names)
    for i in range(5):
        print markov_machine.make_text()
