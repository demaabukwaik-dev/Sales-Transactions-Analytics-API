from fastapi import FastAPI
from processor import SalesProcessor
from processor import Orders


class Server:
    def __init__(self , sales_processor: SalesProcessor):
        self.app = FastAPI()
        self.sales_processor = sales_processor   
        self._setup_routes()

    def _setup_routes(self):
        
        @self.app.get("/")
        def health_check():
            return {"message": "server is running "}


        @self.app.post("/orders")
        def receive_raw_orders(orders :  Orders):
            return self.sales_processor.store_orders(orders)
            

        @self.app.post("/process_orders")
        def process_raw_orders():
            return self.sales_processor.process_orders() 
                   

        @self.app.get("/analytics_summary")
        def get_analytics_summary():
            return self.sales_processor.analyze_orders()
            


processor_instance = SalesProcessor()
server_instance = Server(processor_instance)
app = server_instance.app