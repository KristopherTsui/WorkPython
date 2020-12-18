import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.createWidgets()
        self.pack()

    def createWidgets(self):
        self.createTree()
        self.tree.grid(row=0)
        self.frame = tk.Frame(self)
        self.createFrameLabels(self.frame)
        self.createFrameEntrys(self.frame)
        self.createFrameButtons(self.frame)
        self.frame.grid(row=1)

    def createTree(self):
        self.tree = tk.ttk.Treeview(self, column=('c1', 'c2', 'c3', 'c4'), show="headings")
        headings_list = ["Process", "Max", "Allocation", "Need"]
        for i in range(1, 5):
            self.tree.column(f"c{i}", width=75, anchor="center")
            self.tree.heading(f"c{i}", text=headings_list[i-1])

    def createFrameLabels(self, master=None):
        label_total = tk.Label(master, text="资源总数:")
        label_thread = tk.Label(master, text="进程:")
        label_max = tk.Label(master, text="最大需求资源:")
        label_allo = tk.Label(master, text="已分配资源:")
        label_need = tk.Label(master, text="需要资源:")
        label_request = tk.Label(master, text="请求:")
        label_available = tk.Label(master, text="Available:")
        label_sequence = tk.Label(master, text="Security Sequence:")
        label_list = ['total', 'thread', 'max', 'allo', 'need', 'request', 'available', 'sequence']
        for i in range(8):
            eval(f"label_{label_list[i]}").grid(row=i, column=0)
        self.label_output1 = tk.Label(master, text="")
        self.label_output1.grid(row=6, column=1)
        self.label_output2 = tk.Label(master, text="")
        self.label_output2.grid(row=7, column=1)

    def createFrameEntrys(self, master=None):
        self.entry_obj_total = tk.Entry(master)
        self.entry_obj_thread = tk.Entry(master)
        self.entry_obj_max = tk.Entry(master)
        self.entry_obj_allo = tk.Entry(master)
        self.entry_obj_need = tk.Entry(master)
        self.entry_obj_req = tk.Entry(master)
        entry_list = ['total', 'thread', 'max', 'allo', 'need', 'req']
        for i in range(6):
            eval(f"self.entry_obj_{entry_list[i]}").grid(row=i, column=1)
    
    def createFrameButtons(self, master=None):
        button_initialize = tk.Button(master, text="初始化", width=6, command=self.button_initialize_click_handler)
        button_initialize.grid(row=0, column=2)
        button_enter = tk.Button(master, text="确定", width=6, command=self.button_enter_click_handler)
        button_enter.grid(row=2, column=2)
        self.button_delete = tk.Button(master, text="删除", width=6, command=self.button_delete_click_handler)
        self.button_delete.config(state=tk.DISABLED)
        self.button_delete.grid(row=3, column=2)
        self.button_clear = tk.Button(master, text="清空", width=6, command=self.button_clear_click_handler)
        self.button_clear.config(state=tk.DISABLED)
        self.button_clear.grid(row=4, column=2)
        button_security = tk.Button(master, text="安全性", width=6, command=self.button_security_click_handler)
        button_security.grid(row=6, column=2)
        button_start = tk.Button(master, text="Start", width=6, command=self.button_start_click_handler)
        button_start.grid(row=5, column=2)
        button_exit = tk.Button(master, text="Exit", width=6, command=self.quit)
        button_exit.grid(row=7, column=2)

    def button_initialize_click_handler(self):
        string = self.entry_obj_total.get()
        if string == "":
            error = tk.messagebox.showwarning(title="Warning!", message="资源总数不能为空!")
            print(error)
        elif self.tree.get_children() == ():
            error = tk.messagebox.showwarning(title="Warning!", message="请输入线程信息!")
            print(error)
        else:
            available = np.array(string.split(), dtype=int)
            self.get_data()
            max_source, allocation = self.get_data()
            self.bank = BankerAlgorithm(available, max_source, allocation)
            self.label_output1['text'] = self.bank.available
        
    def button_enter_click_handler(self):
        string1 = self.entry_obj_thread.get()
        string2 = self.entry_obj_max.get()
        string3 = self.entry_obj_allo.get()
        string4 = self.entry_obj_need.get()
        entry_list = ['thread', 'max', 'allo', 'need']
        for item in entry_list:
            eval(f"self.entry_obj_{item}.delete(0, tk.END)")
        if string1 == "" or string2 == "" or (string3 == "" and string4 == ""):
            print(tk.messagebox.showwarning(title="Warning!", message="输入条件不足，请重新输入!"))
        elif string3 != "" and string4 == "":
            self.tree_insert(string1, string2, string3, 1)
            self.button_state_changed()
        elif string3 == "" and string4 != "":
            self.tree_insert(string1, string2, string4, 2)
            self.button_state_changed()
        else:
            max_source = np.array(string2.split(), dtype=int)
            allo_source = np.array(string3.split(), dtype=int)
            need_source = np.array(string4.split(), dtype=int)
            if (max_source == allo_source + need_source).all():
                self.tree_insert(string1, string2, string3, 1)
            else:
                print(tk.messagebox.showwarning(title="Warning!", message="已分配资源与需求资源不符!请重新输入!"))

    def button_delete_click_handler(self):
        self.tree.delete(self.tree.selection())
        if self.tree.get_children() == ():
            self.button_delete.config(state=tk.DISABLED)
            self.button_clear.config(state=tk.DISABLED)

    def button_clear_click_handler(self):
        item_list = self.tree.get_children()
        for item in item_list:
            self.tree.delete(item)
        self.button_delete.config(state=tk.DISABLED)
        self.button_clear.config(state=tk.DISABLED)

    def button_security_click_handler(self):
        if self.label_output1['text'] == "":
            error = tk.ttk.showerror(title="Error!", message="未进行初始化!")
            print(error)
            pass
        else:
            flag = self.bank.security(self.bank.available.copy())
            if not flag:
                error = tk.ttk.showwarning(title="Warning!", message="不安全!不能分配!")
                print(error)
                self.bank.security_sequence = ""
            self.label_output2['text'] = self.bank.security_sequence[:-2]

    def button_start_click_handler(self):
        string = self.entry_obj_req.get()
        self.entry_obj_req.delete(0, tk.END)
        if self.label_output1['text'] == "":
            error = tk.messagebox.showerror(title="Error!", message="未进行初始化!")
            print(error)
        elif string == "":
            error = tk.messagebox.showerror(title="Error!", message="请求不能为空!")
            print(error)
        else:
            idx, req = string.split(',')
            idx = int(idx[1:])
            req = np.array(req.split(), dtype=int)
            self.bank.run(idx, req, window=self)
            self.label_output1['text'] = self.bank.available
            self.label_output2['text'] = self.bank.security_sequence[:-2]

    def get_data(self):
        item_list = self.tree.get_children()
        item_tags = {}
        for item in item_list:
            idx = self.tree.item(item)['tags'][0]
            item_tags[idx] = item
        item_tags = dict(sorted(item_tags.items(), key=lambda d:d[0]))
        item = item_tags.pop(0)
        max_source = np.array([self.tree.item(item)['values'][1].split()], dtype=int)
        allocation = np.array([self.tree.item(item)['values'][2].split()], dtype=int)
        for key, value in item_tags.items():
            a = np.array([self.tree.item(value)['values'][1].split()], dtype=int)
            b = np.array([self.tree.item(value)['values'][2].split()], dtype=int)
            max_source = np.insert(max_source, key, a, axis=0)
            allocation = np.insert(allocation, key, b, axis=0)
        return max_source, allocation

    def tree_insert(self, string1, string2, string3, flag):
        idx = int(string1)
        max_source = list(map(int, string2.split()))
        source1 = list(map(int, string3.split()))
        source2 = list(np.array(max_source) - np.array(source1))
        if flag == 1:
            self.tree.insert("", index=idx, values=(f"P{idx}", max_source, source1, source2), tags=idx)
        else:
            self.tree.insert("", index=idx, values=(f"P{idx}", max_source, source2, source1), tags=idx)

    def button_state_changed(self):
        if self.button_delete['state'] == tk.DISABLED:
            self.button_delete.config(state=tk.NORMAL)
            self.button_clear.config(state=tk.NORMAL)


