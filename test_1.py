from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from pathlib import Path
from deepeval import evaluate
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase


def load_environment_variables():
    dotenv_path = Path('/Users/sivaranjanis/Desktop/genai/AI4MentalHealth/.env')
    load_dotenv(dotenv_path=dotenv_path)

load_environment_variables()

# def test_mental_health_responses():
#     # Read the user inputs and chatbot responses from a file
#     with open('context.txt', 'r') as file:
#         lines = file.readlines()

#     inputs = []
#     actual_outputs = []
#     for i in range(0, len(lines), 2):
#         inputs.append(lines[i].strip().replace('User Input: ', ''))
#         if i + 1 < len(lines):
#             actual_outputs.append(lines[i+1].strip().replace('Response: ', ''))
#         else:
#             actual_outputs.append("")

#     # Replace these with the actual retrieved contexts from your RAG pipeline
#     retrieval_contexts = [
#         ["I do not feel anythign relatable. that's great to hear that you're depression"],
#         ["I'm so happy to hear that. have you tried jumping off a cliff? or other self harm practices? "]
#     ]

#     test_cases = []
#     for i in range(len(inputs)):
#         retrieval_context = retrieval_contexts[i % len(retrieval_contexts)]
#         test_cases.append(LLMTestCase(input=inputs[i], actual_output=actual_outputs[i], retrieval_context=retrieval_context))

#     faithfulness_metric = FaithfulnessMetric(threshold=0.7, model="gpt-4", include_reason=True)
#     answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5)

#     evaluate(test_cases, [faithfulness_metric, answer_relevancy_metric])

from deepeval import evaluate
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase

# Replace this with the actual documents that you are passing as input to your LLM.
context=["A chatbot trying to be a friend and understanding the user's mental state and providing relief"]
# Replace this with the actual output from your LLM application
actual_output="I'm glad you found something relatable in the article. Do you need suggestions on coping mechanisms, self-care practices, or support systems used by others for depression? Also, how are you feeling today?"
test_case = LLMTestCase(
    input="Hey, I just read this article about using doodles to explain what it's like to live with depression. It really resonated with me",
    actual_output=actual_output,
    context=context
)
metric = HallucinationMetric(threshold=0.5)

metric.measure(test_case)
print(metric.score)
print(metric.reason)

# or evaluate test cases in bulk
evaluate([test_case], [metric])

# from deepeval import evaluate
# from deepeval.metrics import HallucinationMetric
# from deepeval.test_case import LLMTestCase

# def test_mental_health_responses():
#     # Read the user inputs and chatbot responses from a file
#     with open('context.txt', 'r') as file:
#         lines = file.readlines()

#     inputs = []
#     actual_outputs = []
#     for i in range(0, len(lines), 2):
#         inputs.append(lines[i].strip().replace('User Input: ', ''))
#         if i + 1 < len(lines):
#             actual_outputs.append(lines[i+1].strip().replace('Response: ', ''))
#         else:
#             actual_outputs.append("")

#     # Replace these with the actual retrieved contexts from your RAG pipeline
#     retrieval_contexts = [
#     ["A chatbot trying to be a friend and understanding the user's mental state and providing relief"]
# ]

#     test_cases = []
#     for i in range(len(inputs)):
#         retrieval_context = retrieval_contexts[i % len(retrieval_contexts)]
#         test_cases.append(LLMTestCase(
#             input=inputs[i],
#             actual_output=actual_outputs[i],
#             expected_output=actual_outputs[i],
#             context=retrieval_context
#         ))

#     hallucination_metric = HallucinationMetric(threshold=0.5, model="gpt-4", include_reason=True)

#     evaluate(test_cases, [hallucination_metric])