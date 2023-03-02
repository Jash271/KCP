'''
suggestions
we cant rely just on the JD. Need more data to do matching (maybe create a dataset and store data corresponding to every position (generic for every company))
the above thing will improve similarity score and also help in giving suggestions, like we can suggest keywords from our dataset.


Resume generator 
Parallel computaion dekhle (do paraphrasing on gpu than cpu's)  Ray, Hugg Do Face ||ism

'''


import os.path
import pickle
import warnings

from parrot import Parrot

warnings.filterwarnings("ignore")


def paraphrase_sentence(phrase, parrot) -> str:
    temp = ""
    paraphrases = parrot.augment(
        input_phrase=phrase, max_return_phrases=4, do_diverse=False)
    if paraphrases:
        for paraphrase in paraphrases:
            temp += str(paraphrase[0])
            temp += '\n'
    return temp


def paraphrase_fn(p_text) -> str:

    if not os.path.isfile('test.pickle'):
        parrot = Parrot()
        with open("test.pickle", "wb") as outfile:
            pickle.dump(parrot, outfile)

    with open("test.pickle", "rb") as infile:
        parrot = pickle.load(infile)

    phrases = p_text.split('.')
    ans = ''
    for phrase in phrases:
        temp = paraphrase_sentence(phrase=phrase, parrot=parrot)

        if temp == "":
            temp = phrase
        ans += temp
        ans += '\n\n'
    return ans


if __name__ == '__main__':
    paraphrase_fn()
    # main()
    # fn2()
