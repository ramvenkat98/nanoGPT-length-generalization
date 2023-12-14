import openai
import random
import tiktoken
from data.parity_no_scratchpad_icl.prepare import generate_some

# openai.api_key = "..."
enc = tiktoken.get_encoding("cl100k_base")

CONTEXT_LENS = [20] # [5, 10, 20]
EVAL_LENS = [20] # [85]
MODELS = ["davinci"] # , "curie", "babbage"]

results = []

for model in MODELS:
    for context_len in CONTEXT_LENS:
        for eval_len in EVAL_LENS:
            correct = 0
            iters = 10 # 20
            for x in range(iters):
                print(f"Iter {x}")
                context = generate_some(context_len, 'train')
                question_and_answer = generate_some(1, 'val', fixed_length = eval_len)[0]
                sep_token = ' A:'
                separator = question_and_answer.find(sep_token)
                question, answer = question_and_answer[:separator + len(sep_token)], question_and_answer[separator + len(sep_token):]
                prompt = '\n'.join(context) + '\n' + question
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
