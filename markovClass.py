import random as r

class MarkovChain:
    order = 2
    length = 16

    def __init__(self):
        self.memory = {}

    def learn(self, samples):
        self.gateways = [] # Possible beginnings

        # Loop through all samples and boil them down to lists
        for sample in [s.split(" ") for s in samples]:

            # Add beginning to possible gateways
            self.gateways.append(" ".join(sample[0:self.order]))

            # Get all n-grams and their possible continuations
            for i, item in enumerate(sample[:-self.order+1]):
                gram = " ".join(sample[i:i+self.order])
                try:
                    self.memory.setdefault(gram, []).append(sample[i+self.order])
                except IndexError:
                    pass

    def generate(self):

        curGram = r.choice(self.gateways)
        markovText = curGram
        for _ in range(self.length):
            if "(end)" in markovText:
                markovText = markovText[:-6]
                break

            nextGram = r.choice(self.memory[curGram])
            markovText += " " + nextGram
            curGram = " ".join(markovText.split(" ")[-self.order:])

        return markovText
