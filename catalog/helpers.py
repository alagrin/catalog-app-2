import random

def gen_random_string(valid, length):
        random_string = ''.join(valid) # join together members of tuple which is iterable
        return ''.join(random.choice(random_string) for x in range(length)) # returns a random string w/ length chars