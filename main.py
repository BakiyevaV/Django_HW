import os
import sys
import subprocess

class Venv:
    def __init__(self, name):
        self.name = name
        print("Виртуальное окружение")

    def create(self):
        os.system(f'python -m venv {self.name}')
        return True

    def activate(self):
        subprocess.run(f'{self.name}\\Scripts\\activate', shell=True)
        print("активировано")

class PackInstallator:
    def __init__(self, version = None):
        self.version = version
        print("Установщик")

    def pack_install(self):
        if self.version == None:
            os.system(f'pip install django')
        else:
            os.system(f'pip install django=={self.version}')
            print('устанавливаю с версией')

    def freeze(self):
        print("freeze")
        os.system('pip freeze > requirements.txt')


class ProjectCreator:
    def __init__(self, name):
        self.name = name
        print("Создание проекта")

    def create_project(self):
        os.system(f'django-admin startproject {self.name} .')


class AppCreator:
    def __init__(self, name):
        self.name = name
        print("Создание приложения")

    def create_app(self):
        os.system(f'python manage.py startapp {self.name}')


if __name__ == "__main__":
     args = sys.argv
     length = len(args)
     if length < 4:
         print("""Введите обязательные аргументы в следующем порядке: 
               python <имя файла> <Наименование виртульного окружения> <версия django (не обязательно> <Наименование проекта> <Наименование приложения>""")
     elif length == 4:
         venv = Venv(args[1])
         venv.create()
         venv.activate()

         ins = PackInstallator()
         ins.pack_install()
         ins.freeze()

         project = ProjectCreator(args[2])
         project.create_project()

         app = AppCreator(args[3])
         app.create_app()

     elif length == 5:
         venv = Venv(args[1])
         venv.create()
         venv.activate()

         if args[2][0].isdigit():

             try:
                 with open('versions.txt',encoding='UTF-8') as file:
                     versions = file.read()
                     file.close()
                 versions_list = versions.split(", ")
                 if args[2] in versions_list:
                     ins = PackInstallator(args[2])
                     ins.pack_install()
                     ins.freeze()
             except FileNotFoundError:
                 ins = PackInstallator()
                 ins.pack_install()
                 ins.freeze()
         else:
             ins = PackInstallator()
             ins.pack_install()
             ins.freeze()

         project = ProjectCreator(args[3])
         project.create_project()

         app = AppCreator(args[4])
         app.create_app()













