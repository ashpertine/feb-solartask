from task_management import Task, ManageTask
import tkinter as tk
from tkinter import ttk
from datetime import datetime
task_manager = ManageTask()

COLORS = {
    'primary': '#6272a4',       # Purple-blue for primary actions
    'secondary': '#3fa963',     # Darker green for success/completion
    'background': '#282a36',    # Dark blue-gray for background
    'text': '#f8f8f2',          # Light gray/white for text
    'accent': '#e63946',        # Darker red for warnings/errors
    'light_accent': '#44475a',  # Medium dark gray for subtle backgrounds
    'dark_accent': '#bd93f9'    # Bright purple for contrast
}
#ModifyTask
class EditWindow(tk.Toplevel):
    def __init__(self, parent, current_title, current_due_date, current_priority):
        super().__init__(parent)
        self.parent = parent
        self.current_title = current_title
        self.current_due_date = current_due_date
        self.current_priority = current_priority
        self.title('Edit Task')
        self.geometry("450x150")
        self.minsize(450, 150)
        self.configure(bg=COLORS['background'])

        self.create_widgets()

    def reset_entries(self, event): #optional event
        if self.title_entry.get() == "Enter a title!":
            self.title_entry.delete(0, tk.END)
            self.title_entry.config(fg=COLORS['text'])
            
        if self.due_date_entry.get() in ("Enter a due date!", "Enter a valid due date!"):
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.config(fg=COLORS['text'])   
    
    def modify_task_request(self, title_entry, due_date_entry, priority_var, button):
        #focusing on non focusable widget
        button.focus()
        title = title_entry.get()
        due_date = due_date_entry.get()
        if len(title) == 0 and len(due_date) == 0:
            title_entry.insert(0, "Enter a title!")
            title_entry.config(fg=COLORS['accent'])
            due_date_entry.delete(0, tk.END)
            due_date_entry.insert(0, "Enter a due date!")
            due_date_entry.config(fg=COLORS['accent'])
            return
        elif len(title) == 0:
            title_entry.insert(0, "Enter a title!")
            title_entry.config(fg=COLORS['accent'])
            return
        elif len(due_date) == 0:
            due_date_entry.insert(0, "Enter a due date!")
            due_date_entry.config(fg=COLORS['accent'])
            return
        #priority
        match priority_var.get():
            case 0:
                priority = "High"
            case 1:
                priority = "Medium"
            case 2:
                priority = "Low"

        try:
            updated_task = Task(title=title, due_date=due_date, priority=priority)
            task_manager.modify_task(task_title=self.current_title, new_title=updated_task.title, new_due_date=updated_task.due_date, new_priority=updated_task.priority)

            add_task_to_list(self.parent.table, self.parent.completed_table)
            self.destroy()
        except ValueError:
            if len(due_date) > 0:
                due_date_entry.delete(0, tk.END)
                due_date_entry.insert(0, "Enter a valid due date!")
                due_date_entry.config(fg=COLORS['accent'])
                return


    def create_widgets(self):
        #New Task Title
        title_frame = tk.Frame(self, bg=COLORS['background'])
        title_label = tk.Label(title_frame, text='New Title: ', font=('', 13), width=14, anchor='e', 
                              bg=COLORS['background'], fg=COLORS['text'])
        self.title_entry = tk.Entry(title_frame, bg=COLORS['light_accent'], fg=COLORS['text'], 
                                   insertbackground=COLORS['text'])
        self.title_entry.insert(0, self.current_title)
        self.title_entry.bind("<FocusIn>", self.reset_entries)
        title_label.grid(row=0, column=0, padx=5)
        self.title_entry.grid(row=0, column=1, padx=5)
        title_frame.pack(anchor='center')

        #New Task Due Date
        due_date_frame = tk.Frame(self, bg=COLORS['background'])
        due_date_label = tk.Label(due_date_frame, text='New Due Date: ', font=('',13), width=14, anchor='e', 
                                 bg=COLORS['background'], fg=COLORS['text'])
        self.due_date_entry = tk.Entry(due_date_frame, bg=COLORS['light_accent'], fg=COLORS['text'], 
                                      insertbackground=COLORS['text'])
        self.due_date_entry.bind("<FocusIn>", self.reset_entries)
        self.due_date_entry.insert(0, self.current_due_date)
        due_date_label.grid(row=0, column=0, padx=5)
        self.due_date_entry.grid(row=0, column=1, padx=5)
        due_date_frame.pack(anchor='center')

        #New Task Priority
        priority_frame = tk.Frame(self, bg=COLORS['background'])
        priority_label = tk.Label(priority_frame, text="Priority: ", font=('',13), width=14, anchor='e', 
                                 bg=COLORS['background'], fg=COLORS['text'])
        self.priority_var = tk.IntVar()
        priority_list = ["High", "Medium", "Low"]
        priority_colors = [COLORS['accent'], COLORS['primary'], COLORS['secondary']]
        
        for i in range(len(priority_list)):
            radiobutton = tk.Radiobutton(priority_frame, text=priority_list[i],
                                       variable=self.priority_var,
                                       value=i,
                                       font=("", 13),
                                       indicatoron=False,
                                       bg=priority_colors[i],
                                       fg='white',
                                       selectcolor=priority_colors[i],
                                       activebackground=priority_colors[i],
                                       activeforeground='white')

            radiobutton.grid(row=0, column=[i+1])
        priority_label.grid(row=0, column=0, padx=5)
        priority_frame.pack(anchor='center', pady=5)

        buttons_frame = tk.Frame(self, bg=COLORS['background'])
        buttons_frame.pack(pady=5)

        modify_task_button = tk.Button(buttons_frame, 
                   text="Modify Task", 
                   command=lambda: self.modify_task_request(self.title_entry, self.due_date_entry, self.priority_var, modify_task_button),
                   bg=COLORS['primary'], 
                   fg='white',
                   activebackground=COLORS['dark_accent'], 
                   activeforeground="white",
                   anchor="center",
                   justify="center",
                   padx=10,
                   pady=5,
                   width=15,
                   relief=tk.FLAT,
                   wraplength=100)
        modify_task_button.pack(side='left', padx=5)
    

