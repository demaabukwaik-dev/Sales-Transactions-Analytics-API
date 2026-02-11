import json
from pydantic import BaseModel
from typing import List, Any , Optional 

class Item(BaseModel):
    product_id: Optional[Any] = None
    category: Optional[Any] = None
    price: Optional[Any] = None
    quantity: Optional[Any] = None

class Order(BaseModel):
    order_id: Optional[Any] = None
    customer_id: Optional[Any] = None
    order_date: Optional[Any] = None
    items: Optional[List[Item]] = None
    payment_method: Optional[Any] = None

class Orders(BaseModel):
    orders: List[Order] = None 


class SalesProcessor:
    def __init__(self):
        self.raw_orders : list[dict] = []  # list of dicts
        self.processed_orders : list[dict] = []  
        

    def store_orders(self, orders : Orders):
        try:
            for order in orders.orders:
                order_dict = order.dict()
                self.raw_orders.append(order_dict)
        
            with open("data/raw_sales.json", "w") as f:
                json.dump(self.raw_orders, f, indent=4)
            return {"status": "stored"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    def validate_order(self, order: dict) :
            try:
                order_id = order.get("order_id")
                if not order_id or not isinstance(order_id, str) :
                    return False

                customer_id = order.get("customer_id")
                if not customer_id or not isinstance(customer_id, str):
                    return False

                order_date = order.get("order_date")
                if not order_date or not isinstance(order_date, str):
                    return False

                items = order.get("items")
                if not items or not isinstance(items, list) :
                    return False

                payment_method = order.get("payment_method")
                if not payment_method or not isinstance(payment_method, str):
                    return False

                return True

            except Exception:
                return False

    def validate_item ( self , item : dict ) :
        try:

            product_id = item.get("product_id")
            if product_id is None or not isinstance(product_id, str):
                return False

            category = item.get("category")
            if category is None or not isinstance(category, str):
                return False

            price = item.get("price")
            if price is None or not isinstance(price, (int, float)) or price <= 0:
                return False

            quantity = item.get("quantity")
            if quantity is None or not isinstance(quantity, int) or quantity <= 0 :
                return False

            return True
        
        except Exception:
            return False

    def merge_items(self, items: List[dict]) : # [ {procudt_id : 1 , quantity : 2} , {procudt_id : 1 , quantity : 3} ]
        merged_items = {} # dict { product_id : {product_id : 1 , quantity : 5} ,  product_id : {product_id : 2 , quantity : 10}}
        for item in items:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 0)
            
            if product_id in merged_items: 
                merged_items[product_id]["quantity"] += quantity
            else:
                merged_items[product_id] = item.copy()

        return list(merged_items.values()) 
    
    def load_raw_orders(self):
        try:
            with open("data/raw_sales.json", "r") as f:
                self.raw_orders = json.load(f)
        except FileNotFoundError:
            self.raw_orders = []

    def process_orders(self):
        self.processed_orders = []
        processed_orders_ids = set()
        self.load_raw_orders()
        
        for order in self.raw_orders:
            order_id = order.get("order_id")
            if order_id in processed_orders_ids:
                continue

            if not self.validate_order(order):
                continue

            order_items = order.get("items", [])
            valid_items = []
            for item in order_items:
                if self.validate_item(item):
                    valid_items.append(item)
            
            merged_items = self.merge_items(valid_items)

            if merged_items:
                clean_order = order.copy()
                clean_order["items"] = merged_items
                self.processed_orders.append(clean_order)
                processed_orders_ids.add(order_id)

        return self.processed_orders
    
                                
    def analyze_orders(self):
        try:
            total_revenue = 0.0
            average_order_value = 0.0
            available_product_categories = set()
            payment_methods_used = set()
            unique_customers = set()
        
            for order in self.processed_orders:
                items = order.get("items", [])  
                order_revenue = 0.0
                customer_id = order.get("customer_id", "Unknown")
                if not customer_id in unique_customers:
                    unique_customers.add(customer_id)


                for item in items:
                    price = item.get("price", 0.0)
                    quantity = item.get("quantity", 0)
                    order_revenue += price * quantity
                
                    category = item.get("category", "Unknown")
                    available_product_categories.add(category)
                    payment_method = order.get("payment_method", "Unknown")
                    payment_methods_used.add(payment_method)
                    
                total_revenue += order_revenue
            average_order_value = total_revenue / len(self.processed_orders) if self.processed_orders else 0.0


            summary = {
                "total_number_of_orders": len(self.processed_orders), 
                "number_of_unique_customers": len(unique_customers),
                "total_revenue": total_revenue,
                "average_order_value": average_order_value,
                "available_product_categories": list(available_product_categories),
                "payment_methods_used": list(payment_methods_used),
            }

            with open("data/sales_summary.json", "w") as f:
                json.dump(summary, f, indent=4)
            return summary
        
        except Exception as e:
            return {"status": "error", "message": str(e)}           





        

