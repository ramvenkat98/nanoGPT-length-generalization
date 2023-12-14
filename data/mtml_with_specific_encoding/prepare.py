import sys
sys.path.append('/home/ramvenkat98/cs330_project_local/nanogpt/data/')
import counting.prepare as counting_prepare
import parity.prepare as parity_prepare
import mode.prepare as mode_prepare
import random

tasks = {
    1: counting_prepare,
    2: parity_prepare,
    3: mode_prepare,
}

meta_vocab_size = max(tasks[i].meta_vocab_size for i in range(1, 4)) + 3
print("Meta vocab size is", meta_vocab_size)

def generate_some(length, split, fixed_task_id = None, fixed_length = None):
    L = []
    for i in range(1, 4):
        task_id = random.randint(1, 3) if fixed_task_id is None else fixed_task_id
        task = tasks[task_id]
        L += [(task_id, x) for x in task.generate_some(length, split, fixed_length = fixed_length)]
    random.shuffle(L)
    return L[:length]

def encode(L):
    encoded = []
    for (task_id, x) in L:
        y = tasks[task_id].encode([x])
        if task_id == 1:
            encoded += [meta_vocab_size - 3]
        elif task_id == 2:
            encoded += [meta_vocab_size - 2]
        elif task_id == 3:
            encoded += [meta_vocab_size - 1]
        encoded += y
    return encoded

def decode(L):
    decoded = []
    i = 0
    while i < len(L):
        assert(L[i] >= meta_vocab_size - 3)
        assert(L[i] < meta_vocab_size)
        task_id = L[i] - (meta_vocab_size - 3) + 1
        j = i + 1
        while j < len(L):
            if L[j] >= meta_vocab_size - 3:
                break
            j += 1
        decoded += [(task_id, m) for m in tasks[task_id].decode(L[i + 1:j])]
        i = j
    return decoded

