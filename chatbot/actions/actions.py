# ManVue Fashion Chatbot Custom Actions
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json

# Configuration for ManVue API
MANVUE_API_BASE = "http://localhost:5000"

class ActionSearchProducts(Action):
    def name(self) -> Text:
        return "action_search_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get entities from user message
        product_type = tracker.get_slot("product_type")
        color = tracker.get_slot("color")
        size = tracker.get_slot("size")
        price_range = tracker.get_slot("price_range")
        
        # Build search query
        search_params = {}
        if product_type:
            search_params["category"] = product_type
        if color:
            search_params["color"] = color
        if size:
            search_params["size"] = size
        
        try:
            # Call ManVue API
            response = requests.get(f"{MANVUE_API_BASE}/products", params=search_params, timeout=5)
            
            if response.status_code == 200:
                products = response.json()
                
                if products:
                    # Format response for user
                    if len(products) == 1:
                        product = products[0]
                        message = f"🛍️ I found this great product:\n\n**{product['title']}**\n💰 ${product['price']}\n📦 Category: {product.get('category', 'N/A')}\n\nWould you like more details or see similar items?"
                    else:
                        message = f"🛍️ I found {len(products)} products matching your search:\n\n"
                        for i, product in enumerate(products[:3]):  # Show top 3
                            message += f"{i+1}. **{product['title']}** - ${product['price']}\n"
                        
                        if len(products) > 3:
                            message += f"\n...and {len(products) - 3} more! Would you like to see them all?"
                else:
                    message = "😔 I couldn't find any products matching your criteria. Try searching for:\n• T-shirts\n• Shirts\n• Jackets\n• Bottoms\n• Accessories"
            else:
                message = "🔧 Sorry, I'm having trouble accessing our product catalog right now. Please try again in a moment."
                
        except requests.RequestException:
            message = "🔧 I'm currently unable to search our products. You can browse our catalog directly on the website!"
        
        dispatcher.utter_message(text=message)
        return []

class ActionGetProductRecommendations(Action):
    def name(self) -> Text:
        return "action_get_product_recommendations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Get featured/recommended products
            response = requests.get(f"{MANVUE_API_BASE}/products", timeout=5)
            
            if response.status_code == 200:
                products = response.json()
                
                # Get trending/popular items (simulate with first few products)
                recommendations = products[:4] if products else []
                
                if recommendations:
                    message = "🌟 **Today's Trending Picks:**\n\n"
                    for product in recommendations:
                        message += f"• **{product['title']}** - ${product['price']}\n"
                    message += "\n✨ These styles are popular with our customers! Want to see more details?"
                else:
                    message = "🎯 Check out our featured collections:\n• Winter Essentials\n• Casual Comfort\n• Office Ready\n• Weekend Vibes"
            else:
                message = "🎯 I recommend browsing our popular categories: T-Shirts, Shirts, Jackets, and Accessories!"
                
        except requests.RequestException:
            message = "🎯 Here are some popular categories to explore:\n• Classic T-Shirts\n• Formal Shirts\n• Stylish Jackets\n• Comfortable Bottoms\n• Fashion Accessories"
        
        dispatcher.utter_message(text=message)
        return []

class ActionGetSizeRecommendation(Action):
    def name(self) -> Text:
        return "action_get_size_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        product_type = tracker.get_slot("product_type")
        
        size_guide = {
            "shirts": "👔 **Shirt Sizing:**\n• S: 38-40\" chest\n• M: 40-42\" chest\n• L: 42-44\" chest\n• XL: 44-46\" chest",
            "t-shirts": "👕 **T-Shirt Sizing:**\n• S: 36-38\" chest\n• M: 38-40\" chest\n• L: 40-42\" chest\n• XL: 42-44\" chest",
            "jackets": "🧥 **Jacket Sizing:**\n• S: 38-40\" chest\n• M: 40-42\" chest\n• L: 42-44\" chest\n• XL: 44-46\" chest",
            "bottoms": "👖 **Bottom Sizing:**\n• 30: 30\" waist\n• 32: 32\" waist\n• 34: 34\" waist\n• 36: 36\" waist"
        }
        
        if product_type and product_type.lower() in size_guide:
            message = size_guide[product_type.lower()]
        else:
            message = "📏 **General Size Guide:**\n• XS: 32-34\" chest\n• S: 34-36\" chest\n• M: 36-38\" chest\n• L: 38-40\" chest\n• XL: 40-42\" chest\n• XXL: 42-44\" chest\n\n💡 Tip: When in doubt, size up for a comfortable fit!"
        
        dispatcher.utter_message(text=message)
        return []

