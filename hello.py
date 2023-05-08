while True:
    user_input = int(input("pls enter the values for iteration:"))
    if user_input>0:
        for i in range(user_input):
            print(i)
        continue
    else:
        print("exit")
        break
