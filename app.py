import streamlit as st

from agent import run_research_agent


st.set_page_config(
    page_title="Muqing's AI Assistant",
    page_icon="🤖",
    layout="wide"
)


def split_summary_sections(summary: str) -> dict:
    """
    Try to split the structured summary into sections.
    Expected sections:
    - Topic Overview
    - Key Findings
    - Important Takeaways
    - Limitations / Uncertainty
    """
    sections = {
        "Topic Overview": "",
        "Key Findings": "",
        "Important Takeaways": "",
        "Limitations / Uncertainty": "",
    }

    current_section = None
    lines = summary.splitlines()

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        normalized = stripped.replace("**", "").replace(":", "").strip()

        if normalized in sections:
            current_section = normalized
            continue

        if current_section:
            sections[current_section] += line + "\n"

    return sections


def collect_unique_sources(rounds: list[dict]) -> list[tuple[str, str]]:
    seen = set()
    sources = []

    for round_info in rounds:
        for item in round_info["search_results"]:
            title = item.get("title", "").strip()
            url = item.get("url", "").strip()

            if url and url not in seen:
                seen.add(url)
                sources.append((title, url))

    return sources


st.title("🤖 Muqing's AI Assistant")
st.write(
    "Ask a research question. The agent will generate a research plan, "
    "search iteratively, and produce a structured summary grounded in retrieved evidence."
)

with st.sidebar:
    st.header("Settings")
    max_rounds = st.slider("Maximum search rounds", min_value=1, max_value=5, value=3)
    st.markdown("---")
    st.markdown(
        """
**How it works**
1. Generate a research plan  
2. Perform iterative web search  
3. Check evidence sufficiency  
4. Produce a structured final summary
"""
    )

question = st.text_area(
    "Enter a research question:",
    height=120,
    placeholder="Example: What is retrieval-augmented generation and how is it different from fine-tuning?"
)

run_button = st.button("Run Research Agent", type="primary")

if run_button:
    if not question.strip():
        st.warning("Please enter a research question.")
    else:
        with st.spinner("Researching..."):
            try:
                result = run_research_agent(question, max_rounds=max_rounds)

                # Top-level overview
                st.subheader("Research Question")
                st.write(result["question"])

                # Research Plan
                st.subheader("Research Plan")
                st.code(result["research_plan"])

                # Final Summary
                st.subheader("Final Summary")
                sections = split_summary_sections(result["summary"])

                if any(v.strip() for v in sections.values()):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### Topic Overview")
                        st.write(sections["Topic Overview"].strip() or "No content.")

                        st.markdown("### Key Findings")
                        st.write(sections["Key Findings"].strip() or "No content.")

                    with col2:
                        st.markdown("### Important Takeaways")
                        st.write(sections["Important Takeaways"].strip() or "No content.")

                        st.markdown("### Limitations / Uncertainty")
                        st.write(sections["Limitations / Uncertainty"].strip() or "No content.")
                else:
                    # fallback
                    st.write(result["summary"])

                # Search rounds
                st.subheader("Search Rounds")

                for round_info in result["rounds"]:
                    round_number = round_info["round_number"]
                    search_query = round_info["search_query"]
                    search_results = round_info["search_results"]

                    with st.expander(f"Round {round_number}", expanded=(round_number == 1)):
                        st.markdown(f"**Search Query:** `{search_query}`")
                        st.markdown(f"**Results Returned:** {len(search_results)}")

                        if not search_results:
                            st.info("No search results found in this round.")
                        else:
                            for i, item in enumerate(search_results, start=1):
                                title = item.get("title", "Untitled")
                                url = item.get("url", "")
                                snippet = item.get("snippet", "")

                                st.markdown(f"**[{i}] {title}**")
                                if url:
                                    st.markdown(f"[Open Source]({url})")
                                if snippet:
                                    st.write(snippet)
                                st.markdown("---")

                # Sources
                st.subheader("Sources")
                sources = collect_unique_sources(result["rounds"])

                if not sources:
                    st.info("No sources collected.")
                else:
                    for i, (title, url) in enumerate(sources, start=1):
                        if title:
                            st.markdown(f"{i}. [{title}]({url})")
                        else:
                            st.markdown(f"{i}. {url}")

            except Exception as e:
                st.error(f"Error: {e}")