# Sales Transactions Analytics API

##  Project Overview
This project is a **Sales Transactions Analytics API** that goes through many stages to deliver validated, clean and analyzed sales data to the client.

---

##  Project Stages

### **Stage (1): The Client Side**
Represents the requests from the client which in our project are:
* Health check
* Send raw data
* Clean orders
* Get summary

### **Stage (2): The Server Side**
Represents the part of the system that receives requests from the client, handles them, and redirects them to **'the logic side'** which processes the requests, and finally returns the response back to the client.

#### **Endpoints (Representing Requests):**

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/` | **Health Check:** To check whether the server is working or not. |
| **POST** | `/orders` | **Send Raw Data:** To send raw data to the server to handle it (storing it for now) and later validating & processing it. |
| **POST** | `/process_orders` | **Clean Orders:** To validate & process the raw data coming from the client so it can be ready for use later in analysis. |
| **GET** | `/analytics_summary` | **Get Summary:** To generate a full analysis serving the project from the processed data. |

### **Stage (3): The Logic Side**
Represents the part of the system that receives requests from the server, validates, and processes them and sends the final response to **'the server side'**.

#### **Logic Methods:**

**1. Main Methods (Related to Server):**
* **`store_orders`**: Recieves raw orders from the server and stors it in the `"data/raw_data"` file.
* **`process_orders`**: Process raw orders following these steps:
    1. `load_raw_orders`: Loading raw orders stored in the `"data/raw_data"` file.
    2. `validate_order`: Check orders and ignores the invalid ones.
    3. `validate_item`: Check items and ignores the invalid ones.
    4. `merge_items`: Merge duplicate items in each order.
    5. Store the cleaned orders in `processed_orders` for analysis or server response.
* **`analyze_orders`**: Generates a full analysis following these steps:
    1. Calculate total revenue, average order value, number of unique customers, total number of orders.
    2. Returns available product categories and payment methods used.
    3. Puts all this data in final summary and storing it in `"data/sales_summary"` file.

**2. Helper Methods (Used inside the main methods):**
* **`validate_order`**: Checks that (`order_id`, `customer_id`, `order_date`, `items`, `payment_method`) exists & its type is as specified. If not, the order is ignored.
* **`validate_item`**: 
    1. Checks that (`product_id`, `category`, `price`, `quantity`) exists & its type is as specified. If not, the order is ignored.
    2. Checks that `quantity` & `price` are `> 0`. If not, the order is ignored.
* **`merge_items`**: At the same order if 2 products or more have the same `product_id`, then merge them in 1 order.
* **`load_raw_orders`**: Load raw orders from `"data/raw_data.json"` file.

> **Note:** According to the project requirements, validation & cleaning rules were only for items (price, quantity, and category). For example, `product_id` is not mentioned, but I handled it so that I can use it safely in the method `merge_items`. The method `merge_items` itself is also not required but I added it just for practice. The same holds for the process of handling repeated orders which I also added for practice.

---

##  Container Choices

1.  **List**: It is used here because there may exists duplicates (as data still not cleaned) and also the order matters in dealing with sales as orders need to be processed with the order they arrived.
    * `raw_orders`, `processed_order`, `items`, `valid items`, `merged item`.
2.  **Set**: It is used here because duplicates are not allowed.
    * `processed_orders_ids`, `unique_customers`, `available_product_categories`, `payment_methods_used`.
3.  **Dict**: It is used here because we need to represent key value elements.
    * `item` (in items), `summary`.
    * `merged_items`: As my goal here is to combine items with the same `product_id` in the same order and sum their quantities, using `product_id` to be the key (just during the method to reach our goal) then it's a list.

---

##  Technical Implementation

### **Error Handling Strategy**
In the Logic layer, we first try to handle errors inside the methods, but to make in consideration the unexpected errors we use **try-except** to avoid the program from stopping suddenly.

### **OOP Design**
1.  **Separation of Responsibilities**: We achieved this by creating 3 separate classes (`client`, `server`, `processor`) each has its separate duty.
2.  **Reusability**: As each class is separate from the other, we can use them in other separate projects which saves time. It's also good in testing so that recognizing errors will be easier.
3.  **Encapsulation**: As all attributes and methods in the class processor are only visible there. 
    * *Note:* I didn't set the methods to be private in my project, but technically the client cannot access them directly because it has no instance of `SalesProcessor`.

    