class BankerAlgorithm():
    def __init__(self, available, max_source, allocation):
        self.available = available
        self.max_source = max_source
        self.allocation = allocation
        self.need = max_source - allocation
        self.security_sequence = ""
        for item in self.allocation:
            self.available -= item

    def security(self, work):
        """ Security algorithm.
        """
        self.security_sequence = ""
        n = self.need.shape[0]
        finish = np.array([False] * n, dtype=bool)
        while not finish.all():
            flag = False
            for i in range(n):
                if not finish[i] and (self.need[i] <= work).all():
                    self.security_sequence += f"P{i}->"
                    flag = True
                    work += self.allocation[i]
                    finish[i] = True
                    break
            if not flag:
                return False
        return True

    def run(self, idx, req, window):
        if (req > self.need[idx]).any():
            error = tk.messagebox.showerror(title="Error!", message="请求错误!请重新输入!")
            print(error)
        elif (req > self.available).any():
            error = tk.messagebox.showerror(title="Error!", message="资源不足!无法分配!")
            print(error)
        else:
            self.available -= req
            self.allocation[idx] += req
            self.need[idx] -= req
            flag = self.security(self.available.copy())
            if not flag:
                error = tk.messagebox.showerror(title="Error!", message="不安全!不能分配!")
                print(error)
                self.available += req
                self.allocation[idx] -= req
                self.need[idx] += req
                self.security_sequence = ""
            item = window.tree.get_children()[idx]
            window.tree.item(item, values=(f"P{idx}", list(self.max_source[idx]),
                        list(self.allocation[idx]), list(self.need[idx])))


def main():
    window = tk.Tk()
    window.title("银行家算法演示")
    window.resizable(width=False, height=False)
    app = Application(master=window)
    app.mainloop()


if __name__ == '__main__':
    main()
