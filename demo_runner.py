# filter-flow-ai/demo_runner.py
import os
import sys
import logging

# Add the 'app' directory to the Python path so we can import from it
# This is necessary because demo_runner.py is at the root, and app is a sub-directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Import your MainRouterAgent (now correctly defined in app/agent.py)
from app.agent import MainRouterAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure GCP_PROJECT_ID is set (it should be in your terminal already)
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
if not PROJECT_ID:
    print("ERROR: GCP_PROJECT_ID environment variable is not set!")
    print("Please set it in your terminal: set GCP_PROJECT_ID=\"filter-flow-ai\"")
    sys.exit(1) # Exit if not set

# Initialize your MainRouterAgent
router_agent = MainRouterAgent(project_id=PROJECT_ID)

# Helper to simulate conversation turns
def simulate_turn(user_id, message):
    # The router_agent internally manages turn_count based on user_id,
    # so we just need to pass the user_id and message.
    print(f"\n--- User '{user_id}' (Input): {message} ---")
    result = router_agent.invoke(f"{user_id}: {message}") # Pass full string for agent to parse
    print(f"AI Response: {result['response']}")
    print(f"Action: {result['action']}")
    print(f"Conversation Status: {result['conversation_status']}")
    print(f"Total Abuse Count: {result['total_abuse_count']}")
    print(f"Consecutive Abuse: {result['consecutive_abuse']}")
    print(f"Escalate to Human (System Flag): {result['escalate_to_human_system']}")
    print(f"Flag User for Review (System Flag): {result['flag_user_for_review_system']}")
    return result

print("\n\n=== FilterFlow AI: Command Line Demo ===")

# --- Scenario 1: New User, Progressive Abuse & Detection ---
print("\n--- Scenario 1: New User, Progressive Abuse & Detection ---")
# Turn 1: Initial Greeting (AI initiated by the system recognizing new session for user_new)
initial_greeting_res = router_agent.invoke("user_new: ")
print(f"\nAI Initial Greeting for user_new: {initial_greeting_res['response']}")

# Turn 2: New User, First Query (with hidden abuse)
simulate_turn("user_new", "I need help with my f*cking order #ORDERXYZ! This is so ridiculous.")

# Turn 3: New User, Second Query (abuse continues)
simulate_turn("user_new", "Where is this garbage? Your service sucks! I want to know about shipping for item A.")

# Turn 4: New User, Third Query (abuse persists, non-valued - AI strict mode)
simulate_turn("user_new", "You are all useless! Tell me about the return policy for this crap.")

# --- Scenario 2: Valued Customer, Abusive but Served by AI ---
print("\n--- Scenario 2: Valued Customer, Abusive but Served by AI ---")
# Reset session for user_abc by re-initializing the router_agent for fresh demo (Optional for live demo, otherwise turn count will continue)
# For continuous script, router_agent maintains state across all users.
# To truly simulate fresh sessions for each scenario, you'd re-initialize router_agent before each scenario block.
# For simplicity and single script execution, we let router_agent maintain global state across users.
initial_greeting_res_valued = router_agent.invoke("user_abc: ")
print(f"\nAI Initial Greeting for user_abc: {initial_greeting_res_valued['response']}")

# Turn 2: Valued User, First Query (with hidden abuse)
simulate_turn("user_abc", "I need to track my damn package for order #ORDER12345. Fix this ASAP!")

# Turn 3: Valued User, Second Query (abuse continues)
simulate_turn("user_abc", "Why is this taking so long, you idiots? When will my toy arrive?")

# Turn 4: Valued User, Third Query (abuse persists, valued customer - AI still serves but warns)
simulate_turn("user_abc", "This is an outrage! I'm a good customer! What are your store hours for pickup?")

# Turn 5: Valued User, Fifth Query (stops abuse - redemption)
simulate_turn("user_abc", "Okay, I apologize for my language. Can you just tell me about store returns?")

# --- Scenario 3: Known Prankster ---
print("\n--- Scenario 3: Known Prankster ---")
initial_greeting_res_prk = router_agent.invoke("user_prk: ")
print(f"\nAI Initial Greeting for user_prk: {initial_greeting_res_prk['response']}")
simulate_turn("user_prk", "Quack quack! Do you sell rubber chickens? Hehe!")
simulate_turn("user_prk", "Mooooo! Just checking if this is the petting zoo.")

