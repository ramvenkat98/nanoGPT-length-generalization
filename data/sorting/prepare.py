import os
import pickle
import requests
import numpy as np
import random
from itertools import chain

ALPHABET_SIZE = 100
ENCODED_ALPHABET_SIZE = 100
TRAIN_MAX_LENGTH = 50

def generate_some(n, split, fixed_length = None):
    L = []
    max_len = TRAIN_MAX_LENGTH if split == 'train' else ALPHABET_SIZE
    for i in range(n):
        seq = [i for i in range(ALPHABET_SIZE)]
        random.shuffle(seq)
        x = random.randint(1, max_len) if fixed_length is None else fixed_length
        L.append(['s'] + seq[:x] + ['m'] + sorted(seq[:x]) + ['e'])
    return L

def encode(L):
    encoded = []
    for x in L:
        if not (x[0] == 's' and x[-1] == 'e'):
            print(x)
            assert False
        y = []
        for i in range(len(x)):
            if x[i] == 's':
                y.append(ENCODED_ALPHABET_SIZE)
            elif x[i] == 'm':
                y.append(ENCODED_ALPHABET_SIZE + 1)
            elif x[i] == 'e':
                y.append(ENCODED_ALPHABET_SIZE + 2)
            else:
                y.append(x[i])
        encoded += y
    return encoded

def decode(L):
    decoded = []
    if L[0] != ENCODED_ALPHABET_SIZE:
        decoded.append([])
    for x in L:
        if x == ENCODED_ALPHABET_SIZE:
            decoded.append(['s',])
        elif x == ENCODED_ALPHABET_SIZE + 1:
            decoded[-1].append('m')
        elif x == ENCODED_ALPHABET_SIZE + 2:
            decoded[-1].append('e')
        else:
            decoded[-1].append(x)
    return decoded

meta_vocab_size = ENCODED_ALPHABET_SIZE + 3
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
    'vocab_size': meta_vocab_size,
}
with open(os.path.join(os.path.dirname(__file__), 'meta.pkl'), 'wb') as f:
    pickle.dump(meta, f)
'''
