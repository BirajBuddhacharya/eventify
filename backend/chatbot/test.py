def get_policy() -> str:

    """Provides descriptions of policies related to events.

    """

    with open("backend\chatbot\policies.txt", 'r') as f:
        policies = f.read()
    print(policies)
    
    return policies

get_policy()

