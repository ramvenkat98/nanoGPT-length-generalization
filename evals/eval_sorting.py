"""
Sample from a trained model
"""
import os
import pickle
from contextlib import nullcontext
import torch
import tiktoken
from model import GPTConfig, GPT

# -----------------------------------------------------------------------------
init_from = 'resume' # either 'resume' (from an out_dir) or a gpt2 variant (e.g. 'gpt2-xl')
out_dir = 'out-sorting' # ignored if init_from is not 'resume'
start = "\n" # or "<|endoftext|>" or etc. Can also specify a file, use as: "FILE:prompt.txt"
num_samples = 1 # number of samples to draw
max_new_tokens = 500 # number of tokens generated in each sample
temperature = 0.8 # 1.0 = no change, < 1.0 = less random, > 1.0 = more random, in predictions
top_k = 1 # 200 # retain only the top_k most likely tokens, clamp others to have 0 probability
seed = 1337
device = 'cuda' # examples: 'cpu', 'cuda', 'cuda:0', 'cuda:1', etc.
dtype = 'bfloat16' if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else 'float16' # 'float32' or 'bfloat16' or 'float16'
compile = False # use PyTorch 2.0 to compile the model to be faster
exec(open('configurator.py').read()) # overrides from command line or config file
# -----------------------------------------------------------------------------

torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.backends.cuda.matmul.allow_tf32 = True # allow tf32 on matmul
torch.backends.cudnn.allow_tf32 = True # allow tf32 on cudnn
device_type = 'cuda' if 'cuda' in device else 'cpu' # for later use in torch.autocast
ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=ptdtype)

# model
if init_from == 'resume':
    # init from a model saved in a specific directory
    ckpt_path = os.path.join(out_dir, 'ckpt.pt')
    checkpoint = torch.load(ckpt_path, map_location=device)
    gptconf = GPTConfig(**checkpoint['model_args'])
    model = GPT(gptconf)
    state_dict = checkpoint['model']
    unwanted_prefix = '_orig_mod.'
    for k,v in list(state_dict.items()):
        if k.startswith(unwanted_prefix):
            state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)
    model.load_state_dict(state_dict)
elif init_from.startswith('gpt2'):
    # init from a given GPT-2 model
    model = GPT.from_pretrained(init_from, dict(dropout=0.0))

model.eval()
model.to(device)
if compile:
    model = torch.compile(model) # requires PyTorch 2.0 (optional)

from data.sorting.prepare import encode, decode, generate_some
results = {}
with torch.no_grad():
    with ctx:
        for length in range(1, 51, 1):
            expected = []
            samples = generate_some(100, 'val', fixed_length = length)
            print("A few samples are ", samples[:10])
            y = [encode([x]) for x in samples]
            x = [y_[:y_.index(101) + 1] for y_ in y]
            print(x[:10])
            for k in range(num_samples):
                correct = 0
                x_lens = {}
                y_lens = {}
                for j in range(len(x)):
                    if len(x[j]) not in x_lens:
                        x_lens[len(x[j])] = [x[j]]
                        y_lens[len(x[j])] = [y[j]]
                    else:
                        x_lens[len(x[j])].append(x[j])
                        y_lens[len(x[j])].append(y[j])
                assert(len(x_lens) == 1)
                assert(len(y_lens) == 1)
                for j in x_lens:
                    x_current = x_lens[j]
                    y_current = y_lens[j]
                    p = torch.tensor(x_current, dtype=torch.long, device=device)
                    print(p.shape)
                    output = model.generate(p, max_new_tokens, temperature = temperature, top_k = top_k)
                    for i in range(len(output)):
                        if output[i][:len(y_current[i])].tolist() == y_current[i]:
                            correct += 1
                    print(f"Sub-length {j}, {len(output)} many samples; correct so far: {correct}")
            results[length] = correct / len(y)
            print(f"At length {length}, accuracy is {results[length]}")
print(results)
