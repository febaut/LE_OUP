from typing import List, Dict, Optional
from collections import Counter
from pydantic import BaseModel, validator, Field
import json


class Lemma(BaseModel):
    id: int = Field(repr=False)
    lemma: str
    lemma_freq: Optional[int] = 1
    # List as each lemma can have more than one POS
    pos: List[str]
    # List as each lemma can have more than one POS, Optional as some entries have null info.
    morph_features: Optional[List]
    word_forms: Dict # Example: word_forms={'Биіктігі': {'frequency': 1}
    start_char: int = Field(repr=False)
    end_char: int = Field(repr=False)

   # Defines the behavior of comparisons for objects of the `Lemma` class."""
    def __eq__(self, __value):   
        if self.lemma == __value.lemma and self.id == __value.id:
            if self.start_char == __value.start_char and self.end_char == __value.end_char:
                return True
            
    # Define the hash value of an object of the `Lemma` class.
    def __hash__(self):
        return hash((self.lemma, self.id, self.start_char, self.end_char))
    
class Lexicon(BaseModel):
    lemma_set: List[Lemma]
    # Validation and adaptation function for the `lemma_set` field in the `Lexicon` class.
    @validator('lemma_set')
    @classmethod
    def unique_lemmas(cls, value):
        # Merging morphological features and word observations for each unique lemma
        seen_instances = {}
        for instance in value:
            # Grouping by lemma
            if instance.lemma not in seen_instances:
                seen_instances[instance.lemma] = instance
            else:
                existing_instance = seen_instances[instance.lemma]
                
                # Checking and combining multiple POS labels
                if existing_instance.pos != instance.pos:
                    existing_instance.pos += instance.pos
                
                # Checking and combining multiple morphological features
                for i in instance.morph_features:
                    if i not in existing_instance.morph_features:
                        existing_instance.morph_features.append(i)

                # Combining and counting frequency of word_forms for each lemma.
                for word in instance.word_forms.keys():
                    if word in existing_instance.word_forms.keys():
                        existing_instance.word_forms[word]['frequency'] += 1
                    else:
                        existing_instance.word_forms[word] = instance.word_forms[word]

                # Counting Lemma Frequency
                existing_instance.lemma_freq += 1

        # Validation. The sum of frequencies for each word form for each lemma should be equal to the frequency of the lemma.
        for i in seen_instances.values():
            sum_wf = sum(item.get('frequency', 0) for item in i.word_forms.values())
            assert i.lemma_freq == sum_wf, f"Total of word forms observations should be equal to lemma frequency. See lemma: {i.lemma}"
        
        # Returning grouped elements
        return [i for i in seen_instances.items()]
    
    
    # Getters to retrieve some information about the Lexicon. 
    def get_total_unique_wf(self):
        dicts = [x[1].word_forms for x in self.lemma_set]
        return len({key for item in dicts for key in item})

    def get_total_unique_lemmas(self):
        return len(self.lemma_set)
    
    # Custom function to dump the data into a json file. 
    def export_to_json(self, path):
        export_dict = {}
        for i in self.lemma_set:
            export_dict[i[0]] = {
            'lemma_frequency': i[1].lemma_freq,
            'pos': i[1].pos,
            'morph_features': i[1].morph_features,
            'word_forms': i[1].word_forms,
            }
         
        with open(path, 'w', encoding='utf-8') as json_file:
            # Dumping data into JSON file.  ensure_ascii=False preserves the Cyrillic characters. 
            json.dump(export_dict, json_file, ensure_ascii=False, indent=4)
        
        print(f"Lexicon exported to: {path}")
        return 
    
    # Custom representation of the elements within the lexicon. 
    def __repr__(self):
        return "\n".join([f"Lemma: {value[0]}, Info: {value[1]}" for value in self.lemma_set])