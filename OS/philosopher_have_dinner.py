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
        self.mutex = threading.Semaphore(1)

    def createWidgets(self):
        self.canva = tk.Canvas(self, width=300, height=300)
        self.canva.grid(row=0, columnspan=3)
        self.canva_initialize()

        button_start = tk.Button(self, text="Start", command=self.button_start_click_handler)
        button_start['width'] = 11 
        button_start.grid(row=1, column=0)
        button_renew = tk.Button(self, text="Renew", command=self.button_renew_click_handler)
        button_renew['width'] = 11 
        button_renew.grid(row=1, column=1)
        button_exit = tk.Button(self, text="Exit", command=self.quit)
        button_exit['width'] = 11 
        button_exit.grid(row=1, column=2)

    def canva_initialize(self):
        screen = turtle.TurtleScreen(self.canva)
        self.pen = turtle.RawTurtle(screen)
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.fillcolor('yellow')
        
        self.pen.penup()
        self.pen.goto(0, -100)
        for i in range(5):
            self.pen.begin_fill()
            self.pen.pendown()
            self.pen.circle(20)
            self.pen.write(i+1)
            self.pen.penup()
            self.pen.end_fill()
            self.pen.circle(100, 72)
            

    def button_start_click_handler(self):
        rlock1 = threading.RLock()
        rlock2 = threading.RLock()
        rlock3 = threading.RLock()
        rlock4 = threading.RLock()
        rlock5 = threading.RLock()

        self.philosopher1 = Philosopher(1, rlock5, rlock1)
        self.philosopher2 = Philosopher(2, rlock2, rlock1)
        self.philosopher3 = Philosopher(3, rlock2, rlock3)
        self.philosopher4 = Philosopher(4, rlock4, rlock3)
        self.philosopher5 = Philosopher(5, rlock4, rlock5)

        for i in range(5):
            t = threading.Thread(target=eval(f"self.philosopher{i+1}").have_dinner,
                                args=(self,))
            t.start()

    def button_renew_click_handler(self):
        self.pen.reset()
        self.canva_initialize()
    
    def update(self, idx, color):
        self.mutex.acquire()
        self.pen.fillcolor(color)
        self.pen.home()
        self.pen.goto(0, -100)
        self.pen.circle(100, (idx-1)*72)
        self.pen.begin_fill()
        self.pen.pendown()
        self.pen.circle(20)
        self.pen.write(idx)
        self.pen.penup()
        self.pen.end_fill()
        self.mutex.release()


class Philosopher():
    def __init__(self, idx, left, right):
        self.left = left
        self.right = right
        self.idx = idx
        self.colors = ['green', 'blue', 'red']

    
    def have_dinner(self, window):
        i = 0
        while True:
            if i >= 3:
                break
            self.think(window)
            left_chop = self.left.acquire()
            if left_chop:
                print(f"Philosopher{self.idx} takes the left chopstick for the {i+1}th time.")
        
            right_chop = self.right.acquire()
            if right_chop:
                print(f"Philosopher{self.idx} takes the right chopstick for the {i+1}th time.")
                self.eat(i, window)

            self.right.release()
            self.left.release()
            i += 1

    def eat(self, n, window):
        print(f"Philosopehr{self.idx} begins to have dinner for the {n+1}th time.")
        window.update(self.idx, self.colors[n])
        time.sleep(random.randint(1, 10)*0.1)

    def think(self, window):
        print(f"Philosopher{self.idx} is thinking.")
        window.update(self.idx, 'white')
        time.sleep(random.randint(1, 10)*0.1)


def main():
    window = tk.Tk()
    window.title("哲学家就餐演示")
    window.geometry("300x340")
    window.resizable(height=False, width=False)
    app = Application(master=window)
    app.mainloop()


if __name__ == '__main__':
    main()
