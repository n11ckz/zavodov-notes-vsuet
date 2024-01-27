from tkinter import *
from tkinter import ttk, messagebox
import json

def OpenNoteWindow(login):
    def AddNote():
        def SaveNote():
            title = titleEntry.get()
            content = contentEntry.get("1.0", END)

            notes[title] = content.strip()
            with open(f"{login.lower()}.json", "w") as file:
                json.dump(notes, file, indent=3)

            noteContent = Text(notebook, width=40, height=10)
            noteContent.insert(END, content)
            notebook.forget(notebook.select())
            notebook.add(noteContent, text=title)

        noteFrame = ttk.Frame(notebook, padding=10)
        notebook.add(noteFrame, text="Новая заметка")

        titleLabel = Label(noteFrame, text="Название:")
        titleLabel.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        titleEntry = Entry(noteFrame, width=40)
        titleEntry.grid(row=0, column=1, padx=10, pady=10)

        contentLabel = Label(noteFrame, text="Содержание:")
        contentLabel.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        contentEntry = Text(noteFrame, width=40, height=10)
        contentEntry.grid(row=1, column=1, padx=10, pady=10)

        saveButton = Button(noteFrame, text="Сохранить", command=SaveNote)
        saveButton.grid(row=2, column=1, padx=10, pady=10)

    def LoadNotes():
        try:
            with open(f"{login.lower()}.json", "r") as file:
                notes = json.load(file)
            for title, content in notes.items():
                noteContent = Text(notebook, width=40, height=10)
                noteContent.insert(END, content)
                notebook.add(noteContent, text=title)
        except FileNotFoundError:
            pass

    def DeleteNote():
        currentTab = notebook.index(notebook.select())
        noteTitle = notebook.tab(currentTab, "text")
        confirm = messagebox.askyesno("Удалить заметку", f"Вы действительно хотите удалить заметку '{noteTitle}'?")

        if not confirm:
            return None

        notebook.forget(currentTab)
        notes.pop(noteTitle)

        with open(f"{login.lower()}.json", "w") as file:
                json.dump(notes, file)

    noteWindow = Tk()
    noteWindow.title(f"Заметки пользователя {login}")
    noteWindow.geometry("500x500")

    notebook = ttk.Notebook(noteWindow)
    notebook.pack(padx=10, pady=10, fill=BOTH, expand=True)

    notes = {}
    try:
        with open(f"{login.lower()}.json", "r") as file:
            notes = json.load(file)
    except FileNotFoundError:
        pass

    LoadNotes()

    newButton = Button(noteWindow, text="Новая заметка", command=AddNote)
    newButton.pack(side=LEFT, padx=10, pady=10)

    deleteButton = ttk.Button(noteWindow, text="Удалить", command=DeleteNote)
    deleteButton.pack(side=LEFT, padx=10, pady=10)

def isEntryEmpty(loginEntry, passwordEntry):
    if loginEntry.get() == "" or passwordEntry.get() == "":
        return True
    return False

def OpenLoginWindow():
    def Login():
        if isEntryEmpty(loginEntry, passwordEntry):
            errorLabel["text"] = "Ошибка\nНеверный логин или пароль"
            return None

        password = users.get(loginEntry.get().lower())
        if password is None or password != passwordEntry.get():
            errorLabel["text"] = "Ошибка\nНеверный логин или пароль"
            return None
        OpenNoteWindow(loginEntry.get())
        loginScreen.destroy()

    loginScreen = Tk()
    loginScreen.geometry("300x235")
    loginScreen.title("Авторизация")

    Label(loginScreen, text="Авторизация", font=("Arial", 15)).pack(pady=10)

    Label(loginScreen, text="Логин").pack()
    loginEntry = Entry(loginScreen)
    loginEntry.pack()

    Label(loginScreen, text="Пароль").pack()
    passwordEntry = Entry(loginScreen)
    passwordEntry.pack()

    loginButton = Button(loginScreen, text="Войти", command=Login)
    loginButton.pack(pady=5)

    errorLabel = Label(loginScreen, text="", height=2)
    errorLabel.pack()

    registerButton = Button(loginScreen, text="Нет аккаунта? Зарегистрироваться", command=OpenRegisterScreen)
    registerButton.pack(pady=5)

def OpenRegisterScreen():
    def RegisterUser():
        users[loginEntry.get().lower()] = passwordEntry.get()
        with open("users.json", "w+") as file:
            json.dump(users, file, indent=3)

    def Register():
        if isEntryEmpty(loginEntry, passwordEntry):
            reportLabel["text"] = "Ошибка\nПопробуйте еще раз"
            return None

        if users.get(loginEntry.get().lower()) is not None:
            reportLabel["text"] = "Такой пользователь уже зарегистрирован"
            return None

        RegisterUser()
        loginButton["state"] = loginEntry["state"] = passwordEntry["state"] = "disabled"
        reportLabel["text"] = "Вы успешно зарегистрировались"

    registerScreen = Toplevel()
    registerScreen.grab_set()
    registerScreen.geometry("275x205")
    registerScreen.title("Регистарция")

    Label(registerScreen, text="Регистарция", font=("Arial", 15)).pack(pady=10)

    Label(registerScreen, text="Логин").pack()
    loginEntry = Entry(registerScreen)
    loginEntry.pack()

    Label(registerScreen, text="Пароль").pack()
    passwordEntry = Entry(registerScreen)
    passwordEntry.pack()

    loginButton = Button(registerScreen, text="Зарегистрироваться", command=Register)
    loginButton.pack(pady=5)

    reportLabel = Label(registerScreen, text="")
    reportLabel.pack()

users = {}
try:
    with open("users.json", "r") as file:
        users = json.load(file)
except FileNotFoundError:
    pass

OpenLoginWindow()

mainloop()