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
        shift = 0
        if task_id >= 2:
            shift += tasks[1].meta_vocab_size
        if task_id >= 3:
            shift += tasks[2].meta_vocab_size
        y_shifted = [i + shift for i in y]
        encoded += y_shifted
    return encoded
    pass

def decode(L):
    decoded = []
    i = 0
    while i < len(L):
        if L[i] < tasks[1].meta_vocab_size:
            lower_bound, upper_bound = 0, tasks[1].meta_vocab_size
            task_id = 1
        elif L[i] < tasks[1].meta_vocab_size + tasks[2].meta_vocab_size:
            lower_bound, upper_bound = tasks[1].meta_vocab_size, tasks[1].meta_vocab_size + tasks[2].meta_vocab_size
            task_id = 2
        else:
            lower_bound, upper_bound = (
                tasks[1].meta_vocab_size + tasks[2].meta_vocab_size,
                tasks[1].meta_vocab_size + tasks[2].meta_vocab_size + tasks[3].meta_vocab_size
            )
            task_id = 3
        j = i
        while j < len(L):
            if not ((lower_bound <= L[j]) and (L[j] < upper_bound)):
                break
            j += 1
        decoded += [(task_id, m) for m in tasks[task_id].decode([x - lower_bound for x in L[i:j]])]
        i = j
    return decoded

meta_vocab_size = sum(tasks[i].meta_vocab_size for i in range(1, 4))
print("Meta vocab size is", meta_vocab_size)
