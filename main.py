import os

class Student:
    def __init__(self, name, email, course, registration_num):
        self.name = name
        self.email = email
        self.course = course
        self.registration_num = registration_num


class StudentManager:
    def __init__(self):
        self.students = {}
        self.course_counters = {}
        self.finished = False

    def generate_registration_num(self, course):
        self.course_counters[course] = self.course_counters.get(course, 0) + 1
        return f"{course}{self.course_counters[course]}"

    def create_student(self):
        name = input("Nome: ")
        email = input("Email: ")
        course = input("Curso: ")

        reg = self.generate_registration_num(course)
        student = Student(name, email, course, reg)

        if course not in self.students:
            self.students[course] = []
        self.students[course].append(student)

        print("Aluno criado:", reg)

    def edit_student(self):
        reg = input("Matrícula: ")
        for students in self.students.values():
            for s in students:
                if s.registration_num == reg:
                    s.name = input("Novo nome: ")
                    s.email = input("Novo email: ")
                    print("Aluno atualizado")
                    return

        print("Aluno não encontrado")

    def remove_student(self):
        reg = input("Matrícula: ")

        for course in self.students:
            for s in self.students[course]:
                if s.registration_num == reg:
                    self.students[course].remove(s)
                    print("Aluno removido")
                    return

        print("Aluno não encontrado")

    def list_students(self):
        for course, students in self.students.items():
            print(f"\nCurso: {course}")
            for s in students:
                print(s.registration_num, s.name, s.email)

    def perform_action(self, choice):
        if choice == "1":
            self.create_student()
        elif choice == "2":
            self.edit_student()
        elif choice == "3":
            self.remove_student()
        elif choice == "4":
            self.list_students()
        elif choice == "5":
            self.finished = True

    def get_choice(self):
        print("\n== CRUD de alunos ==")
        print("(1) Criar aluno")
        print("(2) Editar aluno")
        print("(3) Remover aluno")
        print("(4) Listar alunos")
        print("(5) Sair")

        return input("Escolha: ")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    manager = StudentManager()
    while not manager.finished:
        choice = manager.get_choice()
        manager.perform_action(choice)
        input("Pressione qualquer tecla para continuar")
        clear_screen()


if __name__ == "__main__":
    main()
