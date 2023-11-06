from Lexicon import Lemma, Lexicon
import json
import itertools

# To be modified depending on input source and output purpose
input_json = './Data/sample_parsed_sentences.json'
output_json = './Data/sample_lexicon.json'

"""
Within the corpus, several duplicate tokens are found, as if each sentence had been processed twice. 
If these elements were kept the frequency counts would be distorted, so in my solution, 
I took the option of removing duplicated items for each sentence. 

As an example, the following token '2019' appears twice while in its sentece it appears only once. 

"sentence_text": "2019 жылы 27 желтоқсанда Президент \"Қазақстан Республикасының кейбір заңнамалық актілеріне қылмыстық, 
қылмыстық іс жүргізу заңнамасын жетілдіру және жеке адамның құқықтарын қорғауды күшейту 
мәселелері бойынша өзгерістер мен толықтырулар енгізу туралы\" Заңға қол қойды."

   {
          "id": "1",
          "text": "2019",
          "lemma": "2019",
          "pos": "NUM",
          "pos_finegrained": "num",
          "feats": "NumType=Ord",
          "start_char": "0",
          "end_char": "4"
        },
"""

# This function takes a each token in the json file as input and reformats it into a dictionary to create instances of the class Lemma.
# Some fields like id, start_char and end_char are taken to filter duplicated tokens per sentence. 
def preprocess_sentences(sentence):
    lemma_instances = []
    for token in sentence:
        lemma_entry = {'id': int(token['id']),
                'lemma': token['lemma'],
                'pos': [token['pos']],
                'morph_features': [token['feats']],
                # Takes the word and initializes the frequency counter with 1. 
                'word_forms': {token['text']: {'frequency':1}},
                "start_char": int(token['start_char']),
                "end_char": int(token['end_char'])}
        
        lemma_instances.append(Lemma(**lemma_entry))
    
    return list(set(lemma_instances))

# Creating an instance of the class `Lexicon` and initializing it with a set of `Lemma` objects. 
# The `Lemma` objects are created by iterating over the tokens in the JSON input file reformatting them into a dictionary using the `preprocess_sentences` function. 
# The resulting list of `Lemma` objects is then added to the `lemma_set` parameter of the `Lexicon` constructor.

lexicon = Lexicon(lemma_set=list(itertools.chain.from_iterable([preprocess_sentences(sentence['tokens']) for sentence in json.load(open(input_json, encoding='utf-8'))['sentences']])))

### Optional testing ###
def test_consistency():
    # Creating two lists to evaluate that the solution is working as expected 
    # `total_lemmas` and `total_word_forms`
    total_lemmas = [token['lemma'] for sentence in json.load(open(input_json, encoding='utf-8'))['sentences'] for token in sentence['tokens']]
    total_word_forms = [token['text'] for sentence in json.load(open(input_json, encoding='utf-8'))['sentences'] for token in sentence['tokens']]

    print(f"""
    Input file:
    Total lemmas: {len(total_lemmas)}
    Total unique lemmas: {len(set(total_lemmas))}
    Total word forms: {len(total_word_forms)}
    Total unique word forms: {len(set(total_word_forms))}
    """)

    # Checking if the total of unique lemmas in the `lexicon` is equal to the length of the set of unique lemmas in the input JSON file.
    assert lexicon.get_total_unique_lemmas() == len(set(total_lemmas))
    assert lexicon.get_total_unique_wf() == len(set(total_word_forms))

# comment/uncomment to avoid/excecute the previous test function prior to export.
# test_consistency()

# Calling the class method to export the lexicon  to a JSON file. 
lexicon.export_to_json(output_json)