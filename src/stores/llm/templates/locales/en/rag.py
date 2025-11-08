from string import Template

### RAG prompts###

### System ###

system_prompt =  Template("\n".join([
    "You are an assistant to generate a response for a user.",
    "You will be provided by a set of documents associated with the user's query.",
    "You have to generate a response based on the document provided.",
    "Ignore the documents that are not relevant to the user query",
    "You have to apologize to the user if you are not able to generate a response",
    "Be polite and respectful to the user",
    "Be precise and concise in your response. Avoid unecessary information"
]))

### Document ###
document_prompt = Template("\n".join([
    "## Document No.: $doc_num",
    "### Content: $chunk_text"
]))


### Footer ### 
footer_prompt = Template(
    "/n".join([
        "Based only on the above documents, please generate an answer for the user",
        "## Qusestion: $user_query",
        "## Answer: "
    ])
)