class ActionTrackOrder(Action):
    def name(self) -> Text:
        return "action_track_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = "📦 **Order Tracking:**\n\nTo track your order, I'll need your order number. You can find it in:\n• Your confirmation email\n• Your ManVue account\n• Order receipt\n\n📧 Don't have your order number? Contact our support team at support@manvue.com and we'll help you out!\n\n⏰ Orders typically ship within 1-2 business days."
        
        dispatcher.utter_message(text=message)
        return []

class ActionGetStoreLocations(Action):
    def name(self) -> Text:
        return "action_get_store_locations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = "🏪 **ManVue Store Locations:**\n\n🌟 **Flagship Stores:**\n• New York - 5th Avenue\n• Los Angeles - Beverly Hills\n• Chicago - Magnificent Mile\n• Miami - Brickell City Centre\n\n🛒 **Online Store:**\nShop 24/7 at manvue.com with free shipping on orders over $75!\n\n📍 Looking for a specific location? Use our store locator on the website or call 1-800-MANVUE."
        
        dispatcher.utter_message(text=message)
        return []

class ActionSubscribeNewsletter(Action):
    def name(self) -> Text:
        return "action_subscribe_newsletter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_email = tracker.get_slot("user_email")
        
        if user_email:
            message = f"📧 Perfect! I've added {user_email} to our VIP newsletter.\n\n🎁 **Welcome Benefits:**\n• 15% off your next purchase\n• Early access to sales\n• Style tips & trends\n• Exclusive member deals\n\nCheck your inbox for a welcome email with your discount code!"
        else:
            message = "📧 **Join ManVue VIP Newsletter!**\n\n🎁 **Get:**\n• 15% welcome discount\n• Early sale access\n• Style guides\n• Exclusive offers\n\nSign up on our website or tell me your email address to subscribe!"
        
        dispatcher.utter_message(text=message)
        return []

class ActionCheckAvailability(Action):
    def name(self) -> Text:
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        product_type = tracker.get_slot("product_type")
        size = tracker.get_slot("size")
        color = tracker.get_slot("color")
        
        message = "📦 **Stock Status:**\n\nTo check availability for specific items, I'll need:\n• Product name or ID\n• Size preference\n• Color choice\n\n✅ Most of our popular items are in stock and ready to ship!\n\n🔔 Want notifications when something comes back? Sign up for restock alerts on the product page."
        
        dispatcher.utter_message(text=message)
        return []

class ActionGetCareInstructions(Action):
    def name(self) -> Text:
        return "action_get_care_instructions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        product_type = tracker.get_slot("product_type")
        
        care_instructions = {
            "shirts": "👔 **Shirt Care:**\n• Machine wash cold\n• Use gentle cycle\n• Hang dry or low heat\n• Iron on medium heat\n• Dry clean for best results",
            "t-shirts": "👕 **T-Shirt Care:**\n• Machine wash cold\n• Turn inside out\n• Tumble dry low\n• Avoid bleach\n• Iron inside out if needed",
            "jackets": "🧥 **Jacket Care:**\n• Check care label\n• Dry clean recommended\n• Spot clean when possible\n• Store on hangers\n• Professional cleaning for best results",
            "jeans": "👖 **Denim Care:**\n• Wash inside out in cold water\n• Wash every 4-5 wears\n• Air dry when possible\n• Avoid over-washing\n• Iron inside out if needed"
        }
        
        if product_type and product_type.lower() in care_instructions:
            message = care_instructions[product_type.lower()]
        else:
            message = "🧺 **General Care Tips:**\n• Always check care labels\n• Wash in cold water\n• Turn dark colors inside out\n• Air dry when possible\n• Iron on appropriate heat settings\n\n💡 Pro tip: Proper care extends garment life and maintains quality!"
        
        dispatcher.utter_message(text=message)
        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = "🤔 I didn't quite understand that. I can help you with:\n\n🛍️ **Shopping:**\n• Product search\n• Size guides\n• Recommendations\n\n📦 **Orders:**\n• Shipping info\n• Return policy\n• Order tracking\n\n💡 **Support:**\n• Contact info\n• Store locations\n• Care instructions\n\nWhat would you like to know more about?"
        
        dispatcher.utter_message(text=message)
        return []

