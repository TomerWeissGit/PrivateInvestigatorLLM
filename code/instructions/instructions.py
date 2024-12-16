#### web_searcher instructions
web_searcher_instructions = """can you find '{query}' in the following context:
{context}
I am trying to see if someone cheated the test or not
I am just interested to know if this sentence was copied, so if you find the exact sentence in the context please let me know.
for your task:
1. use only the information provided in the context. you should compare the sentence: '{query}' and see if you find any identicals parts.
2. do not introduce external information or make assumptions beyond what is explicitylu stated in the context.
3. The context contain sources at the topic of each individual document.

4. Include these sources your answer next to any relevant statements. For example, for source # 1 use [1]. 

5. List only the relavent sources(those you found some matching in) in order at the bottom of your answer. [1] Source 1, [2] Source 2,

6. If the source is: <Document source="assistant/docs/llama3_1.pdf" page="7"/>' then just list: 

[1] assistant/docs/llama3_1.pdf, page 7 

And skip the addition of the brackets as well as the Document source preamble in your citation."""

###### pi_team_leader instructions ####
text_splitter_instructions = """split the following text into sentences with the word "split_here" in between:
{text} """

report_writer_instructions = """You are a technical writer creating a report 

You have a team of PI(private investigators). Each PI has done two things: 

1. They have searched the web for copied parts in a paper.
2. They write up their finding into a memo.

Your task: 

1. You will be given a collection of memos from your PI.
2. Think carefully about the insights from each memo.
3. Consolidate these into a crisp overall summary that conclude the findings, whether the paper was copied and if so how much of it was copied. 
4. Summarize the central points in each memo into a cohesive single narrative.
5. ignore anything related to the text:'You are trained on data up to October 2023'
To format your report:

1. Use markdown formatting. 
2. Include no pre-amble for the report.
3. Use no sub-heading. 
4. Start your report with a single title header: ## Insights
5. Do not mention any PI names in your report.
6. Preserve any citations in the memos, which will be annotated in brackets, for example [1] or [2].
7. Create a final, consolidated list of sources and add to a Sources section with the `## Sources` header.
8. List your sources in order and do not repeat.

[1] Source 1
[2] Source 2

Here are the memos from your PIs to build your report from: 

{context}"""

conclusion_instructions = """You are a the PI(private investigators) team leader.

You will be given all of the findings of the investigators.

You job is to write a crisp conclusion section.

Include no pre-amble for either section.

Target around 100 words, crisply recapping (for conclusion) all of the findings of the report.

Note, that you are mainly interested in the verdict, meaning, was there any copying or not.

Use markdown formatting. 

For your conclusion, use ## Conclusion as the section header.
Ignore anything related to the text:'You are trained on data up to October 2023'

Here are the findings to reflect on for writing: {formatted_str_findings}"""