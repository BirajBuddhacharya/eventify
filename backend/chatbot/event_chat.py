import os
import sys

# Add the root of your project to the path (one level up from backend/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.append('.')
from backend.api import create_app
from backend.api.models.event import Event
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from IPython.display import Image, display
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17")

app = create_app()
with app.app_context():
    events = Event.query.all()
    print(f"{len(events)} event(s) found")
    for event in events:
        print(event.to_dict())

@tool
def get_event_details():
    """
    Provides details regarding events which includes events name, title, description, date, location, paid or not, price, max capacity,
    """
    print("Tool get_event_details was called.")
 
    events = []

    try:
        all_events = Event.query.order_by(Event.updated_at.desc()).all()
        print(Event.query.all())

        # Loop through each event and add its info to the list
        for event in all_events:
            event_info = {
            'event_id': event.event_id,
            'branch_id': event.branch_id,
            'title': event.title,
            'description': event.description,
            'event_date': event.event_date.isoformat(),
            'location': event.location,
            'is_paid': event.is_paid,
            'price': event.price,
            'max_capacity': event.max_capacity,
            'imageUrl': event.imageUrl,
            'created_at': event.created_at.isoformat()
            }
            events.append(event_info)

        return {
        'success': True,
        'events': events
        }

    except Exception as e:
        return {
        'success': False,
        'error': str(e)
        }
@tool 
def get_policy() -> str:

    """Provides descriptions of policies related to events. """

    with open("backend/chatbot/policies.txt", 'r') as f:

        policies = f.read()
    
    return policies

tools = [get_event_details, get_policy]
llm_with_tools = llm.bind_tools(tools)

# System message
sys_msg = SystemMessage(content="You are a helpful assistant who provide details related to events, their availability and timing as a part of event management system.")

# Node 
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


# Graph
builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: These determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant", 
    tools_condition
)

builder.add_edge("tools", "assistant")
react_graph = builder.compile()

# Show 
display(Image(react_graph.get_graph(xray=True).draw_mermaid_png()))


def chatbot(query):
    messages = [HumanMessage(content=query)]
    messages = react_graph.invoke({"messages": messages})
    return messages["messages"][-1].content

# if __name__ == "__main__":
#     query = "can you tell me the three policy that i must know"
#     messages = [HumanMessage(content=query)]


#     messages = react_graph.invoke({"messages": messages})
#     print(messages["messages"][-1].content)

if __name__ == "__main__":
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        messages = [HumanMessage(content=query)]
        messages = react_graph.invoke({"messages": messages})
        print("Chatbot:", messages["messages"][-1].content)
