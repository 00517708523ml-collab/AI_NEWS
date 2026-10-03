import gradio as gr

from Backend import dashboard, ask_query


# ============================================================
# GLOBAL NEWS DATA
# ============================================================

news_data = []


# ============================================================
# FORMAT NEWS
# ============================================================

def format_news(news):

    if not news:

        return """
# 📰 AI News Dashboard

No news available.

Click **🔄 Refresh News** to load the latest AI news.
"""

    output = """
# 📰 Latest AI News

> Automatically collected from AI companies, AI news websites,
> research platforms and open-source AI communities.

"""

    for index, item in enumerate(news, start=1):

        source = item.get(
            "source",
            "Unknown Source"
        )

        content = item.get(
            "content",
            ""
        )

        # ----------------------------------------------------
        # Limit content shown in dashboard
        # ----------------------------------------------------

        content = content[:5000]

        output += f"""
---

## {index}. 🌐 {source}

{content}

"""

    return output


# ============================================================
# LOAD NEWS
# ============================================================

def load_news():

    global news_data

    try:

        for news in dashboard():

            news_data = news

            yield format_news(news)

    except Exception as error:

        yield f"# ❌ Error Loading News\n\n{error}"
    

def search(query):

    if not query or not query.strip():
        return "Please enter a search query."

    try:
        exa_results, tavily_results = ask_query(query)

    except Exception as error:
        return f"# ❌ Search Error\n\n{error}"

    output = f"# 🔎 Search Results for: `{query}`\n\n"

    # ========================================================
    # EXA RESULTS
    # ========================================================

    output += "## 🔵 Exa Results\n\n"

    if exa_results and exa_results.results:

        for index, r in enumerate(exa_results.results, start=1):

            title = r.title or "No title"
            url = r.url or ""
            
            # Exa highlights
            highlights = getattr(r, "highlights", None)

            output += f"""
### {index}. {title}

"""

            if highlights:

                if isinstance(highlights, list):
                    output += "\n".join(highlights)

                else:
                    output += str(highlights)

            else:

                output += "No content available."

            output += f"""

**Source:** {url}

---
"""

    else:

        output += "No Exa results found.\n\n"


    # ========================================================
    # TAVILY RESULTS
    # ========================================================

    output += "## 🟢 Tavily Results\n\n"

    tavily_list = tavily_results.get("results", [])

    if tavily_list:

        for index, r in enumerate(tavily_list, start=1):

            title = r.get("title", "No title")
            content = r.get("content", "No content available")
            url = r.get("url", "")

            output += f"""
### {index}. {title}

{content}

**Source:** {url}

---
"""

    else:

        output += "No Tavily results found."

    return output


with gr.Blocks(title="AI News Dashboard") as app:
    gr.Markdown("# 📰 AI News Dashboard")

    with gr.Tab("Latest News"):
        refresh_btn = gr.Button("🔄 Refresh News")
        news_output = gr.Markdown(format_news([]))
        refresh_btn.click(load_news, outputs=news_output)

    with gr.Tab("Search"):
        query = gr.Textbox(label="Search AI news")
        search_btn = gr.Button("Search")
        search_output = gr.Markdown()
        search_btn.click(search, inputs=query, outputs=search_output)
        query.submit(search, inputs=query, outputs=search_output)

app.launch(share = True)