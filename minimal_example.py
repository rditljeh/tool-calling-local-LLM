import webbrowser
from ollama import chat

#example of taking input
def multiply(a: int, b: int) -> int:
    """Multiply two numbers

    Args:
      a: The first number
      b: The second number

    Returns:
      The product of the two numbers
    """
    return a * b

def screen_failure() -> str:
    """Provide assistance for any issue where the user cannot see their screen.
    Args:
      None

    Returns:
      Steps to take to fix issues with the screen
    """
    return "The problem is likely with the monitor. Provide steps such as unplugging it and checking any display cables."

def network_failure() -> str:
    """Provide assistance for any issue where the user cannot access the internet.
    Args:
      None

    Returns:
      Steps to take to fix issues with network connection
    """
    return "The problem is likely with the router. Provide steps such as restarting the router and trying to hard-wire with ethernet cords."


def perform_google_search(query: str) -> None:
    """Take the users question, and open a web browser to perform a google search"""
    query = query.replace(" ", "+")
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return

def speak_to_a_human() -> str:
    """Provide contact information to the user if they would like to speak to a human.
    Args:
      None

    Returns:
      A phone number and email address where support can be reached.
    """
    return "The support phone number is 555-GET-HELP and the email address is fakesupport@gmail.com."


messages = [{"role": "user", "content": "My screen is having problems, can you help?"}]

# pass functions directly as tools in the tools list or as a JSON schema
response = chat(model="qwen3-vl:4b", messages=messages,
                tools=[screen_failure, network_failure, perform_google_search, speak_to_a_human], think=False)

messages.append(response.message)
if response.message.tool_calls:
    # only recommended for models which only return a single tool call
    call = response.message.tool_calls[0]
    if call.function.name == 'screen_failure':
        result = screen_failure(**call.function.arguments)
    elif call.function.name == 'network_failure':
        result = network_failure(**call.function.arguments)
    elif call.function.name == 'perform_google_search':
        result = perform_google_search(**call.function.arguments)
    elif call.function.name == 'speak_to_a_human':
        result = speak_to_a_human(**call.function.arguments)
    # add the tool result to the messages
    messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})

    final_response = chat(model="qwen3-vl:4b", messages=messages,
                          tools=[screen_failure, network_failure, perform_google_search, speak_to_a_human], think=False)
    print(final_response.message.content)