class App(tk.Tk):
    def __init__(self, size):
        #main setup
        super().__init__()
        self.title('Solartask')
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.configure(bg=COLORS['background'])

        #Task Input Frame
        self.task_input_frame = TaskInputFrame(self)
        self.task_input_frame.pack()
        self.mainloop()
    
class TaskInputFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['background'])
        #Program Title
        tk.Label(self, text="Solartask☀️", font=('', 22, 'bold'), bg=COLORS['background'], 
                fg=COLORS['primary']).pack(anchor='center', pady=20)
        self.place(x = 0, y = 0, relwidth = 0.3, relheight=0.1)
        self.create_task_widgets()
    def search_by_deadline_request(self):
        search_window = tk.Toplevel(self)
        search_window.title("Search by Due Date")
        search_window.geometry("800x500")
        search_window.minsize('800', '500')
        search_window.configure(bg=COLORS['background'])
        
        # Label and Entry for deadline
        label = tk.Label(search_window, text="Enter deadline (dd/mm/YYYY):",
                        font=('', 12), bg=COLORS['background'], fg=COLORS['text'])
        label.pack(pady=10)
        
        entry = tk.Entry(search_window, bg=COLORS['light_accent'],
                        fg=COLORS['text'], insertbackground=COLORS['text'], font=('', 12))
        entry.pack(pady=5)
        
        # Create a Treeview to show search results
        columns = ('title', 'due_date', 'priority')
        result_tree = ttk.Treeview(search_window, columns=columns, show='headings', height=10)
        result_tree.heading('title', text="Title")
        result_tree.heading('due_date', text="Due Date")
        result_tree.heading('priority', text="Priority")
        result_tree.column('title', width=250, anchor='center')
        result_tree.column('due_date', width=150, anchor='center')
        result_tree.column('priority', width=100, anchor='center')
        result_tree.pack(pady=5, fill='both', expand=True)
        
        def perform_search():
            search_date = entry.get()
            try:
                result_list = task_manager.bst.find_before_due_date(task_manager.bst.root, datetime.strptime(search_date, '%d/%m/%Y'))
                for item in result_tree.get_children():
                    result_tree.delete(item)
                if result_list:
                    for task in result_list:
                        result_tree.insert('', 'end', values=(task.title, task.due_date.strftime('%d/%m/%Y'), task.priority))
                else:
                    result_tree.insert('', 'end', values=("No tasks found", "", ""))
            except ValueError:
                for item in result_tree.get_children():
                    result_tree.delete(item)
                result_tree.insert('', 'end', values=("Enter a valid date format (dd/mm/YYYY)", "", ""))
        
        search_btn = tk.Button(search_window, text="Search", command=perform_search,
                            bg=COLORS['primary'], fg='white',
                            activebackground=COLORS['dark_accent'], activeforeground='white',
                            padx=10, pady=5)
        search_btn.pack(pady=10)
    def complete_task_request(self):
        complete_title_list = []
        for i in self.table.selection():
            item_data = self.table.item(i)
            task_title = item_data['values'][0]
            print(task_title)
            #data
            data = (item_data['values'][0], item_data['values'][1], item_data['values'][2])
            print(data)
            complete_title_list.append(task_title)
            self.table.delete(i)
            self.completed_table.insert('', 'end', values=data) 
        for i in complete_title_list:
            task_manager.complete_task(i)

    def reset_entries(self, event):#optional event
        if self.title_entry.get() == "Enter a title!":
            self.title_entry.delete(0, tk.END)
            self.title_entry.config(fg=COLORS['text'])
            
        if self.due_date_entry.get() in ("Enter a due date!", "Enter a valid due date!"):
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.config(fg=COLORS['text'])    

    def on_double_click(self, event):
        item_id = self.table.focus()
        if not item_id:
            return
        values = self.table.item(item_id, 'values')
        EditWindow(self, values[0], values[1], values[2]) 
    
    def undo_request(self):
        task_manager.undo()
        add_task_to_list(self.table, self.completed_table)
    
    def create_task_widgets(self):
        #Task Title
        title_frame = tk.Frame(self, bg=COLORS['background'])
        title_label = tk.Label(title_frame, text='Title: ', font=('', 13), width=10, anchor='e', 
                              bg=COLORS['background'], fg=COLORS['text'])
        self.title_entry = tk.Entry(title_frame, bg=COLORS['light_accent'], fg=COLORS['text'], 
                                   insertbackground=COLORS['text'])
        self.title_entry.bind("<FocusIn>", self.reset_entries)
        title_label.grid(row=0, column=0, padx=5)
        self.title_entry.grid(row=0, column=1, padx=5)
        title_frame.pack(anchor='center')

        #Task Due Date
        due_date_frame = tk.Frame(self, bg=COLORS['background'])
        due_date_label = tk.Label(due_date_frame, text='Due Date: ', font=('',13), width=10, anchor='e', 
                                 bg=COLORS['background'], fg=COLORS['text'])
        self.due_date_entry = tk.Entry(due_date_frame, bg=COLORS['light_accent'], fg=COLORS['text'], 
                                      insertbackground=COLORS['text'])
        self.due_date_entry.bind("<FocusIn>", self.reset_entries)
        due_date_label.grid(row=0, column=0, padx=5)
        self.due_date_entry.grid(row=0, column=1, padx=5)
        due_date_frame.pack(anchor='center')

        #Task Priority
        priority_frame = tk.Frame(self, bg=COLORS['background'])
        priority_label = tk.Label(priority_frame, text="Priority: ", font=('',13), width=10, anchor='e', 
                                 bg=COLORS['background'], fg=COLORS['text'])
        self.priority_var = tk.IntVar()
        priority_list = ["High", "Medium", "Low"]
        priority_colors = [COLORS['accent'], COLORS['primary'], COLORS['secondary']]
        
        for i in range(len(priority_list)):
            radiobutton = tk.Radiobutton(priority_frame, text=priority_list[i],
                                       variable=self.priority_var,
                                       value=i,
                                       font=("", 13),
                                       indicatoron=False,
                                       bg=priority_colors[i],
                                       fg='white',
                                       selectcolor=priority_colors[i],
                                       activebackground=priority_colors[i],
                                       activeforeground='white')

            radiobutton.grid(row=0, column=[i+1])
        priority_label.grid(row=0, column=0, padx=5)
        priority_frame.pack(anchor='center', pady=5)

        buttons_frame = tk.Frame(self, bg=COLORS['background'])
        buttons_frame.pack(pady=5, anchor='center')

        #style for buttons
        add_task_button = tk.Button(buttons_frame, 
                   text="Add Task", 
                   command=lambda: (add_task_request(self.title_entry, self.due_date_entry, self.priority_var, add_task_button), add_task_to_list(self.table, self.completed_table)),
                   bg=COLORS['primary'], 
                   fg='white',
                   activebackground=COLORS['dark_accent'], 
                   activeforeground="white",
                   anchor="center",
                   justify="center",
                   padx=10,
                   pady=5,
                   width=15,
                   relief=tk.FLAT,
                   wraplength=100)
        add_task_button.grid(row=0, column=0, padx=5)
        
        complete_task_button = tk.Button(buttons_frame, 
                   text="Complete Task", 
                   command=self.complete_task_request,
                   bg=COLORS['secondary'], 
                   fg='white',
                   activebackground=COLORS['dark_accent'], 
                   activeforeground="white",
                   anchor="center",
                   justify="center",
                   padx=10,
                   pady=5,
                   width=15,
                   relief=tk.FLAT,
                   wraplength=100)
        complete_task_button.grid(row=0, column=1, padx=5)

        undo_button = tk.Button(buttons_frame, 
                   text="Undo", 
                   command=self.undo_request,
                   bg=COLORS['accent'], 
                   fg='white',
                   activebackground=COLORS['dark_accent'], 
                   activeforeground="white",
                   anchor="center",
                   justify="center",
                   padx=10,
                   pady=5,
                   width=15,
                   relief=tk.FLAT,
                   wraplength=100)
        undo_button.grid(row=0, column=2, padx=5)

        #custom style for Treeview
        style = ttk.Style()
        style.configure("Treeview", 
                      background=COLORS['light_accent'],
                      foreground=COLORS['text'],
                      rowheight=25,
                      fieldbackground=COLORS['light_accent'])
        style.configure("Treeview.Heading", 
                      background=COLORS['primary'],
                      foreground="black",
                      relief="flat")
        style.map("Treeview.Heading",
                background=[('active', COLORS['dark_accent'])])
        style.map("Treeview",
                background=[('selected', COLORS['primary'])],
                foreground=[('selected', 'white')])

        #Task List
        table_frame = tk.Frame(self, bg=COLORS['background'])
        table_frame.pack(fill='x', pady=10)
        
        #available tasks
        available_frame = tk.Frame(table_frame, bg=COLORS['background'])
        available_frame.pack(side='left')
        table_label = tk.Label(available_frame, text='Available tasks 📖', font=('', 15, 'bold'), 
                              bg=COLORS['background'], fg=COLORS['dark_accent'])
        table_columns = ('title', 'due_date', 'priority')
        self.table = ttk.Treeview(available_frame, columns=table_columns, show='headings')
        for column in table_columns:
            self.table.heading(column, text=column.replace('_', ' ').title())
        self.table.column(column="title", width=150, anchor='center')
        self.table.column(column="due_date", width=100, anchor='center')
        self.table.column(column="priority", width=75, anchor='center')
        self.table.bind("<Double-1>", self.on_double_click)
        table_label.pack(anchor='center', pady=5)
        self.table.pack()

        #completed tasks
        completed_frame = tk.Frame(table_frame, bg=COLORS['background'])
        completed_frame.pack(side='right', padx=10)
        completed_table_label = tk.Label(completed_frame, text='Completed Tasks ✔️', font=('', 15, 'bold'), 
                                        bg=COLORS['background'], fg=COLORS['dark_accent'])
        self.completed_table = ttk.Treeview(completed_frame, columns=table_columns, show='headings')
        for column in table_columns:
            self.completed_table.heading(column, text=column.replace('_', ' ').title())
        self.completed_table.column(column="title", width=150, anchor='center')
        self.completed_table.column(column="due_date", width=100, anchor='center')
        self.completed_table.column(column="priority", width=75, anchor='center')
        completed_table_label.pack(anchor='center', pady=5)
        self.completed_table.pack()

        #event - delete
        def delete_items(_):
            delete_title_list = []
            for i in self.table.selection():
                item_data = self.table.item(i)
                task_title = item_data['values'][0]
                delete_title_list.append(task_title)
                self.table.delete(i)
            for i in delete_title_list:
                task_manager.delete_task(i)
        self.table.bind('<Delete>', delete_items)
        search_frame = tk.Frame(self, bg=COLORS['background'])
        search_frame.pack(pady=10)
        search_button = tk.Button(search_frame, text="Search by Deadline", 
                                  command=self.search_by_deadline_request,
                                  bg=COLORS['primary'], fg='white',
                                  activebackground=COLORS['dark_accent'], activeforeground='white',
                                  padx=10, pady=5)
        search_button.pack()


