from app.graph.state import GraphState
from app.schemas.answer import GradeAnswer
from app.llms.openai import grader_llm
answer_grader_structured_llm = grader_llm.with_structured_output(
    GradeAnswer
)


def answer_validation_node(state: GraphState):

    # question = state["rewritten_question"]

    answer = state["answer"]
    

    print("\n===== ANSWER VALIDATION =====")
    print(answer)
    if "INSUFFICIENT_INFORMATION" in answer:
        print("ROUTE -> FALLBACK")
        print("answer_found = no")
        return {
            "answer_found": "no"
        }
    print("ROUTE -> END")
    print("answer_found = yes")
    return {
        "answer_found": "yes"
    }
#     context = "\n\n".join(
#     [doc.page_content for doc in state["documents"][:5]]
# )

#     prompt = f"""
# You are an answer grader.

# Determine whether the answer sufficiently answers
# the user's question and is supported by the retrieved context.

# The answer does NOT need to be perfect.

# The answer does NOT need to be extremely detailed.

# Return "yes" if the answer is reasonably correct and
# addresses the user's question.
# If the answer is substantially correct,
# even if it is brief or not perfectly worded,
# return yes.

# Return "no" only if:
# - the answer is unrelated
# - the answer is incorrect
# - the answer is unsupported by the context
# - the answer fails to answer the question

# Question:
# {question}

# Retrieved Context:
# {context}

# Answer:
# {answer}
# """
#     result = answer_grader_structured_llm.invoke(
#         prompt
#     )
#     print("Answer Found:", result.answer_found)
    # return {
    #     "answer_found": result.answer_found
    # }