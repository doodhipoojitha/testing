class RedBus:
    redbus_discount = 5
    def __init__(self,source,destination,price,bus_dis):
        self.source = source
        self.destination = destination
        self.price = price
        self.bus_dis = bus_dis

    def final_price(self):    #normal obj use method
        return self.price - self.price*self.bus_dis/100 - self.price*self.redbus_discount/100

    def string_rep(self):       #normal obj use method
        print("-----------")
        print("source: ",self.source)
        print("destination: ",self.destination)
        print("final price: ",self.final_price())

    @staticmethod     #Just like normal func inside a class, it won't use class/obj variable, we can call with class name & objects
    def max_num(num1,num2):
        print(max(num1,num2))

    @classmethod       #The function that uses class variable(redbus_discount), we can call only using class name
    def change_app_dis(cls,discount):
        cls.redbus_discount = discount


s1 = RedBus("Tirupathi","Bangalore",500,4)
s2 = RedBus("Tirupathi","Hyderabad",600,5)
print("___________Before____________")
s1.string_rep()
s2.string_rep()
RedBus.change_app_dis(10)
print("___________After_______________")
s1.string_rep()
s2.string_rep()
RedBus.max_num(6,2)
s1.max_num(0,2)
s2.max_num(1.2,0.2)



# while True:
#     user_input = int(input("please enter the values for iteration:"))
#     if user_input>0:
#         for i in range(user_input):
#             print(i)
#         continue
#     else:
#         print("exit")
#         break
