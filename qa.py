import csv
import json
import os
import pdb

import nltk
from pattern import en
import spacy


mnli_dir = os.path.expanduser('~/JHU/Research/Augmentation/')
mnli_train = os.path.join(mnli_dir, 'multinli_1.0_train.jsonl')
mnli_headers = ['index', 'promptID', 'pairID', 'genre', 'sentence1_binary_parse', 'sentence2_binary_parse', 'sentence1_parse', 'sentence2_parse', 'sentence1', 'sentence2', 'label1', 'gold_label']

nlp = spacy.load('en_core_web_sm')
ner = nlp.create_pipe('ner')
parser = nlp.create_pipe('parser')
lemmatizer = nltk.stem.WordNetLemmatizer()

def load_boolq_train():
    return [json.loads(x) for x in open('boolq/train.jsonl').readlines()]

def lower_first(s):
    return s[0].lower() + s[1:]        

def upper_first(s):
    return s[0].upper() + s[1:]        

def find_two_entities():
    for ex in train[:100]:
        doc = nlp(ex['passage'])
        if len([e for e in doc.ents if e.label_ == 'PERSON']) > 0:
            print(doc, [(e.text, e.label_) for e in doc.ents])

def visualize():
    for i in train:
        print(i['question'])
        print(i['answer'])
        print(i['passage'])
        print()
        
def load_fiction():
    fname = os.path.expanduser('~/JHU/Research/Augmentation/train.tsv')
    reader = csv.DictReader(open(fname), delimiter='\t')
    l = []
    while True:
        try:
            row = next(reader)
            if row['genre'] == 'travel':
                l.append(row)
        except StopIteration:
            break
        except Exception as e:
            print(e)
    return l


