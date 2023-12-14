import openai
import random
import tiktoken
# from data.parity_with_tuples_and_indexing_with_consistent_starts_icl.prepare import generate_some
# from data.map_unique.prepare import generate_some
# from data.copy_unique.prepare import generate_some
# from data.map_unique.prepare_lookup_per_question import generate_some
from data.copy_with_lots_of_repeats.prepare_scratchpad import generate_some

# openai.api_key = ... "<YOUR_API_KEY>"
enc = tiktoken.get_encoding("cl100k_base")

CONTEXT_LENS = [20] # [5] # [5, 10, 20]
EVAL_LENS = [30] # [13, 26] # [26] # [20] # [85]
MODELS = ["davinci"] # , "curie", "babbage"]

results = []

for model in MODELS:
    for context_len in CONTEXT_LENS:
        for eval_len in EVAL_LENS:
            correct = 0
            iters = 5
            for x in range(iters):
                print(f"Iter {x}")
                context = generate_some(context_len, 'train')
                question_and_answer = generate_some(1, 'val', fixed_length = eval_len)[0]
                sep_token = ' A:'
                separator = question_and_answer.find(sep_token)
                question, answer = question_and_answer[:separator + len(sep_token)], question_and_answer[separator + len(sep_token):]
                initial_spiel = "" # "We will compute the parity of a sequence of bits (0 or 1) in the following examples.\n"
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
