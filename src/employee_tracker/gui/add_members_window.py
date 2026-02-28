import tkinter as tk
from tkinter import messagebox, ttk

from employee_tracker.domain.tracker import Tracker
from employee_tracker.gui.style import centre_window

### AI DECLARATION - ChatGPT was used in the creation of GUI elements, given the creator's lack of experience in front-end

# This window is launched as a child of the department window. 
class AddMembersWindow(tk.Toplevel):
    def __init__(self,parent:tk.Tk,tracker:Tracker,dep_id:str,on_done=None):
        super().__init__(parent)
        self.tracker = tracker
        self.dep_id = dep_id
        self.on_done = on_done

        # Title and assertion that window should be a fixed size
        self.title("Add Department Members")
        self.resizable(False, False)

        # The below ensures that this window shows above the parent and grabs attention, whilst not being shown as a separate window in the taskbar
        self.transient(parent)
        self.grab_set()

        ### AI Declaration - implementation of ttk for homogenised styling was strongly aided by AI
        # Container for the window built with ttk
        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        # These were added to create stability, some windows were behaving in strange ways with extra width before these were added
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        container.columnconfigure(0, weight=1)

        ttk.Label(container, text="Add members", style="Title.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Sub frame for holding search entry
        search_frame = ttk.LabelFrame(container, text="Search", padding=10)
        search_frame.grid(row=1, column=0, sticky="ew")
        search_frame.columnconfigure(0, weight=1)

        # Search for employees
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=0, sticky="ew")
        # Employee list refreshes as the user is typing rather than on a button press -  this suggestion was made by an LLM
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_employee_list())

        # List frame showing employees, this was aided by ChatGPT
        list_frame = ttk.LabelFrame(container, text="Employees (Ctrl/Shift-click to multi-select)", padding=10)
        list_frame.grid(row=2, column=0, sticky="nsew", pady=(12, 0))
        list_frame.columnconfigure(0, weight=1)

        # Listbox within the frame
        self.emp_listbox = tk.Listbox(list_frame, width=55, height=14, selectmode=tk.EXTENDED, exportselection=False)
        self.emp_listbox.grid(row=0, column=0, sticky="nsew")

        self.emp_ids = []
        
        # Buttons for adding employees and closing window
        btns = ttk.Frame(container)
        btns.grid(row=3, column=0, sticky="ew", pady=(14, 0))
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        ttk.Button(btns, text="Add selected", style="Primary.TButton", command=self.on_add_selected).grid(row=0, column=0, sticky="ew")
        ttk.Button(btns, text="Close", command=self.destroy).grid(row=0, column=1, sticky="ew", padx=(10, 0))

        # Pressing Esc closes the window
        self.bind("<Escape>", lambda e: self.destroy())

        # Window is centered. Employee list refreshed on opening and focus on search box
        centre_window(self, 520, 520)
        self.refresh_employee_list()
        self.search_entry.focus_set()

    # refresh list of employees
    def refresh_employee_list(self):
        search = self.search_entry.get().strip().lower()

        # Ensuring correct department is set, and list employees already in department
        dep = self.tracker.departments[self.dep_id]
        current_members = set(dep.members or [])

        # delete temporary list of ids before new one created
        self.emp_listbox.delete(0, tk.END)
        self.emp_ids = []

        # Utilising the list method in tracker
        for emp in self.tracker.list_employees():
            # simplified search function (this would eventually be replaced by the more complex search function within list_employees)
            search_bucket = f"{emp.name} {emp.role}".lower()
            # skip employees that don't fix the pattern
            if search and search not in search_bucket:
                continue
            # don't show employees already in the department
            if emp.id in current_members:
                continue
            # add employees that pass into the results and present a selection of it's properties
            self.emp_ids.append(emp.id)
            self.emp_listbox.insert(tk.END, f"{emp.id} {emp.name} ({emp.role})")

    # method to be called on clicking Add
    def on_add_selected(self):
        selected = self.emp_listbox.curselection()
        # Error handling for no selection
        if not selected:
            messagebox.showerror("Add members", "Select at least one employee to add.")
            return
        
        # similar to in refresh employees
        dep = self.tracker.departments[self.dep_id]
        current_members = set(dep.members or [])

        added = 0
        errors = []

        for idx in selected:
            emp_id = self.emp_ids[idx]
            # This will already have been checked at this point, but to catch any edge cases, stop duplicate additions
            if emp_id in current_members:
                continue

            try:
                # Utilise tracker methods to add employees
                self.tracker.add_employee_to_department(self.dep_id,emp_id)
                added += 1
            except Exception as err:
                errors.append(f"{emp_id}: {err}")
            
        self.refresh_employee_list()
        
        # Flag to show parent window that adding is completed
        if self.on_done:
            self.on_done()
        
        if errors:
            messagebox.showerror("Some additions failed", "\n".join(errors))
        else:
            messagebox.showinfo("Added", f"Added {added} employees(s).")