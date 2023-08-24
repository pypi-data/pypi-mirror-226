from pathlib import  Path
import tkinter as tk
from tkinter import font

from trigger_count.daq.fast import SubprocessDaq

SOURCES = [
    "twophoton_scanner",
    "widefield_camera",
    "vitals_monitor",
    "left_eye_camera",
    "right_eye_camera",
]

DEFAULT_PORTS = [
    "DIO0",
    "Do not use",
    "DIO1",
    "DIO2",
    "DIO3",
]


class LabjackGui:
    def __init__(self, output_folder: Path | None = None) -> None:
        self.output_folder = output_folder

        self.window = tk.Tk()
        self.window.title("Labjack Configuration")
        self.window.geometry("500x275")

        self.port_variables = {}
        self.main_variables = {}

        self.proceed = False

    def set_up(self) -> None:
        frame = tk.Frame(self.window)
        frame.pack()

        tk.Label(frame, text="Trigger source").grid(row=0, column=0)
        tk.Label(frame, text="Port").grid(row=0, column=1)
        tk.Label(frame, text="Main counter").grid(row=0, column=2)

        for i_source, source in enumerate(SOURCES):
            i_row = i_source + 1

            label = tk.Label(frame, text=source)
            label.grid(row=i_row, column=0)

            variable = tk.StringVar()
            variable.set(DEFAULT_PORTS[i_source])
            dropdown = tk.OptionMenu(frame, variable, *DEFAULT_PORTS)
            dropdown.grid(row=i_row, column=1)
            self.port_variables[source] = variable

            variable = tk.BooleanVar()
            if i_source == 0:
                variable.set(True)
            else:
                variable.set(False)
            check_box = tk.Checkbutton(frame, variable=variable)
            check_box.grid(row=i_row, column=2)
            self.main_variables[source] = variable

        frame = tk.Frame()
        frame.pack()
        go_button = tk.Button(frame, text="Continue", command=self.enable)
        go_button.grid(row=0, column=0)

        abort_button = tk.Button(frame, text="Abort", command=self.window.destroy)
        abort_button.grid(row=0, column=1)

        frame = tk.Frame(self.window)
        frame.pack()

        italics = font.Font(slant="italic", size=10)
        text = "Note: Labjack T7 can only handle up to 4 counters at the same time.\n" \
               "Use DIO0 for either twophoton_scanner or widefield_camera"
        tk.Label(frame, text=text, font=italics).pack()

    def enable(self) -> None:
        self.proceed = True
        self.window.destroy()

    def run(self) -> SubprocessDaq:
        self.set_up()
        self.window.mainloop()

        if self.proceed:
            daq = self.configure_labjack()
        else:
            raise Exception("User aborted configuration.")
        return daq

    def configure_labjack(self) -> SubprocessDaq:
        daq = SubprocessDaq(self.output_folder)
        for source, variable in self.port_variables.items():
            port = variable.get()
            if "DIO" in port:
                daq.add_counter(source, port)
                print(f"Counter: {source} -> {port}")

        for source, variable in self.main_variables.items():
            is_main = variable.get()
            if is_main:
                daq.set_main_counter(source)
                print(f"Counter: {source} set as main counter.")
        return daq

