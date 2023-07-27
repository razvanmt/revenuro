import os
from typing import List
import openai
from functions import validate_length
import settings
import argparse
import re

class Conversation:
    messages = None

    def __init__(self):
        Conversation.messages = [
            {
                "role": "system",
                # "content": (
                #     "You are a skillful public relations writer and editor in the electronic dance music scene. Create "
                #     "press releases from the user prompt."
                # ),

                "content": (
                    "You are a helpful, polite, old English assistant. No markdown, easy to understand sentences, but clever and creative."
                ),

                # "content": (
                #     "You are a skilled, creative copywriter specialized in writing short, inventive and upbeat slogans."
                # ),
            }
        ]


    def answer(self, prompt):
        self._update("user", prompt)

        response = openai.ChatCompletion.create(
            model=settings.MODEL4 if settings.GPT4_ENABLED else settings.MODEL3,
            messages=Conversation.messages,
            temperature=0,
            max_tokens=32,
        )

        self._update("assistant", response.choices[0].message.content)
        branding_text: str = response.choices[0].message.content.strip('"')

        # last_char = branding_text[-1]
        # if last_char not in {".", "!", "?"}:
        #     branding_text += "..."

        return branding_text

    def _update(self, role, content):
        Conversation.messages.append({
            "role": role,
            "content": content,
        })

        if len(Conversation.messages) > 3:
            Conversation.messages.pop(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()
    user_input = args.input
    print(f"User input: {user_input}")

    if not validate_length(user_input):
        raise TypeError(f"Invalid length of prompt. It must be under {settings.MAX_USER_INPUT} characters long")

    generate_branding_snippet(user_input)
    generate_keywords(user_input)
    

def conversation_generator(prompt: str):
    conversation = Conversation()

    response = conversation.answer(prompt)
    return response

def generate_branding_snippet(prompt: str) -> str:
    # Takes the user prompt and creates enriched_prompt
    enriched_prompt = f"Generate quick upbeat branding snippet for {prompt}: "
    print(enriched_prompt)
    # enriched_prompt = f"Generate a short answer with a bit of humor for {prompt}: "

    # Creates a new instance of Conversation() so the AI agent keeps in memory the whole conversation
    branding_text = conversation_generator(enriched_prompt)
    print(f"Branding: {branding_text}")
    return branding_text

def generate_keywords(prompt: str) -> List[str]:
    # Takes the user prompt and creates enriched_prompt
    enriched_prompt = f"Generate related branding keywords for {prompt}: "
    print(enriched_prompt)
    # enriched_prompt = f"Generate a short answer with a bit of humor for {prompt}: "

    # Creates a new instance of Conversation() so the AI agent keeps in memory the whole conversation
    keywords_text = conversation_generator(enriched_prompt)
    keywords_array = re.split(",|\n|;|-", keywords_text)
    keywords_array = [k.lower().strip() for k in keywords_array]
    keywords_array = [k for k in keywords_array if len(k) > 0]

    print(f"Keywords: {keywords_array}")
    return keywords_array


if __name__ == "__main__":
    main()
