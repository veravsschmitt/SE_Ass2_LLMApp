import json
from openai import OpenAI
import re
from openAI_interface import LLM_Interact

llm = LLM_Interact()

def run_test(test):
    
    pdf_path = f"eval_study_notes/{test['study_notes']}"
    llm.set_study_notes(pdf_path)
    
    answer_check = llm.check_answer(
        question=test["question"],
        answer=test["input"]
    )

    pattern = test["expected_pattern"]
    passed = re.search(pattern, answer_check, re.IGNORECASE) is not None

    return passed, answer_check


def main():
    
    with open("test.json", "r", encoding="utf-8") as f:
        tests = json.load(f)

    passed_count = 0

    for test in tests:
        print(f"==== Test '{test['name']}' ================================================================= \n")
        passed, answer = run_test(test)
        print(f"Test '{test['name']}': {'PASSED' if passed else 'FAILED'} \n\n")
        if not passed:
            print(f"Expected pattern: {test['expected_pattern']}")
            print(f"Model answer: {answer}\n")
        if passed:
            passed_count += 1

    print("\n=================================")
    print(f"Pass rate: {passed_count}/{len(tests)} "
          f"({(passed_count / len(tests)) * 100:.1f}%)")
    print("=================================\n")

if __name__ == "__main__":
    main()
