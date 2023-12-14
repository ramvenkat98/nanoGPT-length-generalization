import openai
import random
import tiktoken
# from data.parity_with_tuples_and_indexing_with_consistent_starts_icl.prepare import generate_some
# from data.map_unique.prepare import generate_some
# from data.copy_unique.prepare import generate_some
from data.map_unique.prepare_lookup import generate_some

# openai.api_key = "..."
enc = tiktoken.get_encoding("cl100k_base")

CONTEXT_LENS = [30] # [5] # [5, 10, 20]
EVAL_LENS = [13, 26] # [26] # [20] # [85]
MODELS = ["davinci"] # , "curie", "babbage"]

results = []

for model in MODELS:
    for context_len in CONTEXT_LENS:
        for eval_len in EVAL_LENS:
            correct = 0
            iters = 5
            for x in range(iters):
                print(f"Iter {x}")
                context, lookup = generate_some(context_len, 'train')
                question_and_answer, lookup_2 = generate_some(1, 'val', fixed_length = eval_len)
                question_and_answer = question_and_answer[0]
                assert(lookup == lookup_2)
                sep_token = ' A:'
                separator = question_and_answer.find(sep_token)
                question, answer = question_and_answer[:separator + len(sep_token)], question_and_answer[separator + len(sep_token):]
                initial_spiel = lookup # "We will compute the parity of a sequence of bits (0 or 1) in the following examples.\n"
                prompt = initial_spiel + '\n'.join(context) + '\n' + question
                print(prompt)
                print("Expected response:")
                print(answer.strip())
                response = openai.Completion.create(
                  engine=model,
                  prompt=prompt,
                  max_tokens=300
                )
                expected_answer = answer.strip()
                response = response.choices[0].text.strip()
                print("Actual response:")
                print(response[:len(expected_answer)])
                if (expected_answer == response[:len(expected_answer)]):
                    print("Correct")
                    correct += 1
                else:
                    print("Wrong")
            results.append((model, context_len, eval_len, correct / iters))
            print(results[-1])

print(results)
