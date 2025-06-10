import matplotlib.pyplot as plt

def show_gantt(log):
    fig,ax = plt.subplots(figsize=(10, 3))
    y_labels = []
    y_ticks = []
    
    color_map={}
    current_y = 10
    
    for pid,start, duration in log:
        y_labels.append(f"P{pid}")
        y_ticks.append(current_y)
        color = color_map.get(pid,f"C{pid%10}")
        
        ax.broken_barh([(start, duration)], (current_y - 2, 4), facecolors=color)
        current_y += 10
        ax.set_ylim(5, current_y)
        
    ax.set_xlim(0, max(start + duration for _, start, duration in log) + 1)
    ax.set_xlabel("Time")
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.set_title("Gantt Chart")
    plt.tight_layout()
    plt.show()
        
        