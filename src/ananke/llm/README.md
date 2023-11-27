LLM Support
- OpenAI

example:

```python


assistant = AzureOpenAI(api_key, api_version, azure_endpoint)

df = pd.DataFrame(
    {
        "text": [
            "NASA traces its roots to the National Advisory Committee for Aeronautics (NACA). ",
            "Determined to regain American leadership in aviation, Congress created the Aviation Section of the U.S. Army Signal Corps in 1914 and established NACA in 1915 to foster aeronautical research and development.",
        ]
    }
)

df = assistant.embedding_df(df, "text")


print(df)

print(assistant.search_docs(df, "What is nasa root from?"))

                                               text  n_tokens                                    AnankeEmbedding
0  NASA traces its roots to the National Advisory...        18  [-0.001609626691788435, -0.01872904784977436, ...
1  Determined to regain American leadership in av...        43  [-0.023721234872937202, -0.02078939788043499, ...
1536
                                                text  ...  similarities
0  NASA traces its roots to the National Advisory...  ...      0.801512
1  Determined to regain American leadership in av...  ...      0.745144

[2 rows x 4 columns]
                                                text  ...  similarities
0  NASA traces its roots to the National Advisory...  ...      0.801512
1  Determined to regain American leadership in av...  ...      0.745144

```



- Anthropic
- Gradient
- Hugging Face
- EverlyAI
- LiteLLM
- PaLM
- Predibase
- Replicate
- LangChain
- Llama API
- Llama CPP
- Xorbits Inference
- MonsterAPI
- RunGPT
- Portkey
- AnyScale
- Ollama
- Konko