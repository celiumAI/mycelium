import llm

def construct_rephrase(system_message: str, task_prompt: str, note: str):
    def str_to_message(role: str, text: str):
        return {"role": role, "content": text}

    user_message = task_prompt.replace("<note>", note)

    roles = ["system", "user"]
    contents = [system_message, user_message]

    messages = [
        str_to_message(role, content)
        for role, content in zip(roles, contents)
    ]

    return messages

if __name__ == "__main__":
    messages_rephrase = construct_rephrase("a", "b<note>", "c")
    print(llm.chat(messages_rephrase))

