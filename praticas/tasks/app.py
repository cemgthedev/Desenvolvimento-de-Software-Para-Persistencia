import uuid

class Task:
    def __init__(self, id_task, title, description, date):
        self.id = id_task
        self.title = title
        self.description = description
        self.date = date

def add_task(task):
    with open('tasks.txt', 'a') as file:
        file.write(f'{task.id};{task.title};{task.description};{task.date}\n')
    print("Adicionado com sucesso!")

def list_tasks():
    with open('tasks.txt', 'r') as file:
        print(file.read())
    
def remove_task(id):
    with open('tasks.txt', 'r') as file:
        lines = file.readlines()
    with open('tasks.txt', 'w') as file:
        for line in lines:
            if line.split(';')[0] != id:
                file.write(line)
    
def update_task(id):
    with open('tasks.txt', 'r') as file:
        lines = file.readlines()
    with open('tasks.txt', 'w') as file:
        for line in lines:
            if line.split(';')[0] == id:
                id_task = str(uuid.uuid4())
                title = input('Digite o novo título da tarefa: ')
                description = input('Digite a nova descrição da tarefa: ')
                date = input('Digite a nova data da tarefa: ')
                file.write(f'{id_task};{title};{description};{date}\n')
            else:
                file.write(line)
    
while(True):
    opcao = input('1 - Adicionar tarefa\n2 - Listar tarefas\n3 - Remover tarefa\n4 - Atualizar tarefa\n5 - Sair\nSelecione uma opção: ')
    if opcao == '1':
        title = input('Digite o título da tarefa: ')
        description = input('Digite a descrição da tarefa: ')
        date = input('Digite a data da tarefa: ')
        task = Task(id, title, description, date)
        add_task(task)
    elif opcao == '2':
        list_tasks()
    elif opcao == '3':
        id = input('Digite o ID da tarefa que deseja remover: ')
        remove_task(id)
    elif opcao == '4':
        id = input('Digite o ID da tarefa que deseja atualizar: ')
        update_task(id)
    elif opcao == '5':
        break