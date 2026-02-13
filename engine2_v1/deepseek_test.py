from openai import OpenAI

DEEPSEEK_API_KEY = "REMOVEDcba2c84723ee4062980cab0f2dd2421a"

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="DeepSeek-V3.2",
    messages=[
        {"role": "user", "content": "Explain what AI is simply."}
    ]
)

print(response.choices[0].message.content)
