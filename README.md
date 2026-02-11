Sales Transactions Analytics API
*Project Overview
    this project is a sales Transactions Analytics API that goes through many stages
    to deliver validated , clean and analyzed sales data to the client.

*project stages :- 
    stage(1):
    'the client side'
        represents the requests from the client which in our project are :
            - health check
            - send raw data                      
            - clean orders  
            - get summary   

    stage(2):
    'the server side'
        represents the part of the system that receives requests from the client, handles them, and
        redirects them to 'the logic side' which processes the requests , and finally returns the response back to the client.

        Endpoints (representing requests) in our project:

        GET  /                  --> Health Check: to check whether the server is working or not.

        POST /orders            --> Send Raw Data:to send raw data to the server to handle it ( storing  it for now )
                                    and later validating & processing it according to what required.  

        POST /process_orders    --> Clean Orders: to validate & process the raw data coming from the client 
                                    so it can be ready for use later in analysis.

        GET  /analytics_summary --> Get Summary: to generate a full analysis serving the project from the processed data  


    stage(3):
    'the logic side'
        represents the part of the system that receives requests from the server, validates, and
        processes them and sends the final response to 'the server side'

        logic methods:
        main methods (related to server):
            store_orders    --> recieves raw orders from the server and stors it in the "data/raw_data" file. 

            process_orders  --> process raw orders following these steps:
                                1. ( load_raw_orders )   --> loading raw orders stored in the "data/raw_data" file. 
                                2. ( validate_order  )   --> check orders and ignores the invalid ones 
                                3. ( validate_item   )   --> check items and ignores the invalid ones
                                4. ( merge_items     )   --> merge duplicate items in each order 
                                5. store the cleaned orders in processed_orders for analysis or server response.

            analyze_orders  --> generates a full analysis following these steps:
                                1. calculate total revenue , average order value , number of unique customers , 
                                   total number of orders. 
                                2. returns available product categories and payment methods used.
                                3. puts all this data in final summary and storing it in data/sales_summary" file. 
 

        helper methods ( used inside the main methods )
            validate_order  --> cheacks that ( order_id , customer_id , order_date , items , payment_method)
                                exists & its type is as specified . if not the order is ignored

            validate_item   --> 1. cheacks that ( product_id ,category , price , quantity ) 
                                   exists & its type is as specified , if not the order is ignored
                                2. checks that quantity &  price are > 0   , if not the order is ignored 

            merge_items     -->    at the same order if 2 products or more have the same product_id,
                                   then merge them in 1 order  
            load_raw_orders -->    load raw orders from "data/raw_data.json" file 


        Note :
        According to the project requirements, validation & cleaning rules were only for items ( price, quantity, and category).
        for example product_id is not mentioned , but i handled it so that i can use it safely in the method merge items.
        the method merge items itself is also not required but i added it just for practice.
        the same holds for the proccess of handling repeated orders which i also added for practice.



*Container choices :-
    1. list 
        it is used here because there may exists duplicates (as data still not cleaned) and also the order matters
        in dealing with sales as orders need to be processed with the order they arrived.
        - raw_orders 
        - processed_order 
        - items 
        - valid items
        - merged item 
        

    2. set 
        it is used here because duplicates are not allowed.
        -processed_orders_ids
        -unique_customers
        -available_product_categories
        -payment_methods_used

    3. dict 
        it is used here because we need to represent key value elements 
        -item (in items) 
        -summary
        -merged_items --> as my goal here is to combine items with the same product_id in the same oreder and 
                          sum their quantities, using product_id to be the key  (just during the method to reach our goal)
                          then its a list 


*Error handling strategy :-
    in the Logic lier , we first try to handle errors inside the methods , but to make in considiration the unexpected errors
    we use try-except to avoid the program from stoping suddenly.  
     
*OOP design :- 
    1.separation of responsibilities:
        we achieved this by creating 3 separate classes (client , server, processor ) each has its separate duty
    2.reusability:
        as each class is separate from the other, we can use them in other seperate projects which saves time.
        its also good in testing so that recognizing errors will be easier.
    3.encapsulation:
        as all attributes and methods in the class processor are only visible there 
        note that i didint set the methods to be private in my project, but technically the client 
        can not access them directly because it has no instance of SalesProcessor.
