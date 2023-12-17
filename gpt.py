import openai
openai.api_key = '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'
def get_chat_completion(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return str(e)