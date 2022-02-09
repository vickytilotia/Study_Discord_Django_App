class Item:
    pay_rate =  0.8
    def __init__(self,name: str,price: float,qty =0):
        #run validations on the recieved parameters
#         assert price >=0
#         assert qty >=0, f"Here we can write the exception error"
        
        #Assign to self objects
        self.name = name
        self.price = price
        self.qty = qty
        
    def calcultate_total_price(self):
        return self.price * self.qty
    
    
item1 = Item("phone", 1000, 4)
item2 = Item("laptop", 3000, 2)
item2 = Item("laptop", 3000, "string")
item2 = Item("laptop", "3000", 2)

