from tkinter import *
from buffer import Buffer

class BufferOverflowVisualizer():
    def __init__(self):
        self.buffer = Buffer("little", "x32")
        self.root = Tk()
        self.root.geometry("1080x720")
        self.root.resizable(width=False, height=False)
        self.root.title("Buffer Overflow Visualizer")
        self.root.config(background="grey")

        self.code_view = Label(self.root, text="Code View", relief=SOLID, justify=LEFT)
        self.program_view = Label(self.root, text="Program View", relief=SOLID, width=50, justify=LEFT)
        self.register_view = Label(self.root, text="Register View", relief=SOLID, width=50)
        self.stack_view = Label(self.root, text="Stack View", relief=SOLID, width=50)
        self.input_box = Text(self.root, relief=SOLID, width=50)
        self.buf_slider = Scale(self.root, from_=1, to=25, orient=HORIZONTAL, command=self.buf_slider_interact, relief=SOLID, label="Buf Size:")
        self.reset_button = Button(self.root, text="Reset", relief=SOLID, width=50, command=self.reset_button_interact, bg="red")
        self.execute_button = Button(self.root, text="Execute", relief=SOLID, width=50, command=self.execute_button_interact, bg="lime")

        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.endianess = StringVar()
        self.architecture = StringVar()
        self.resolution = StringVar() 

        self.endianess_options = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Endianess", menu=self.endianess_options)
        self.endianess_options.add_radiobutton(label="Little Endian", command=self.update_preferences, value="little", variable=self.endianess)
        self.endianess_options.add_radiobutton(label="Big Endian", command=self.update_preferences, value="big", variable=self.endianess)

        self.architecture_options = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Architecture", menu=self.architecture_options)
        self.architecture_options.add_radiobutton(label="x32", command=self.update_preferences, value="x32", variable=self.architecture)
        self.architecture_options.add_radiobutton(label="x64", command=self.update_preferences, value="x64", variable=self.architecture)

        self.resolution_options = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Screen Resolution", menu=self.resolution_options)
        self.resolution_options.add_radiobutton(label="720x480", command=self.update_preferences, value="720x480", variable=self.resolution)
        self.resolution_options.add_radiobutton(label="1080x720", command=self.update_preferences, value="1080x720", variable=self.resolution)

        self.endianess_options.invoke(0)
        self.architecture_options.invoke(0)
        self.resolution_options.invoke(1)
        self.refresh_display()
        self.input_box.insert("1.0", 'AAAAAAAAA')

    def update_preferences(self): 
        self.reset_button_interact()
        current_window = str(self.root.winfo_screenwidth()) + "x" + str(self.root.winfo_screenheight())
        if self.resolution.get() != current_window:
            self.root.geometry(self.resolution.get())
        if self.resolution.get() == "720x480":
            self.code_view.place(x=16,y=16,width=200,height=266)
            self.program_view.place(x=235,y=16,width=200,height=266)
            self.register_view.place(x=450,y=400,width=255,height=65)
            self.stack_view.place(x=450,y=16,width=255,height=366)
            self.input_box.place(x=235,y=317,width=200,height=65)
            self.buf_slider.place(x=235,y=400,width=200,height=65)
            self.buf_slider.config(to=20)
            self.reset_button.place(x=16,y=400,width=200,height=65)
            self.execute_button.place(x=16,y=317,width=200,height=65)
        elif self.resolution.get() == "1080x720":
            self.code_view.place(x=20,y=20,width=300,height=400)
            self.program_view.place(x=350,y=20,width=300,height=400)
            self.register_view.place(x=675,y=600,width=380,height=100)
            self.stack_view.place(x=675,y=20,width=380,height=550)
            self.input_box.place(x=350,y=475,width=300,height=100)
            self.buf_slider.place(x=350,y=600,width=300,height=100)
            self.buf_slider.config(to=32)
            self.reset_button.place(x=20,y=600,width=300,height=100)
            self.execute_button.place(x=20,y=475,width=300,height=100)

    def refresh_display(self):
        self.stack_view.config(text=self.buffer.get_stack())
        self.register_view.config(text=self.buffer.get_registers())
        self.program_view.config(text=self.buffer.get_program_view())
        self.code_view.config(text=self.buffer.get_code_view())

    def buf_slider_interact(self, buf_size):
        self.buffer.set_buf(int(buf_size))
        self.refresh_display() 

    def execute_button_interact(self):
        if self.buffer.executed is True:
            self.buffer = Buffer(self.endianess.get(), self.architecture.get())
            self.buf_slider_interact(self.buf_slider.get())
        self.buffer.set_input(self.input_box.get("1.0", END).replace('\n', ''))
        self.buffer.buffer_overflow()
        self.refresh_display()

    def reset_button_interact(self):
        self.buffer = Buffer(self.endianess.get(), self.architecture.get())
        self.refresh_display()
        self.input_box.delete("1.0","end")
        self.buf_slider.set(1)

if __name__ == '__main__':
    app = BufferOverflowVisualizer()
    app.root.mainloop()