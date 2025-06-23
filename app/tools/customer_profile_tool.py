# filter-flow-ai/app/tools/customer_profile_tool.py
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CustomerProfileTool:
    def __init__(self):
        # Mock customer data: {user_id: {is_valued: bool, total_orders: int, recent_order_value: float, is_flagged_prankster: bool}}
        self.customer_data = {
            "user_abc": {"is_valued": True, "total_orders": 15, "recent_order_value": 250.00, "is_flagged_prankster": False},
            "user_xyz": {"is_valued": False, "total_orders": 1, "recent_order_value": 15.00, "is_flagged_prankster": False},
            "user_prk": {"is_valued": False, "total_orders": 0, "recent_order_value": 0.00, "is_flagged_prankster": True}, # Flagged prankster
            "user_new": {"is_valued": False, "total_orders": 0, "recent_order_value": 0.00, "is_flagged_prankster": False}, # Truly new customer
            "default_playground_user": {"is_valued": False, "total_orders": 0, "recent_order_value": 0.00, "is_flagged_prankster": False} # Default user
        }
        logging.info("CustomerProfileTool initialized with mock data.")

    def get_customer_profile(self, user_id: str) -> dict:
        """
        Retrieves a mock customer profile.
        In a real scenario, this would query a database.
        """
        profile = self.customer_data.get(user_id, self.customer_data["default_playground_user"]) # Default to 'default_playground_user' if ID not found
        logging.info(f"Retrieved profile for user '{user_id}': {profile}")
        return profile

    def get_order_details(self, order_id: str) -> dict:
        """
        Retrieves mock order details.
        In a real scenario, this would query an order database.
        """
        # Mock order data: {order_id: {user_id: str, value: float, confirmed: bool}}
        mock_orders = {
            "ORDER12345": {"user_id": "user_abc", "value": 250.00, "confirmed": True},
            "ORDER98765": {"user_id": "user_xyz", "value": 15.00, "confirmed": True},
            "ORDER00000": {"user_id": "user_prk", "value": 5.00, "confirmed": False}, # Example of unconfirmed/fake order
        }
        order_info = mock_orders.get(order_id, {"value": 0.0, "confirmed": False})
        logging.info(f"Retrieved order details for order '{order_id}': {order_info}")
        return order_info