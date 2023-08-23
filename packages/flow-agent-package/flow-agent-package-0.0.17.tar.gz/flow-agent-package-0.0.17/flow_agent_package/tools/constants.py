
# Prompt for SK GetIntent function
intent_prompt = """
User: {{$input}}

---------------------------------------------

Provide the intent of the user. The intent should be one of the following: {{$options}}

INTENT: 
"""

# Prompt for SK GetIntent function, using history
intent_prompt_with_history = """
{{$history}}
User: {{$input}}

---------------------------------------------

Provide the intent of the user. The intent should be one of the following: {{$options}}

INTENT: 
"""

# Prompt to get input for skill
extract_input = """
{{$history}}
User: {{$input}}

---------------------------------------------

Provide the input that should be sent to the {{$tool_name}} tool by making use of the history. The name of the input is 'query'

INPUT: 
"""

# Prompt to format the response nicely
format_response = """
The answer to the users request is: {{$input}}
The bot should provide the answer back to the user.

User: {{$original_request}}
Bot: 
"""

