import os
import sys

# Load environment variables up front
from dotenv import load_dotenv
load_dotenv()

# Ensure project root is on the path
sys.path.append('.')

from api.models.event import Event
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from IPython.display import Image, display

# Set up database session
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment variables")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set in environment variables")

llm = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model="gemini-2.5-flash-preview-04-17")

# Define LangChain tools
@tool
def get_event_details() -> dict:
    """
    Returns a list of event details in JSON:
    event_id, branch_id, title, description, event_date, location,
    is_paid, price, max_capacity, imageUrl, created_at
    """
    try:
        events = []
        all_events = session.query(Event).order_by(Event.updated_at.desc()).all()
        for e in all_events:
            events.append({
                'event_id': e.event_id,
                'branch_id': e.branch_id,
                'title': e.title,
                'description': e.description,
                'event_date': e.event_date.isoformat(),
                'location': e.location,
                'is_paid': e.is_paid,
                'price': e.price,
                'max_capacity': e.max_capacity,
                'imageUrl': e.imageUrl,
                'created_at': e.created_at.isoformat(),
            })
        return {'success': True, 'events': events}
    except Exception as err:
        return {'success': False, 'error': str(err)}

@tool
def get_policy() -> str:
    """Return policy descriptions from policies.txt"""
    policies_path = os.path.join(os.path.dirname(__file__), 'backend', 'chatbot', 'policies.txt')
    with open(policies_path, 'r') as f:
        return f.read()

# Bind tools to the LLM
tools = [get_event_details, get_policy]
llm_with_tools = llm.bind_tools(tools)

# Build the RAG/Tool invocation graph
sys_msg = SystemMessage(content="You are a helpful assistant providing event details and policies.")

def assistant_node(state: MessagesState):
    # Invoke LLM with accumulated messages
    response = llm_with_tools.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}

builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant_node)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")
react_graph = builder.compile()

# Display graph structure (Jupyter only)
try:
    display(Image(react_graph.get_graph(xray=True).draw_mermaid_png()))
except Exception:
    pass

# Chatbot function

def chatbot(query: str) -> str:
    messages = [HumanMessage(content=query)]
    state = react_graph.invoke({"messages": messages})
    return state["messages"][-1].content

# CLI loop
if __name__ == "__main__":
    print("Chatbot is running. Type 'exit' or 'quit' to stop.")
    with Session() as session: 
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Chatbot: Goodbye!")
                break
            print("Chatbot:", chatbot(user_input))
