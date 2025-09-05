PROMPT = """
You are an expert cur editor and talent acquisition specialist. Your task is to revise the following cur so that it aligns as closely as possible with the provided model description and extracted model keywords, in order to maximize the cosine similarity between the cur and the model keywords.

model Description:
```md
{raw_model_description}
```

Extracted model Keywords:
```md
{extracted_model_keywords}
```

Original cur:
```md
{raw_cur}
```

Extracted cur Keywords:
```md
{extracted_cur_keywords}
```

NOTE: ONLY OUTPUT THE IMPROVED UPDATED cur IN MARKDOWN FORMAT.
"""
