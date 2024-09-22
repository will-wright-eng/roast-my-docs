import os
import openai
import weave

def main():
    weave.init("roast-my-docs")

    system_content = "You are a travel agent. Be descriptive and helpful."
    user_content = "Tell me about San Francisco"

    client = openai.OpenAI(
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )
    chat_completion = client.chat.completions.create(
        extra_headers={
            # "HTTP-Referer": "",
            "X-Title": "My App",
        },
        model="microsoft/phi-3-mini-128k-instruct:free",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
        temperature=0.7,
        max_tokens=1024,
    )
    response = chat_completion.choices[0].message.content
    print("Model response:\n", response)
