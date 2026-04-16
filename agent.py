from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

from prompts import (
    SYSTEM_PROMPT,
    PLAN_PROMPT,
    NEXT_QUERY_PROMPT,
    SUFFICIENCY_PROMPT,
    FINAL_SUMMARY_PROMPT,
)
from tools import search_web


load_dotenv()


def get_llm():
    return ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )


def format_search_results(results: list[dict]) -> str:
    if not results:
        return "No search results found."

    lines = []
    for i, item in enumerate(results, start=1):
        lines.append(
            f"""Result {i}
Title: {item['title']}
URL: {item['url']}
Snippet: {item['snippet']}
"""
        )
    return "\n".join(lines)


def make_research_plan(question: str) -> str:
    llm = get_llm()
    prompt = PLAN_PROMPT.format(question=question)
    response = llm.invoke(prompt)
    return response.content.strip()


def generate_next_query(
    question: str,
    research_plan: str,
    evidence: str,
    round_number: int,
) -> str:
    llm = get_llm()
    prompt = NEXT_QUERY_PROMPT.format(
        question=question,
        research_plan=research_plan,
        evidence=evidence,
        round_number=round_number,
    )
    response = llm.invoke(prompt)
    return response.content.strip()


def is_evidence_sufficient(question: str, evidence: str) -> bool:
    llm = get_llm()
    prompt = SUFFICIENCY_PROMPT.format(
        question=question,
        evidence=evidence,
    )
    response = llm.invoke(prompt).content.strip().upper()
    return response.startswith("YES")


def generate_final_summary(question: str, research_plan: str, evidence: str) -> str:
    llm = get_llm()
    prompt = FINAL_SUMMARY_PROMPT.format(
        question=question,
        research_plan=research_plan,
        evidence=evidence,
    )
    response = llm.invoke([
        ("system", SYSTEM_PROMPT),
        ("user", prompt),
    ])
    return response.content.strip()


def run_research_agent(question: str, max_rounds: int = 3) -> dict:
    research_plan = make_research_plan(question)

    all_rounds = []
    collected_evidence_parts = []

    for round_number in range(1, max_rounds + 1):
        current_evidence = "\n\n".join(collected_evidence_parts) if collected_evidence_parts else "None yet."

        search_query = generate_next_query(
            question=question,
            research_plan=research_plan,
            evidence=current_evidence,
            round_number=round_number,
        )

        search_results = search_web(search_query, max_results=6)
        formatted_results = format_search_results(search_results)

        collected_evidence_parts.append(
            f"""Round {round_number}
Search Query: {search_query}
Search Results:
{formatted_results}
"""
        )

        all_rounds.append(
            {
                "round_number": round_number,
                "search_query": search_query,
                "search_results": search_results,
            }
        )

        combined_evidence = "\n\n".join(collected_evidence_parts)

        if is_evidence_sufficient(question, combined_evidence):
            break

    final_evidence = "\n\n".join(collected_evidence_parts)
    summary = generate_final_summary(question, research_plan, final_evidence)

    return {
        "question": question,
        "research_plan": research_plan,
        "rounds": all_rounds,
        "summary": summary,
        "evidence": final_evidence,
    }