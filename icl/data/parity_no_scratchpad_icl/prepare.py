import os
import pickle
import requests
import numpy as np
import random
import string

TRAIN_MAX_LENGTH = 20
VAL_MAX_LENGTH = 40
random.seed(3)
ALPHABET_SIZE = 42
alphabet = [str(i) for i in range(ALPHABET_SIZE)]

def generate_some(length, split, fixed_length = None):
    L = []
    max_len = TRAIN_MAX_LENGTH if split == 'train' else VAL_MAX_LENGTH
    for i in range(length):
        l = random.randint(1, max_len) if fixed_length is None else fixed_length
        x = random.choices([0, 1], k = l)
        index_hint_start = random.randint(2, 41)
        current = []
        result = alphabet[0]
        index_hint = index_hint_start
        for i in range(len(x)):
            current.append(alphabet[x[i]])
            if x[i] == 1:
                result = alphabet[0] if result == alphabet[1] else alphabet[1]
        L.append("Q: " + ' '.join(current) + " A: " + ' '.join(result))
    return L

'''
def generate_some(length, split, fixed_length = None):
    L = []
    max_len = TRAIN_MAX_LENGTH if split == 'train' else ALPHABET_SIZE
    for i in range(length):
        random.shuffle(L_sub)
        L_sub = [alphabet[j] for j in L_sub]
        l = random.randint(1, max_len) if fixed_length is None else fixed_length
        values = random.choices([alphabet[0], alphabet[1]], k = l)
        num_str = ' '.join(values)
        ans_str = [alphabet[0]]

        L.append("Q: " + num_str + " A: " + num_str)
    return L
'''

def generate_all(length):
    L = []
    for i in range(ALPHABET_SIZE - length + 1):
        L.append(['s', i, i + length - 1, 'm'] + [j for j in range(i, i + length)] + ['e'])
    return L
d = {}
for length in range(1, ALPHABET_SIZE + 1):
    d[length] = generate_all(length)

def encode(L):
    encoded = []
    for x in L:
        if not (x[0] == 's' and x[-1] == 'e'):
            print(x)
            assert False
        y = x.copy()
        for i in range(len(y)):
            if y[i] == 's':
                y[i] = ALPHABET_SIZE
            elif y[i] == 'm':
                y[i] = ALPHABET_SIZE + 1
            elif y[i] == 'e':
                y[i] = ALPHABET_SIZE + 2
        encoded += y
    return encoded

def decode(L):
    decoded = []
    if L[0] != ALPHABET_SIZE:
        decoded.append([])
    for x in L:
        if x == ALPHABET_SIZE:
            decoded.append(['s',])
        elif x == ALPHABET_SIZE + 1:
            decoded[-1].append('m')
        elif x == ALPHABET_SIZE + 2:
            decoded[-1].append('e')
        else:
            decoded[-1].append(x)
    return decoded

# TODO: Instead of commenting it out, properly use if name == __main__ ...
train_data = []
# eventual implementation
for length in range(1, TRAIN_MAX_LENGTH + 1):
    train_data += d[length]
val_data = []
for x in d.values():
    val_data += x

meta_vocab_size = ALPHABET_SIZE + 3
'''
# encode both to integers
train_ids = encode(train_data)
val_ids = encode(val_data)
assert(decode(train_ids) == train_data)
assert(decode(val_ids) == val_data)
print(f"train has {len(train_ids):,} tokens")
print(f"val has {len(val_ids):,} tokens")

# export to bin files
train_ids = np.array(train_ids, dtype=np.uint16)
val_ids = np.array(val_ids, dtype=np.uint16)
train_ids.tofile(os.path.join(os.path.dirname(__file__), 'train.bin'))
val_ids.tofile(os.path.join(os.path.dirname(__file__), 'val.bin'))

# save the meta information as well, to help us encode/decode later
meta = {
    'vocab_size': ALPHABET_SIZE + 3,
}
with open(os.path.join(os.path.dirname(__file__), 'meta.pkl'), 'wb') as f:
    pickle.dump(meta, f)
'''
