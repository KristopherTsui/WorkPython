import threading
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import time


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.entry_obj_val = tk.StringVar()
        self.check_box_var = tk.IntVar()
        self.createWidgets()
        self.pack()

    def createWidgets(self):
        self.createFrame1()
        self.createFrame2()
        self.frame1.grid(row=0)
        self.frame2.grid(row=0, column=1)

    def createFrame1(self):
        self.frame1 = tk.Frame(self)
        self.list_box_input = tk.Listbox(self.frame1, width=25, height=15)
        self.list_box_input.grid(row=0, columnspan=3)
        label_input = tk.Label(self.frame1, text="输入:")
        label_input.grid(row=1, column=0)
        self.entry_obj = tk.Entry(self.frame1)
        self.entry_obj.grid(row=1, column=1, columnspan=2)
        button_input = tk.Button(self.frame1, text="输入", command=self.button_input_click_handler)
        button_input['height'] = 2
        button_input.grid(row=2, column=0)
        self.button_delete = tk.Button(self.frame1, text="删除", command=self.button_delete_click_handler)
        self.button_delete['height'] = 2 
        self.button_delete.config(state=tk.DISABLED)
        self.button_delete.grid(row=2, column=1, padx=30)
        self.button_clear = tk.Button(self.frame1, text="清空", command=self.button_clear_click_handler)
        self.button_clear['height'] = 2
        self.button_clear.config(state=tk.DISABLED)
        self.button_clear.grid(row=2, column=2)

    def createFrame2(self):
        self.frame2 = tk.Frame(self)
        self.list_box_output = tk.Listbox(self.frame2, width=35, height=15)
        self.list_box_output.grid(row=0, columnspan=3)
        label_path = tk.Label(self.frame2, text="目标路径:")
        label_path.grid(row=1, column=0)
        self.entry_obj_path = tk.Entry(self.frame2, textvariable=self.entry_obj_val)
        self.entry_obj_path.grid(row=1, column=1)
        button_select = tk.Button(self.frame2, text="选择文件", command=self.button_select_click_handler)
        button_select.grid(row=1, column=2)
        button_start = tk.Button(self.frame2, text="开始", command=self.button_start_click_handler)
        button_start['height'] = 2
        button_start.grid(row=2, column=0)
        button_exit = tk.Button(self.frame2, text="退出", command=self.quit)
        button_exit['height'] = 2
        button_exit.grid(row=2, column=1)
        self.createFrame3(master=self.frame2)
        self.frame3.grid(row=2, column=2)

    def createFrame3(self, master):
        self.frame3 = tk.Frame(master)
        check_box1 = tk.Radiobutton(self.frame3, text="文件输入", value=1,
                                    variable=self.check_box_var)
        check_box1.grid(row=0)
        check_box2 = tk.Radiobutton(self.frame3, text="手动输入", value=2,
                                    variable=self.check_box_var)
        check_box2.grid(row=1)

    def button_input_click_handler(self):
        input_str = self.entry_obj.get()
        if input_str == '':
            error = tk.messagebox.showerror(title="Error!", message="输入不能为空!")
            print(error)
        else:
            self.list_box_input.insert(tk.END, input_str)
            self.entry_obj.delete(0, tk.END)
            if self.button_delete['state'] == tk.DISABLED:
                self.button_delete.config(state=tk.NORMAL)
                self.button_clear.config(state=tk.NORMAL)

    def button_delete_click_handler(self):
        self.list_box_input.delete(tk.ACTIVE)
        if self.list_box_input.size() == 0:
            self.button_delete.config(state=tk.DISABLED)
            self.button_clear.config(state=tk.DISABLED)

    def button_clear_click_handler(self):
        self.list_box_input.delete(0, tk.END)
        self.button_delete.config(state=tk.DISABLED)
        self.button_clear.config(state=tk.DISABLED)

    def button_select_click_handler(self):
        filename = tk.filedialog.askopenfilename()
        self.entry_obj_val.set(filename)

    def button_start_click_handler(self):
        idx_list = []              # thread id
        rw_list = []               # writer or reader
        start_time_list = []       # start time
        continue_time_list = []    # continue time
        if self.check_box_var.get() == 1:
            filename = self.entry_obj_path.get()
            self.loadData(filename, idx_list, rw_list, start_time_list, continue_time_list)
            self.run(idx_list, rw_list, start_time_list, continue_time_list)
        elif self.check_box_var.get() == 2:
            data = self.list_box_input.get(0, tk.END)
            for x in data:
                x = x.split()
                idx_list.append(int(x[0]))
                rw_list.append(x[1])
                start_time_list.append(int(x[2]))
                continue_time_list.append(int(x[3]))
            self.run(idx_list, rw_list, start_time_list, continue_time_list)
        else:
            print(tk.messagebox.showerror(title="Error", message="输入方式不能为空!"))
    
    def loadData(self, filename, idx_list, rw_list, start_time_list, continue_time_list):
        with open(filename, 'r') as f:
            data = f.readlines()
            for x in data:
                x = x.split()
                idx_list.append(int(x[0]))
                rw_list.append(x[1])
                start_time_list.append(int(x[2]))
                continue_time_list.append(int(x[3]))
        
    def run(self, idx_list, rw_list, start_time_list, continue_time_list):
        rw = ReaderWriter()
        self.list_box_output.delete(0, tk.END)
        self.list_box_output.insert(tk.END, "---------All threads start---------")
        for i in range(len(rw_list)):
            if rw_list[i] == 'R':
                t = threading.Thread(target=rw.reader, args=(idx_list[i],
                start_time_list[i], continue_time_list[i], self))
                t.start()
            else:
                t = threading.Thread(target=rw.writer, args=(idx_list[i],
                start_time_list[i], continue_time_list[i], self))
                t.start()


class ReaderWriter():
    def __init__(self):
        self.R_mutex = threading.Semaphore(1)
        self.W_mutex = threading.Semaphore(1)
        self.R_count = 0

    def reader(self, idx, prepare_read, continue_time, window):
        """ Reader

        Args:
            idx: int, id number of readers
            prepare_read: int, arriving time of readers
            continue_time: int, reading time of readers
        """
        time.sleep(prepare_read)

        self.R_mutex.acquire()
        if self.R_count == 0:
            self.W_mutex.acquire()
        self.R_count += 1
        self.R_mutex.release()
        window.list_box_output.insert(tk.END, f"Reader{idx} is reading.")
        time.sleep(continue_time)
        window.list_box_output.insert(tk.END, f"Reader{idx} has finished reading.")
        self.R_mutex.acquire()
        self.R_count -= 1
        if self.R_count == 0:
            self.W_mutex.release()
        self.R_mutex.release()

    def writer(self, idx, prepare_write, continue_time, window):
        """ Writer

        Args:
            idx: int, id number of writers
            prepare_write: int, arriving time of writers
            continue_time: int, writing time of writers
        """
        time.sleep(prepare_write)
        self.W_mutex.acquire()
        window.list_box_output.insert(tk.END, f"Writer{idx} is writing.")
        time.sleep(continue_time)
        window.list_box_output.insert(tk.END, f"Writer{idx} has finished writing.")
        self.W_mutex.release()


def main():
    window = tk.Tk()
    window.title("读者写者问题")
    window.resizable(width=False, height=False)
    app = Application(master=window)
    app.mainloop()


if __name__ == '__main__':
    main()
