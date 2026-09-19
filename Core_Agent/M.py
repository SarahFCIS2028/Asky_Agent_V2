from groq import Groq

client = Groq(api_key="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")

models = client.models.list()

for model in models.data:
    print(model.id)