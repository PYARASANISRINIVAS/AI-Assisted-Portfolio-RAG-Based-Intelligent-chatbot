# eval_retriever.py
from dotenv import load_dotenv

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import ContextualRecallMetric, ContextualPrecisionMetric
from deepeval.evaluate import CacheConfig
import json 
# from src.reranker import RerankingRetriever
# from evals.harness import load_goldens, summarize_by_metric, print_summary
from  app.rag_chatbot import retriver
from deepeval.models import LiteLLMModel
from deepeval.evaluate import AsyncConfig

load_dotenv()

GOLDEN_PATH = "D:/Portfolio/backend/knowledge_base/golden_dataset.json"

THRESHOLD = 0.7

JUDGE_MODEL = LiteLLMModel(
    model="groq/openai/gpt-oss-20b",
    temperature=0
)


def load_goldens(path):
    print("loading the data ")
    with open(path) as f:
        return json.load(f)



def run(retriever):
    # 1. LOAD the golden set --- the fixed, human-authored truth
    goldens = load_goldens(GOLDEN_PATH)

    # 2. RUN THE INJECTED RETRIEVER on each question to fill retrieval_context,
    #    then build one test case per golden.
    test_cases = []
    for g in goldens:
        retrieved = retriever.invoke(g["question"])
        retrieval_context = [doc.page_content for doc in retrieved]
        print("Creating the TestCase")

        test_cases.append(
            LLMTestCase(
                input=g["question"],
                expected_output=g["expected_answer"],
                retrieval_context=retrieval_context,
                actual_output="(generator not evaluated in this run)",
            )
        )

    # 3. THE METRICS --- recall (did we miss?) and precision (ranked well?)
    metrics = [
        ContextualRecallMetric(threshold=THRESHOLD, model=JUDGE_MODEL, include_reason=True),
        ContextualPrecisionMetric(threshold=THRESHOLD, model=JUDGE_MODEL, include_reason=True),
    ]
    print("Metrics created ! ")

    # 4. EVALUATE --- every metric on every case, batched + parallel, printed report.
    #    hyperparameters travel with the run so the report is tagged with the config.
    # result = evaluate(
    #     test_cases=test_cases,
    #     metrics=metrics,
    #     async_config=AsyncConfig(
    #     run_async=False
    #         ),
    #             cache_config=CacheConfig(
    #     use_cache=False,
    #     write_cache=False
    # ),
    #     hyperparameters={
    #         # "retriever": "reranker",          # vs "reranked" when you swap it in
    #         "embedding_model": "text-embedding-3-large",
    #         "chunk_size": 1000,
    #         "chunk_overlap": 150,
    #         "top_k": 3,
    #         "judge_model": JUDGE_MODEL,
    #         "golden_set": GOLDEN_PATH,
    #     },
    # )
    # print("evaluated ! ")
    # return result

    test_cases = test_cases[:10]

    import time

    all_results = []

    for i, test_case in enumerate(test_cases):

        print(f"\nEvaluating test case {i + 1}/{len(test_cases)}")

        for metric in metrics:

            result = evaluate(
                test_cases=[test_case],
                metrics=[metric],
                async_config=AsyncConfig(run_async=False)
                # cache_config=CacheConfig(
                #     use_cache=False,
                #     write_cache=False
                # )
            )

            all_results.append(result)

            time.sleep(15)

        print(f"Test case {i + 1} completed!")

    print("\nEvaluation completed!")

    all_scores = {}

    for result in all_results:
        for test_result in result.test_results:
            for metric in test_result.metrics_data:

                name = metric.name

                if name not in all_scores:
                    all_scores[name] = []

                all_scores[name].append(metric.score)


    print("\n========== OVERALL EVALUATION ==========")

    for name, scores in all_scores.items():

        average = sum(scores) / len(scores)

        passed = sum(score >= THRESHOLD for score in scores)
        total = len(scores)

        print(f"\n{name}")
        print(f"Average Score : {average:.2f}")
        print(f"Pass Rate     : {(passed / total) * 100:.2f}%")
        print(f"Passed        : {passed}/{total}")

print(run(retriver))

