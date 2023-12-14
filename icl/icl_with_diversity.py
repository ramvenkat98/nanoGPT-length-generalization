import openai
import random
import tiktoken
from data.parity_with_tuples_and_indexing_with_consistent_starts_icl.prepare import generate_some

# openai.api_key = "..."
enc = tiktoken.get_encoding("cl100k_base")

CONTEXT_LENS = [10] # [5] # [5, 10, 20]
EVAL_LENS = [5] # [20] # [85]
MODELS = ["davinci"] # , "curie", "babbage"]

results = []

for model in MODELS:
    for context_len in CONTEXT_LENS:
        for eval_len in EVAL_LENS:
            correct = 0
            technically_correct = 0
            iters = 50
            for x in range(iters):
                print(f"Iter {x}")
                context = []
                for i in range(1, 4):
                    dedupped = list(set(generate_some(100, 'train', fixed_length = i)))
                    random.shuffle(dedupped)
                    print(dedupped)
                    print(i, len(dedupped))
                    context += dedupped
                print(len(context))
                context += generate_some(context_len // 2, 'train', fixed_length = 4)
                dedupped = list(set(generate_some(100, 'train', fixed_length = 5)))
                random.shuffle(dedupped)
                context += dedupped[:context_len // 2]
                print(len(context))
                question_and_answer = dedupped[context_len // 2] # generate_some(1, 'val', fixed_length = eval_len)[0]
                sep_token = ' A:'
                separator = question_and_answer.find(sep_token)
                question, answer = question_and_answer[:separator + len(sep_token)], question_and_answer[separator + len(sep_token):]
                initial_spiel = "We will compute the parity of a sequence of bits (0 or 1) in the following examples.\n"
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
                if (expected_answer[-1] == response[:len(expected_answer)][-1]):
                    print("Technically Correct")
                    technically_correct += 1
                else:
                    print("Technically Wrong")
            results.append((model, context_len, eval_len, correct / iters, technically_correct / iters))
            print(results[-1])

print(results)