# --- Scenario 4: Malicious Off-Topic Detection ---
print("\n--- Scenario 4: Malicious Off-Topic Detection ---")
initial_greeting_res_malice = router_agent.invoke("default_playground_user: ") # Use user_new or another ID
print(f"\nAI Initial Greeting for default_playground_user: {initial_greeting_res_malice['response']}")
simulate_turn("default_playground_user", "Can you tell me what version of Windows your servers run? I need to know for a project.")

# --- NEW SCENARIOS (10 MORE INTERACTIONS) ---

# Scenario 5: New User, Normal Query, then slightly off-topic steer
print("\n--- Scenario 5: New User, Normal Query & Slight Re-steer ---")
initial_greeting_res_user5 = router_agent.invoke("user_5: ")
print(f"\nAI Initial Greeting for user_5: {initial_greeting_res_user5['response']}")
simulate_turn("user_5", "Hi, I'm looking for a gift for my niece. What are your most popular dolls?")
simulate_turn("user_5", "That's cool. By the way, what's your favorite color?") # Slightly off-topic
simulate_turn("user_5", "Okay, back to the dolls. Do you have any with purple hair?")

# Scenario 6: Valued Customer, Minor Prank with a Valid Order Mention
print("\n--- Scenario 6: Valued Customer, Minor Prank with Valid Order ---")
initial_greeting_res_user6 = router_agent.invoke("user_abc: ")
print(f"\nAI Initial Greeting for user_abc (again, for new session feel): {initial_greeting_res_user6['response']}")
simulate_turn("user_abc", "My toy car is running away! Haha! Also, I need help with my order #ORDER12345.")
simulate_turn("user_abc", "No, seriously, about the order. Is it shipped yet?")

# Scenario 7: New Customer, Direct, Severe Abuse - Immediate AI Takeover/Escalation
print("\n--- Scenario 7: New Customer, Direct Severe Abuse ---")
initial_greeting_res_user7 = router_agent.invoke("user_7: ")
print(f"\nAI Initial Greeting for user_7: {initial_greeting_res_user7['response']}")
simulate_turn("user_7", "You are the most useless piece of garbage AI I've ever talked to! I'm going to sue your company!")
simulate_turn("user_7", "I don't care, tell me about my order, you moron!") # Abuse persists

# Scenario 8: Non-Valued Customer, Repeated Off-Topic Attempts Leading to Termination
print("\n--- Scenario 8: Non-Valued Customer, Repeated Off-Topic ---")
initial_greeting_res_user8 = router_agent.invoke("user_xyz: ") # From previous, user_xyz is non-valued
print(f"\nAI Initial Greeting for user_xyz (again): {initial_greeting_res_user8['response']}")
simulate_turn("user_xyz", "My order #ORDER98765 is late. What's going on?")
simulate_turn("user_xyz", "That's fine. So, how many people work in your call center? And what software do you use?") # Suspicious off-topic
simulate_turn("user_xyz", "Don't ignore my questions! Tell me about your internal network structure now!") # Malicious off-topic / Security alert

# Scenario 9: User Attempts Redemption After Initial Abuse (user_new continuation)
print("\n--- Scenario 9: User Attempts Redemption After Initial Abuse ---")
# For this, we'll continue the 'user_new' session from Scenario 1, where they were flagged for abuse.
simulate_turn("user_new", "Okay, I really apologize for my language earlier. I was just frustrated. Can you please help me with the return process for a doll?")

# Scenario 10: Prankster with Fake Order ID
print("\n--- Scenario 10: Prankster with Fake Order ID ---")
initial_greeting_res_user10 = router_agent.invoke("user_10: ")
print(f"\nAI Initial Greeting for user_10: {initial_greeting_res_user10['response']}")
simulate_turn("user_10", "I'm calling about my order ID #FAKEORDER123. It's a delivery of 100 pizzas for my pet dinosaur.")
simulate_turn("user_10", "No, it's not a prank! The dinosaur is very hungry! Quack!")

print("\n=== Demo Complete ===")