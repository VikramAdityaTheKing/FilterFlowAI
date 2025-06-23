# filter-flow-ai/app/agent.py (FINAL VERSION - GEMINI API CALLS MOCKED FOR DEMO)
import os
import logging
# from adk.agents import Agent # REMOVED
# from adk.graph import Application # REMOVED
# from vertexai.preview.generative_models import GenerativeModel # REMOVED for mocking
import json
import re
import time

# --- CustomerProfileTool (DEFINED DIRECTLY IN THIS FILE) ---
class CustomerProfileTool:
    def __init__(self):
        self.customer_data = {
            "user_abc": {"is_valued": True, "total_orders": 15, "recent_order_value": 250.00, "is_flagged_prankster": False},
            "user_xyz": {"is_valued": False, "total_orders": 1, "recent_order_value": 15.00, "is_flagged_prankster": False},
            "user_prk": {"is_valued": False, "total_orders": 0, "recent_order_value": 0.00, "is_flagged_prankster": True},
            "user_new": {"is_valued": False, "total_orders": 0, "recent_order_value": 0.00, "is_flagged_prankster": False},
            "default_playground_user": {"is_valued": False, "total_orders": 0, "recent_order_value": 0.00, "is_flagged_prankster": False}
        }
        logging.info("CustomerProfileTool initialized with mock data.")

    def get_customer_profile(self, user_id: str) -> dict:
        profile = self.customer_data.get(user_id, self.customer_data["default_playground_user"])
        logging.info(f"Retrieved profile for user '{user_id}': {profile}")
        return profile

    def get_order_details(self, order_id: str) -> dict:
        mock_orders = {
            "ORDER12345": {"user_id": "user_abc", "value": 250.00, "confirmed": True},
            "ORDER98765": {"user_id": "user_xyz", "value": 15.00, "confirmed": True},
            "ORDER00000": {"user_id": "user_prk", "value": 5.00, "confirmed": False},
        }
        order_info = mock_orders.get(order_id, {"value": 0.0, "confirmed": False})
        logging.info(f"Retrieved order details for order '{order_id}': {order_info}")
        return order_info

# --- End CustomerProfileTool ---


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# PROJECT_ID is still needed for logging/context, but not directly for model loading now
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
if not PROJECT_ID:
    logging.error("GCP_PROJECT_ID environment variable not set. Using fallback 'filter-flow-ai'.")
    PROJECT_ID = "filter-flow-ai"

# --- AbuseDetectionAgent (Mocks Gemini responses) ---
class AbuseDetectionAgent:
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        # self.model = GenerativeModel("gemini-pro") # MOCKED: No longer calling Gemini API
        logging.info(f"Initialized AbuseDetectionAgent for project {project_id} in {location}.")

    def analyze_text(self, text_input: str) -> dict:
        # MOCKING GEMINI BEHAVIOR BASED on keywords to simulate detection
        lower_input = text_input.lower()

        if "f*cking" in lower_input or "garbage" in lower_input or "sucks" in lower_input or "useless" in lower_input or "idiots" in lower_input or "moron" in lower_input or "crap" in lower_input:
            return {"category": "abusive_language", "severity": 4, "reason": "Simulated: Detected offensive terms.", "suggested_action": "simulated_escalate"}
        if "quack" in lower_input or "moooo" in lower_input or "hehe" in lower_input or "pet dinosaur" in lower_input or "pizzas for" in lower_input:
            return {"category": "prank_call", "severity": 2, "reason": "Simulated: Detected prank keywords.", "suggested_action": "simulated_warning"}

        # Default to normal if no keywords
        return {"category": "normal_query", "summary": "Simulated: General query.", "suggested_action": "simulated_response"}

# --- StandardQueryAgent (Mocks Gemini responses) ---
class StandardQueryAgent:
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.name = "StandardQueryAgent"
        self.description = "Handles legitimate customer inquiries using a generative AI model."
        self.project_id = project_id
        self.location = location
        # self.model = GenerativeModel("gemini-pro") # MOCKED: No longer calling Gemini API
        logging.info(f"StandardQueryAgent initialized for project {project_id} in {location}.")

    def invoke(self, input_data: dict) -> dict:
        message = input_data.get("message", "")
        # MOCKING GEMINI BEHAVIOR
        if "shipping" in message.lower() or "delivery" in message.lower():
            return {"response": "Simulated AI Response: Your shipping details are being looked up. Delivery usually takes 3-5 business days."}
        if "return" in message.lower() or "returns" in message.lower():
            return {"response": "Simulated AI Response: For returns, please visit our website's returns policy page or provide an order ID for specific instructions."}
        if "store hours" in message.lower():
            return {"response": "Simulated AI Response: Our store hours are Monday-Friday, 9 AM to 7 PM, and Saturday 10 AM to 5 PM."}
        if "dolls" in message.lower():
            return {"response": "Simulated AI Response: Our most popular dolls include the Starlight Princess and the Adventure Explorer series."}

        return {"response": f"Simulated AI Response: I can help with general toy store queries. You asked: '{message}'"}