class MNLISyntacticRegularizer(object):

    # Potential refinements:
    # Fix agreement features on verb if relevant:
    # Everyone likes the benefits -> the benefits like everyone

    def __init__(self):
        self.present_to_past = {}
        self.present_to_vb = {}
        self.present_to_vbz = {}

    def tsv(self, filename):
        return csv.writer(open(filename, 'w'), delimiter='\t')

    def loop(self, debug=False):
        w_subjobj_orig = self.tsv('subj_obj_orig_premise.tsv')
        w_subjobj_hap = self.tsv('subj_obj_hyp_as_premise.tsv')
        w_passive_orig = self.tsv('passive_orig_premise.tsv')
        w_passive_hap = self.tsv('passive_hyp_as_premise.tsv')

        self.lines = open(mnli_train).readlines()
        already_seen = set()
        self.dicts = []
        n = 0
        for i, line in enumerate(self.lines):
            j = json.loads(line)
            self.dicts.append(j)
            if i % 10000 == 0:
                print('%d out of %d' % (i, len(self.lines)))
            if debug and i == 10000:
                break
            if j['genre'] == 'telephone':
                continue

            tree = j['hyptree'] = nltk.tree.Tree.fromstring(j['sentence2_parse'])

            ss = [x for x in tree.subtrees() if x.label() == 'S']

            for s in ss[:1]:
                if len(s) < 2:  # Not a full NP + VP sentence
                    continue

                subj_head = self.get_np_head(s[0])
                if subj_head is None:
                    continue
                subject_number = self.get_np_number(s[0])

                vp_head = self.get_vp_head(s[1])
                if vp_head is None:
                    continue

                subj = ' '.join(s[0].flatten())
                arguments = tuple(x.label() for x in s[1][1:])

                #print(vp_head)
                #print(type(vp_head))
                #print(en.lemma(vp_head))

                if (arguments != ('NP',) or en.lemma(vp_head) in ['be', 'have']):
                    continue
		

                direct_object = ' '.join(s[1][1].flatten())

                #print('\n')
                #print(s[1][1])
                object_number = self.get_np_number(s[1][1])

                if object_number is None:
                    # Personal pronoun, very complex NP, or parse error
                    continue

                subjobj_rev_hyp = ' '.join([
                    upper_first(direct_object),
                    # FIXME: keep tense
                    en.conjugate(vp_head, number=object_number),
                    lower_first(subj)]) + '.'

                passive_hyp_same_meaning = ' '.join([
                    upper_first(direct_object),
                    self.passivize_vp(s[1], object_number),
                    lower_first(subj)]) + '.'

                passive_hyp_inverted = ' '.join([
                    subj,
                    self.passivize_vp(s[1], subject_number),
                    direct_object])

                #print(subjobj_rev_hyp)
                if j['gold_label'] == 'entailment':
                    self.mnli_row(w_subjobj_orig, 1000000 + n,
                            j['sentence1'], subjobj_rev_hyp, 'neutral')

                self.mnli_row(w_subjobj_hap, 1000000 + n,
                        j['sentence2'], subjobj_rev_hyp, 'neutral')

                self.mnli_row(w_passive_orig, 1000000 + n,
                        j['sentence1'], passive_hyp_same_meaning, 
                        j['gold_label'])

                self.mnli_row(w_passive_hap, 1000000 + n,
                        j['sentence2'], passive_hyp_inverted, 'neutral')
                self.mnli_row(w_passive_hap, 2000000 + n,
                        j['sentence2'], passive_hyp_same_meaning, 'entailed')

                n += 1


    def mnli_row(self, writer, i, premise, hypothesis, label):
        row = [str(i)] + ['ba'] * 7 + [premise, hypothesis, 'ba', label]
        writer.writerow(row)

    def get_vp_head(self, vp):
        head = None
        if vp.label() == 'VP':
            while True:
                nested_vps = [x for x in vp[1:] if x.label() == 'VP']
                if len(nested_vps) == 0:
                    break
                vp = nested_vps[0]
            if vp[0].label().startswith('VB'):
                head = vp[0][0].lower()
        return (head, vp[0].label())

    def passivize_vp(self, vp, subj_num=en.SINGULAR):
        head = None
        flat = vp.flatten()
        if vp.label() == 'VP':
            nesters = []
            while True:
                nesters.append(vp[0][0])
                nested_vps = [x for x in vp[1:] if x.label() == 'VP']
                if len(nested_vps) == 0:
                    break
                vp = nested_vps[0]
            label = vp[0].label()
            if label.startswith('VB'):
                head = vp[0][0].lower()
                if len(nesters) > 1:
                    passivizer = 'be'
                elif label in ['VBP', 'VB', 'VBZ']: 
                    # 'VB' here (not nested) is a POS tag error
                    passivizer = 'are' if subj_num == en.PLURAL else 'is'
                elif label == 'VBD' or label == 'VBN':
                    # 'VBN' here (not nested) is a POS tag error
                    passivizer = 'were' if subj_num == en.PLURAL else 'was'
                    # Alternatively, figure out the number of the subject
                    # to decide whether it's was or were
                vbn = en.conjugate(head, 'ppart')
                #print(vp.flatten())
                #print( #pdb.set_trace()
        return '%s %s by' % (passivizer, vbn)

    def get_np_head(self, np):
        head = None
        if (np.label() == 'NP' and np[0].label() == 'DT'):
            head_candidates = [x for x in np[1:] if
                    x.label().startswith('NN')]
            if len(head_candidates) == 1:
                # > 1: Complex noun phrases unlikely to be useful
                # 0: Pronominal subjects like "many"
                head = lemmatizer.lemmatize(head_candidates[0][0])
        return head 

    def get_np_number(self, np):
        number = None
        if np[0].label() == 'NP':
            np = np[0]
        head_candidates = [x for x in np if x.label().startswith('NN')]
        if len(head_candidates) == 1:
            label = head_candidates[0].label()
            number = en.PLURAL if label == 'NNS' else en.SINGULAR
        elif len(head_candidates) > 1:
            number = en.PLURAL
        return number 

test = MNLISyntacticRegularizer()
test.loop()
