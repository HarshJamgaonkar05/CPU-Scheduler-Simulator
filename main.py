# import tkinter as tk
# import matplotlib.pyplot as plt
# import random
# from process import Process
# from algorithms.fcfs import fcfs
# from algorithms.sjf import sjf
# from algorithms.srtf import srtf
# from algorithms.priority import priority_scheduling
# from algorithms.round_robin import round_robin


# def gen_pro(count = 5):
#     processes = []
#     for i in range(count):
#         pid = i + 1
#         arrival_time = random.randint(0,10)
#         burst_time = max(1, int(random.gauss(5,2)))
#         priority = random.randint(1,5)
#         processes.append(Process(pid, arrival_time, burst_time, priority))
#     return processes

# def display_results(processes):
#     print("PID\tArrival\tBurst\tStart\tCompletion\tWaiting\tTurnaround")
#     for p in processes:
#         print(f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t{p.start_time}\t{p.completion_time}\t\t{p.waiting_time}\t{p.turnaround_time}")
    
    
# if __name__ == "__main__":
#     plist = gen_pro(5)
#     print("\nGenerated Processes:")
#     for p in plist:
#         print(p)
    
#     sch_fcfs = fcfs(plist)
#     print('\nFCFS Scheduling Results:')
#     display_results(sch_fcfs)

    
#     sch_sjf = sjf(plist)
#     print('\nSJF Scheduling Results:')
#     display_results(sch_sjf)
    
#     # sch_srtf = srtf(plist)  
#     # print('\nSRTF Scheduling Results:')
#     # display_results(sch_srtf)   
    
#     sch_p = priority_scheduling(plist)
#     print('\nPriority Scheduling Results:')
#     display_results(sch_p)
    
#     sch_rr = round_robin(plist)
#     print('\nRound Robin Scheduling Results:')
#     display_results(sch_rr)