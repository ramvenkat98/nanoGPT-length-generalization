import os
import pickle
import requests
import numpy as np
import random

ALPHABET_SIZE = 52
TRAIN_MAX_LENGTH = 50
VAL_MAX_LENGTH = 100

def generate_some(length, split, unique_tokens = 5, fixed_length = None):
    L = []
    max_len = TRAIN_MAX_LENGTH if split == 'train' else VAL_MAX_LENGTH
    all_tokens = [i for i in range(ALPHABET_SIZE)]
    for i in range(length):
        tokens = random.sample(all_tokens, k = unique_tokens)
        x = random.choices(tokens, k = random.randint(1, max_len) if fixed_length is None else fixed_length)
        counts = list(map(x.count, tokens))
        if counts.count(max(counts)) > 1:
            current_max_count = max(counts)
            first = counts.index(current_max_count)
            second = counts.index(current_max_count, first + 1)
            while True:
                pos = random.randint(0, len(x) - 1)
                if x[pos] == tokens[first]:
                    x[pos] = tokens[second]
                    break
        counts = list(map(x.count, tokens))
        assert(counts.count(max(counts)) == 1)
        mode = tokens[counts.index(max(counts))]
        num_str = ' '.join(map(str, x))
        L.append("Q: " + num_str + " A: " + str(mode))
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
