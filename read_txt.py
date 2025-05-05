import os
current_dir = os.path.dirname(os.path.abspath(__file__))
with open(current_dir+"/confidencial_information.txt", "r") as file:
    lines = file.readlines()
    print(lines[0])