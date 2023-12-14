import os
import pickle
import requests
import numpy as np
import random

ALPHABET_SIZE = 100 + 2 + 2
VAL_MAX_LENGTH = 100
TRAIN_MAX_LENGTH = 50

def generate_some(length, split, fixed_length = None):
    L = []
    max_len = TRAIN_MAX_LENGTH if split == 'train' else VAL_MAX_LENGTH
    for i in range(length):
        l = random.randint(1, max_len) if fixed_length is None else fixed_length
        x = random.choices([0, 1], k = l)
        index_hint_start = random.randint(2, 101)
        current = ['s']
        result = ['m', '+']
        index_hint = index_hint_start
        for i in range(len(x)):
            index_hint += 1
            if index_hint >= 102:
                index_hint -= 100
            current.append(index_hint)
            current.append(x[i])
            if x[i] == 1:
                result.append(index_hint)
                result.append('-' if result[-2] == '+' else '+')
        L.append(current + result + ['e'])
    return L

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
            elif y[i] == '+':
                y[i] = ALPHABET_SIZE - 2
            elif y[i] == '-':
                y[i] = ALPHABET_SIZE - 1
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
        elif x == ALPHABET_SIZE - 2:
            decoded[-1].append('+')
        elif x == ALPHABET_SIZE - 1:
            decoded[-1].append('-')
        else:
            decoded[-1].append(x)
    return decoded

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