# --- MainRouterAgent (Your Primary FilterFlowAI Logic) ---
class MainRouterAgent:
    def __init__(self, project_id: str):
        self.name = "MainRouterAgent"
        self.description = "Routes incoming customer queries, manages abuse detection, and applies adaptive response strategies based on customer history and conversation state."
        self.project_id = project_id
        # self.model = GenerativeModel("gemini-pro") # MOCKED: No longer calling Gemini API for focus assessment
        self.abuse_detector = AbuseDetectionAgent(project_id=project_id)
        self.standard_query_agent = StandardQueryAgent(project_id=project_id)
        self.customer_profile_tool = CustomerProfileTool()

        self.conversation_states = {}
        logging.info("MainRouterAgent initialized with advanced routing logic and state management.")

    def _extract_order_id(self, text: str) -> str | None:
        match = re.search(r'(?:order|id|transaction|ref)[\s#]*(\w{5,})', text, re.IGNORECASE)
        if match:
            return match.group(1).upper()
        return None

    def _assess_conversation_focus(self, conversation_history: list[str], current_message: str, main_topic: str = "customer service query related to orders or products") -> dict:
        # MOCKING GEMINI BEHAVIOR
        lower_input = current_message.lower()

        if "windows" in lower_input or "servers" in lower_input or "network structure" in lower_input or "software" in lower_input:
            return {"focus_status": "off_topic_suspicious", "reason": "Simulated: Asking about internal systems.", "flag_potential_malice": True}
        if "color" in lower_input or "sick" in lower_input or "cat" in lower_input:
            return {"focus_status": "slightly_off_topic", "reason": "Simulated: Personal or irrelevant question.", "flag_potential_malice": False}

        return {"focus_status": "on_topic", "reason": "Simulated: On topic.", "flag_potential_malice": False}


    def invoke(self, text_input: str) -> dict:
        user_id_match = re.match(r'^(user_new|user_abc|user_xyz|user_prk|default_playground_user|user_5|user_7|user_10):?\s*(.*)', text_input, re.IGNORECASE)
        if user_id_match:
            user_id = user_id_match.group(1).lower()
            message = user_id_match.group(2).strip()
        else:
            user_id = "default_playground_user"
            message = text_input

        if user_id not in self.conversation_states:
            self.conversation_states[user_id] = {
                "turn_count": 0,
                "abuse_count": 0,
                "abuse_flagged_round": 0,
                "consecutive_abuse_count": 0,
                "last_input_was_abuse": False,
                "status": "normal",
                "order_details_requested": False,
                "history": []
            }

        current_state = self.conversation_states[user_id]

        if current_state["turn_count"] == 0:
            current_state["turn_count"] += 1
            current_state["history"].append("AI: Hello! Welcome to our customer service. How may I be of service? Please tell me your query, and if you have one, include your Order ID for faster assistance.")
            current_state["order_details_requested"] = True
            return {
                "response": "Hello! Welcome to our customer service. How may I be of service? Please tell me your query, and if you have one, include your Order ID for faster assistance.",
                "action": "INITIAL_GREETING",
                "user_id": user_id,
                "current_turn_count": current_state["turn_count"],
                "detection_category": "N/A",
                "conversation_status": current_state["status"],
                "total_abuse_count": current_state["abuse_count"],
                "consecutive_abuse": current_state["consecutive_abuse_count"],
                "escalate_to_human_system": False,
                "flag_user_for_review_system": False
            }

        current_state["turn_count"] += 1
        current_turn_count = current_state["turn_count"]
        current_state["history"].append(f"User: {message}")

        logging.info(f"MainRouterAgent received input for user '{user_id}' (Turn {current_turn_count}): '{message}'")

        customer_profile = self.customer_profile_tool.get_customer_profile(user_id)
        is_valued_customer = customer_profile.get("is_valued", False)
        total_orders = customer_profile.get("total_orders", 0)
        recent_order_value = customer_profile.get("recent_order_value", 0.0)
        is_flagged_prankster_in_db = customer_profile.get("is_flagged_prankster", False)

        # --- MOCKED Gemini Calls ---
        detection_result = self.abuse_detector.analyze_text(message) # This now uses mocked detection
        category = detection_result.get("category")
        severity = detection_result.get("severity", 0)
        reason = detection_result.get("reason", "N/A")

        is_current_message_abuse = (category in ["abusive_language", "prank_call", "spam_or_unrelated"] and severity > 0)

        if is_current_message_abuse:
            current_state["consecutive_abuse_count"] += 1
            current_state["abuse_count"] += 1
            current_state["last_input_was_abuse"] = True
        else:
            current_state["consecutive_abuse_count"] = 0
            current_state["last_input_was_abuse"] = False

        order_id = self._extract_order_id(message)
        order_details = None
        if order_id:
            order_details = self.customer_profile_tool.get_order_details(order_id)
            logging.info(f"Order ID '{order_id}' found. Details: {order_details}")

        focus_assessment = self._assess_conversation_focus( # This now uses mocked focus
            conversation_history=current_state["history"][:-1],
            current_message=message,
            main_topic="customer service query related to toy store orders or products"
        )
        focus_status = focus_assessment.get("focus_status")
        flag_potential_malice = focus_assessment.get("flag_potential_malice", False)
        focus_reason = focus_assessment.get("reason", "")

        response_to_user = ""
        action_taken = ""
        escalate_to_human_system = False
        flag_user_for_review_system = False

        query_response_data = self.standard_query_agent.invoke({"message": message, "user_id": user_id}) # This now uses mocked standard query
        core_query_response = query_response_data.get("response", "Simulated: Default AI response for query.")


        if is_flagged_prankster_in_db:
            response_to_user = f"Your behavior is consistently inappropriate for this service. This conversation is strictly limited to order-related queries. Any deviation will result in termination. (Simulated: Known prankster)."
            action_taken = "AI_ONLY_MODE_KNOWN_PRANKSTER"
            current_state["status"] = "ai_only_mode"
            flag_user_for_review_system = True
            logging.info(f"AI took over for known prankster '{user_id}'.")
        elif flag_potential_malice:
            response_to_user = f"Your current line of questioning appears to be off-topic and potentially suspicious. For security reasons, this conversation is now being escalated to a security specialist for review and may be terminated. (Simulated: {focus_status} - {focus_reason})."
            action_taken = "ESCALATE_TO_SECURITY_SPECIALIST_MALICE_DETECTED"
            escalate_to_human_system = True
            flag_user_for_review_system = True
            current_state["status"] = "ai_only_mode_security_alert"
            logging.critical(f"Immediate escalation for user '{user_id}' due to suspected malicious off-topic behavior.")
        elif current_turn_count == 2:
            if is_current_message_abuse:
                current_state["abuse_flagged_round"] = 2
                response_to_user = f"{core_query_response}\n\n*Note: We've noted your language. Please keep interactions respectful.*"
                action_taken = "QUERY_RESPONDED_ABUSE_DETECTED_FIRST_GRACE"
                logging.info(f"First abuse detected for user '{user_id}' (Turn 2), grace period applied.")
            else:
                response_to_user = core_query_response
                action_taken = "QUERY_RESPONDED_NORMAL"
                logging.info(f"Normal query for user '{user_id}' (Turn 2).")

        elif current_turn_count == 3:
            if is_current_message_abuse:
                current_state["abuse_flagged_round"] = 3
                response_to_user = f"{core_query_response}\n\n**Important Notice:** Your language is affecting the quality of our conversation and may impact our ability to efficiently process your inquiries. Please refrain from using abusive or inappropriate terms to ensure productive assistance."
                action_taken = "QUERY_RESPONDED_ABUSE_INFORMAL_NOTICE"
                current_state["status"] = "final_flag"
                flag_user_for_review_system = True
                logging.warning(f"Second abuse detected for user '{user_id}' (Turn 3), informal notice issued.")
            elif focus_status in ["off_topic_suspicious", "slightly_off_topic"]:
                 response_to_user = f"{core_query_response}\n\nJust a quick note, please try to keep our conversation focused on your orders or product queries so I can assist you best."
                 action_taken = "RESTEER_SLIGHTLY_OFF_TOPIC"
                 logging.info(f"User '{user_id}' off-topic (Turn 3). AI re-steering softly.")
            else:
                if current_state["abuse_flagged_round"] == 2:
                    response_to_user = f"{core_query_response}\n\nThank you for maintaining a productive conversation. How else can I assist?"
                    action_taken = "QUERY_RESPONDED_REDEEMED_BEHAVIOR"
                    current_state["abuse_flagged_round"] = 0
                    logging.info(f"User '{user_id}' redeemed behavior (Turn 3).")
                else:
                    response_to_user = core_query_response
                    action_taken = "QUERY_RESPONDED_NORMAL"
                    logging.info(f"Normal query for user '{user_id}' (Turn 3).")

        elif current_turn_count >= 4:
            if is_current_message_abuse:
                if is_valued_customer and (total_orders > 5 or recent_order_value > 50.0):
                    response_to_user = f"{core_query_response}\n\n**Reminder:** Please note that disrespectful communication does not expedite your request. We will continue to address your valid queries related to your orders, but non-relevant or abusive comments may be disregarded."
                    action_taken = "AI_ONLY_MODE_VALUED_ABUSE_FOCUSED"
                    current_state["status"] = "ai_only_mode"
                    escalate_to_human_system = True
                    logging.warning(f"Valued customer '{user_id}' continues abuse (Turn {current_turn_count}). AI focused on query.")
                else:
                    response_to_user = f"Your behavior is inappropriate. I can only assist with confirmed order details. Please provide a valid Order ID or the conversation will be terminated. (Simulated: {category})."
                    action_taken = "AI_ONLY_MODE_NON_VALUED_ABUSE_STRICT"
                    current_state["status"] = "ai_only_mode"
                    flag_user_for_review_system = True
                    logging.warning(f"Non-valued customer '{user_id}' continues abuse (Turn {current_turn_count}). AI strictly focused/cutting off.")

                    if not order_id and not re.search(r'\border(?:s)?\b|\bproduct(?:s)?\b|\bship(?:ing)?\b', message, re.IGNORECASE):
                         response_to_user += "\n\nThis conversation is now being terminated due to irrelevance and continued inappropriate behavior."
                         action_taken += "_TERMINATED"
                         logging.warning(f"Conversation terminated for non-valued user '{user_id}' due to continued abuse and irrelevance.")
            elif focus_status == "off_topic_suspicious":
                 response_to_user = f"Your query appears to be significantly off-topic from standard customer service. To ensure we can help you efficiently, please re-focus on your order or product related inquiry. (Simulated: {focus_status} - {focus_reason})"
                 action_taken = "RESTEER_OFF_TOPIC_SUSPICIOUS"
                 flag_user_for_review_system = True
                 logging.warning(f"User '{user_id}' off-topic and suspicious (Turn {current_turn_count}). AI re-steering.")
            elif focus_status == "slightly_off_topic":
                 response_to_user = f"{core_query_response}\n\nJust a quick note, please try to keep our conversation focused on your orders or product queries so I can assist you best."
                 action_taken = "RESTEER_SLIGHTLY_OFF_TOPIC"
                 logging.info(f"User '{user_id}' slightly off-topic (Turn {current_turn_count}). AI re-steering softly.")
            else:
                if current_state["abuse_flagged_round"] > 0:
                    response_to_user = f"{core_query_response}\n\nThank you for your cooperation and for keeping our conversation productive. How else can I assist you today?"
                    action_taken = "QUERY_RESPONDED_REDEEMED_BEHAVIOR_LONG_TERM"
                    current_state["status"] = "normal"
                    current_state["abuse_flagged_round"] = 0
                    logging.info(f"User '{user_id}' redeemed behavior after multiple turns (Turn {current_turn_count}).")
                else:
                    response_to_user = core_query_response
                    action_taken = "QUERY_RESPONDED_NORMAL"
                    logging.info(f"Normal query for user '{user_id}' (Turn {current_turn_count}).")
        else:
            response_to_user = core_query_response
            action_taken = "QUERY_RESPONDED_FALLBACK_NORMAL"
            logging.info(f"Fallback: Normal query for user '{user_id}' (Turn {current_turn_count}).")

        current_state["history"].append(f"AI: {response_to_user}")

        return {
            "response": response_to_user,
            "action": action_taken,
            "escalate_to_human_system": escalate_to_human_system,
            "flag_user_for_review_system": flag_user_for_review_system,
            "detection_category": category,
            "detection_severity": severity,
            "detection_reason": reason,
            "user_id": user_id,
            "current_turn_count": current_state["turn_count"],
            "conversation_status": current_state["status"],
            "total_abuse_count": current_state["abuse_count"],
            "consecutive_abuse": current_state["consecutive_abuse_count"] # Use consecutive_abuse_count
        }

# This is the actual agent instance that agent_engine_app.py will import as 'root_agent'
root_agent = MainRouterAgent(project_id=PROJECT_ID)