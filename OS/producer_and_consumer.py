import threading
import tkinter as tk
import turtle
import time
import random


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.createWidgets()
        self.pack()

    def createWidgets(self):
        self.canva = tk.Canvas(self, width=300, height=300)
        self.canva.grid(row=0, columnspan=3)
        self.canva_initialize()

        button_start = tk.Button(self, text="Start", command=self.button_start_click_handler)
        button_start['width'] = 12
        button_start.grid(row=1, column=0)
        button_exit = tk.Button(self, text="Exit", command=self.quit)
        button_exit['width'] = 12
        button_exit.grid(row=1, column=1)

    def canva_initialize(self):
        screen = turtle.TurtleScreen(self.canva)
        self.pen = turtle.RawTurtle(screen)
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.speed(0)

    def button_start_click_handler(self):
        pc = ProducerConsumer()

        t1 = threading.Thread(target=pc.producer, args=(1, self))
        t2 = threading.Thread(target=pc.consumer, args=(1, self))
        t3 = threading.Thread(target=pc.producer, args=(2, self))

        for i in range(1, 4):
            eval(f"t{i}").start()

    def update(self, idx, color):
        x = idx % 10
        y = idx // 10
        self.pen.pencolor(color)
        self.pen.fillcolor(color)
        if x == 0:
            self.pen.goto(-135+9*30, 120-(y-1)*30)
        else:
            self.pen.goto(-135+(x-1)*30, 120-y*30)
        self.pen.pendown()
        self.pen.begin_fill()
        self.pen.circle(15)
        self.pen.end_fill()
        self.pen.penup()


class ProducerConsumer():
    def __init__(self):
        self.queue = list()
        self.mutex = threading.Semaphore(1)
        self.empty = threading.Semaphore(10)
        self.full = threading.Semaphore(0)
        self.count1 = 0

    def producer(self, idx, window):
        colors = ['red', 'blue', 'green']
        while True:
            if self.count1 < 60:
                time.sleep(random.randint(1, 10)*0.1)
            elif self.count1 < 99:
                time.sleep(random.randint(1, 10)*0.3)
            else:
                break
            self.empty.acquire()
            self.mutex.acquire()
            self.count1 += 1
            self.queue.append(self.count1)
            print(f"生产者{idx}生产了{self.queue[-1]}")
            window.update(self.queue[-1], colors[idx-1])
            self.mutex.release()
            self.full.release()

    def consumer(self, idx, window):
        while True:
            if self.count1 < 60:
                time.sleep(random.randint(1, 10)*0.1)
            elif self.count1 < 100:
                time.sleep(random.randint(1, 10)*0.005)
            else:
                break
            self.full.acquire()
            self.mutex.acquire()
            count = self.queue.pop(0)
            window.update(count, 'white')
            print(f"消费者{idx}消费了{count}")
            self.mutex.release()
            self.empty.release()


def main():
    window = tk.Tk()
    window.title("生产者消费者问题演示")
    window.geometry("300x340")
    window.resizable(width=False, height=False)
    app = Application(master=window)
    app.mainloop()


if __name__ == '__main__':
    main()
