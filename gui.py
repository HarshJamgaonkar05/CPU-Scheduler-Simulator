import tkinter as tk
from tkinter import ttk, messagebox
from process import Process
from gantt import show_gantt
from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.srtf import srtf
from algorithms.priority import priority_scheduling
from algorithms.round_robin import round_robin
import random
import copy

# ---------- THEME SETUP ----------
def apply_dark_theme():
    style = ttk.Style()
    style.theme_use("default")
    style.configure(".", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e")
    style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 10))
    style.configure("TButton", background="#2d2d2d", foreground="white", padding=6, font=("Segoe UI", 10))
    style.configure("TCombobox", fieldbackground="#2d2d2d", background="#2d2d2d", foreground="white")
    style.configure("Treeview", background="#2d2d2d", fieldbackground="#2d2d2d",
                    foreground="white", rowheight=25, font=("Segoe UI", 10))
    style.configure("Treeview.Heading", background="#3a3a3a", foreground="white", font=("Segoe UI", 10, "bold"))
    style.map("TButton", background=[("active", "#3a3a3a")])
    style.map("TCombobox", fieldbackground=[("readonly", "#2d2d2d")])

# ---------- DATA GENERATION ----------
def generate_processes(count=5):
    processes = []
    for i in range(count):
        pid = i + 1
        arrival = random.randint(0, 10)
        burst = max(1, int(random.gauss(5, 2)))
        priority = random.randint(1, 5)
        processes.append(Process(pid, arrival, burst, priority))
    return processes

# ---------- DISPLAY TABLE ----------
def display_results(processes):
    for row in result_tree.get_children():
        result_tree.delete(row)

    total_waiting = 0
    total_turnaround = 0

    for p in processes:
        result_tree.insert("", "end", values=(
            p.pid, p.arrival_time, p.burst_time, p.priority,
            p.start_time, p.completion_time, p.waiting_time, p.turnaround_time
        ))
        total_waiting += p.waiting_time
        total_turnaround += p.turnaround_time

    avg_wait = total_waiting / len(processes)
    avg_turn = total_turnaround / len(processes)

    avg_label.config(text=f"Avg Waiting Time: {avg_wait:.2f}   |   Avg Turnaround Time: {avg_turn:.2f}")


# ---------- SIMULATOR LOGIC ----------
def run_scheduler(count):
    algorithm = algo_var.get()
    if not algorithm:
        messagebox.showerror("Error", "Please select a scheduling algorithm")
        return

    plist = generate_processes(count)
    original = copy.deepcopy(plist)

    # Show generated processes
    for row in proc_tree.get_children():
        proc_tree.delete(row)
    for p in original:
        proc_tree.insert("", "end", values=(p.pid, p.arrival_time, p.burst_time, p.priority))

    if algorithm == "FCFS":
        scheduled, log = fcfs(plist)
    elif algorithm == "SJF":
        scheduled, log = sjf(plist)
    elif algorithm == "SRTF":
        scheduled, log = srtf(plist)
    elif algorithm == "Priority":
        scheduled, log = priority_scheduling(plist)
    elif algorithm == "Round Robin":
        tq = quantum_var.get()
        scheduled, log = round_robin(plist, time_quantum=tq)
    elif algorithm == "Compare All":
        all_results = []

        algos = [
            ("FCFS", fcfs),
            ("SJF", sjf),
            ("SRTF", srtf),
            ("Priority", priority_scheduling),
            ("Round Robin", lambda p: round_robin(p, time_quantum=quantum_var.get()))
        ]

        for name, func in algos:
            cloned = copy.deepcopy(original)
            scheduled, _ = func(cloned)
            avg_wait = sum(p.waiting_time for p in scheduled) / len(scheduled)
            avg_turn = sum(p.turnaround_time for p in scheduled) / len(scheduled)
            all_results.append((name, avg_wait, avg_turn))

        compare_window = tk.Toplevel(root)
        compare_window.title("Algorithm Comparison")
        compare_window.configure(bg="#1e1e1e")

        tk.Label(compare_window, text="Algorithm Comparison", font=("Segoe UI", 14, "bold"),
                bg="#1e1e1e", fg="white").pack(pady=10)

        table = ttk.Treeview(compare_window, columns=("Algorithm", "Avg Waiting", "Avg Turnaround"), show="headings")
        for col in ("Algorithm", "Avg Waiting", "Avg Turnaround"):
            table.heading(col, text=col)
            table.column(col, width=150, anchor=tk.CENTER)
        table.pack(padx=20, pady=10, fill="x")

        for name, awt, att in all_results:
            table.insert("", "end", values=(name, f"{awt:.2f}", f"{att:.2f}"))

    else:
        messagebox.showerror("Error", "Unsupported algorithm selected")
        return

    display_results(scheduled)
    show_gantt(log)

# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("1024x650")
root.configure(bg="#1e1e1e")
apply_dark_theme()

# ---------- HEADER SECTION ----------
header = tk.Label(root, text="CPU Scheduling Simulator", font=("Segoe UI", 16, "bold"), bg="#1e1e1e", fg="white")
header.pack(pady=15)

top_frame = tk.Frame(root, bg="#1e1e1e")
top_frame.pack(pady=5)

algo_var = tk.StringVar()
tk.Label(top_frame, text="Algorithm:", font=("Segoe UI", 10), bg="#1e1e1e", fg="white").grid(row=0, column=0, padx=5)
algo_menu = ttk.Combobox(top_frame, textvariable=algo_var, state="readonly",
                         values=["FCFS", "SJF", "SRTF", "Priority", "Round Robin", "Compare All"], width=15)
algo_menu.grid(row=0, column=1, padx=5)

tk.Label(top_frame, text="Processes:", font=("Segoe UI", 10), bg="#1e1e1e", fg="white").grid(row=0, column=2, padx=5)
process_count_var = tk.IntVar(value=5)
tk.Spinbox(top_frame, from_=1, to=20, textvariable=process_count_var, width=5).grid(row=0, column=3, padx=5)

quantum_frame = tk.Frame(root, bg="#1e1e1e")
quantum_label = tk.Label(quantum_frame, text="Time Quantum:", font=("Segoe UI", 10), bg="#1e1e1e", fg="white")
quantum_var = tk.IntVar(value=2)
quantum_spin = tk.Spinbox(quantum_frame, from_=1, to=10, textvariable=quantum_var, width=5)
quantum_frame.pack_forget()

def on_algorithm_change(event):
    if algo_var.get() == "Round Robin":
        quantum_frame.pack(pady=5)
        quantum_label.pack(side=tk.LEFT)
        quantum_spin.pack(side=tk.LEFT)
    else:
        quantum_frame.pack_forget()

algo_menu.bind("<<ComboboxSelected>>", on_algorithm_change)

tk.Button(top_frame, text="Run Simulation", command=lambda: run_scheduler(process_count_var.get())).grid(row=0, column=4, padx=10)

# ---------- GENERATED PROCESSES ----------
tk.Label(root, text="Generated Processes:", font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="white").pack(pady=(10, 0))
proc_tree = ttk.Treeview(root, columns=("PID", "Arrival", "Burst", "Priority"), show="headings")
for col in ("PID", "Arrival", "Burst", "Priority"):
    proc_tree.heading(col, text=col)
    proc_tree.column(col, width=100, anchor=tk.CENTER)
proc_tree.pack(pady=5, fill="x", padx=20)

# ---------- SCHEDULING RESULTS ----------
tk.Label(root, text="Scheduling Results:", font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="white").pack(pady=(10, 0))
result_columns = ("PID", "Arrival", "Burst", "Priority", "Start", "Completion", "Waiting", "Turnaround")
result_tree = ttk.Treeview(root, columns=result_columns, show="headings")
for col in result_columns:
    result_tree.heading(col, text=col)
    result_tree.column(col, width=100, anchor=tk.CENTER)
result_tree.pack(pady=5, fill="x", padx=20)

# Average time display
avg_label = tk.Label(root, text="", font=("Segoe UI", 11, "bold"), bg="#1e1e1e", fg="white")
avg_label.pack(pady=(5, 10))


# ---------- RUN APP ----------
root.mainloop()