#Adding
def add_task_request(title_entry, due_date_entry, priority_var, button):
    #focusing on non focusable widget
    button.focus()
    title = title_entry.get()
    due_date = due_date_entry.get()
    if len(title) == 0 and len(due_date) == 0:
        title_entry.insert(0, "Enter a title!")
        title_entry.config(fg=COLORS['accent'])
        due_date_entry.delete(0, tk.END)
        due_date_entry.insert(0, "Enter a due date!")
        due_date_entry.config(fg=COLORS['accent'])
        return
    elif len(title) == 0:
        title_entry.insert(0, "Enter a title!")
        title_entry.config(fg=COLORS['accent'])
        return
    elif len(due_date) == 0:
        due_date_entry.insert(0, "Enter a due date!")
        due_date_entry.config(fg=COLORS['accent'])
        return

    #priority
    match priority_var.get():
        case 0:
            priority = "High"
        case 1:
            priority = "Medium"
        case _:
            priority = "Low"

    try:
        new_task = Task(title=title, due_date=due_date, priority=priority)
        print(f"Task Info\nTitle:{new_task.title}\nDue Date:{new_task.due_date}\nPriority:{new_task.priority}")
        task_manager.add_task(new_task)
    except ValueError:
        #check if format matches date
        if len(due_date) > 0:
            due_date_entry.delete(0, tk.END)
            due_date_entry.insert(0, "Enter a valid due date!")
            due_date_entry.config(fg=COLORS['accent'])
            return
            
def add_task_to_list(table, completed_table):
    for item in table.get_children():
        table.delete(item)  
    
    for item in completed_table.get_children():
        completed_table.delete(item)

    task_list = task_manager.get_task()
    completed_task_history = task_manager.completed_task_history.get_history()
    try:
        if task_list: #check if task list exists
            for i in range(0, len(task_list)):
                data = (task_list[i].title, datetime.strftime(task_list[i].due_date, '%d/%m/%Y'), task_list[i].priority)
                table.insert('', 'end', values=data)
        if completed_task_history:
            for i in range(0, len(completed_task_history)):
                data = (completed_task_history[i].title, datetime.strftime(completed_task_history[i].due_date, '%d/%m/%Y'), completed_task_history[i].priority)
                completed_table.insert('', 'end', values=data)
    except TypeError:
        return


if __name__ == "__main__":
    app = App(['900', '600'])