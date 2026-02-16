
filepath = "todolist.txt"

def add_values(todos):
    with open (filepath,"w") as file :
        file.writelines(todos)

def read_todos():
    with open (filepath,"r") as file :
        todolist = file.readlines()
        return todolist