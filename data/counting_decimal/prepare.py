import os
import pickle
import requests
import numpy as np
import random
from itertools import chain

ALPHABET_SIZE = 155
ENCODED_ALPHABET_SIZE = 10
TRAIN_MAX_LENGTH = 50

def generate_all(length):
    L = []
    for i in range(ALPHABET_SIZE - length + 1):
        start_number = [int(c) for c in str(i)]
        end_number = [int(c) for c in str(i + length - 1)]
        numbers = [[int(c) for c in str(j)] for j in range(i, i + length)]
        L.append(['s'] + start_number + ['p'] + end_number + ['m'] + list(chain.from_iterable(numbers)) + ['e'])
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
        y = []
        for i in range(len(x)):
            if x[i] == 's':
                y.append(ENCODED_ALPHABET_SIZE)
            elif x[i] == 'm':
                y.append(ENCODED_ALPHABET_SIZE + 1)
            elif x[i] == 'e':
                y.append(ENCODED_ALPHABET_SIZE + 2)
            elif x[i] == 'p':
                y.append(ENCODED_ALPHABET_SIZE + 3)
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
        elif x == ENCODED_ALPHABET_SIZE + 3:
            decoded[-1].append('p')
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

meta_vocab_size = ENCODED_ALPHABET_SIZE + 4
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
