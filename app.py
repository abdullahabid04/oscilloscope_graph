import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
from backend import plot_graph, open_dataset, calculate_cycle_time
from requirements import config
from utils import set_scaler_values, set_samples_values, set_position_offsets_values, set_no_of_channels, clear_plot


class App(object):
    def __init__(self, win):
        self.win = win

        self.settings_frame = None
        self.graph_frame = None
        self.subplot = None
        self.canvas = None

    def run(self):
        self.setup_ui()
        self.create_graph()

    def setup_ui(self):
        main_frame = tk.Frame(self.win)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.settings_frame = tk.Frame(main_frame)
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

        self.graph_frame = tk.Frame(main_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        channel_selectors = tk.Frame(self.settings_frame)
        channel_selectors.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        channel_scalers = tk.Frame(self.settings_frame)
        channel_scalers.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        channel_position_offsets = tk.Frame(self.settings_frame)
        channel_position_offsets.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        channel_samples = tk.Frame(self.settings_frame)
        channel_samples.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        buttons = tk.Frame(self.settings_frame)
        buttons.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        var_ch1 = tk.IntVar()
        var_ch2 = tk.IntVar()
        var_ch3 = tk.IntVar()
        var_ch4 = tk.IntVar()
        channels_no = tk.IntVar()
        cycle_time = tk.DoubleVar()

        channel_selection = tk.Label(channel_selectors, text="Select channel")

        ch1_btn = tk.Checkbutton(channel_selectors, text="CH1", variable=var_ch1, selectcolor='red',
                                 background='white', foreground='black', activebackground='black',
                                 activeforeground='white', highlightbackground='red', highlightcolor='red',
                                 command=lambda: plot_graph(self.subplot, self.canvas, channels=0, ch1=var_ch1.get(),
                                                            ch2=var_ch2.get(),
                                                            ch3=var_ch3.get(), ch4=var_ch4.get()))
        ch2_btn = tk.Checkbutton(channel_selectors, text="CH2", variable=var_ch2, selectcolor='green',
                                 background='white', foreground='black', activebackground='black',
                                 activeforeground='white', highlightbackground='green', highlightcolor='green',
                                 command=lambda: plot_graph(self.subplot, self.canvas, channels=0, ch1=var_ch1.get(),
                                                            ch2=var_ch2.get(),
                                                            ch3=var_ch3.get(), ch4=var_ch4.get()))
        ch3_btn = tk.Checkbutton(channel_selectors, text="CH3", variable=var_ch3, selectcolor='blue',
                                 background='white', foreground='black', activebackground='black',
                                 activeforeground='white', highlightbackground='blue', highlightcolor='blue',
                                 command=lambda: plot_graph(self.subplot, self.canvas, channels=0, ch1=var_ch1.get(),
                                                            ch2=var_ch2.get(),
                                                            ch3=var_ch3.get(), ch4=var_ch4.get()))
        ch4_btn = tk.Checkbutton(channel_selectors, text="CH4", variable=var_ch4, selectcolor='purple',
                                 background='white', foreground='black', activebackground='black',
                                 activeforeground='white', highlightbackground='purple', highlightcolor='purple',
                                 command=lambda: plot_graph(self.subplot, self.canvas, channels=0, ch1=var_ch1.get(),
                                                            ch2=var_ch2.get(),
                                                            ch3=var_ch3.get(), ch4=var_ch4.get()))
        ch_all_btn = tk.Button(channel_selectors, text="ALL",
                               command=lambda: plot_graph(self.subplot, self.canvas, channels=1, ch1=0,
                                                          ch2=0,
                                                          ch3=0, ch4=0))
        channel_selection.pack()
        ch1_btn.pack()
        ch2_btn.pack()
        ch3_btn.pack()
        ch4_btn.pack()
        ch_all_btn.pack()

        channel_scales = tk.Label(channel_scalers, text="scale channels")

        ch1_scaler = tk.Entry(channel_scalers, foreground='red')
        ch2_scaler = tk.Entry(channel_scalers, foreground='green')
        ch3_scaler = tk.Entry(channel_scalers, foreground='blue')
        ch4_scaler = tk.Entry(channel_scalers, foreground='purple')

        ch1_scaler.insert(0, config.CH1_SCALER)
        ch2_scaler.insert(0, config.CH2_SCALER)
        ch3_scaler.insert(0, config.CH3_SCALER)
        ch4_scaler.insert(0, config.CH4_SCALER)

        set_scaler_btn = tk.Button(channel_scalers, text="set",
                                   command=lambda: set_scaler_values(ch1_scaler.get(), ch2_scaler.get(),
                                                                     ch3_scaler.get(), ch4_scaler.get()))

        channel_scales.pack()
        ch1_scaler.pack()
        ch2_scaler.pack()
        ch3_scaler.pack()
        ch4_scaler.pack()
        set_scaler_btn.pack()

        channel_offsets = tk.Label(channel_position_offsets, text="channels position")

        ch1_offset = tk.Entry(channel_position_offsets, foreground='red')
        ch2_offset = tk.Entry(channel_position_offsets, foreground='green')
        ch3_offset = tk.Entry(channel_position_offsets, foreground='blue')
        ch4_offset = tk.Entry(channel_position_offsets, foreground='purple')

        ch1_offset.insert(0, config.CH1_OFFSET)
        ch2_offset.insert(0, config.CH2_OFFSET)
        ch3_offset.insert(0, config.CH3_OFFSET)
        ch4_offset.insert(0, config.CH4_OFFSET)

        set_offsets_btn = tk.Button(channel_position_offsets, text="set",
                                    command=lambda: set_position_offsets_values(ch1_offset.get(), ch2_offset.get(),
                                                                                ch3_offset.get(), ch4_offset.get(), ))

        channel_offsets.pack()
        ch1_offset.pack()
        ch2_offset.pack()
        ch3_offset.pack()
        ch4_offset.pack()

        set_offsets_btn.pack()

        no_channels_label = tk.Label(buttons, text="so of channels")
        open_plot_btn = tk.Label(buttons, text="open / plot")

        select_no_channels = tk.Spinbox(buttons, from_=1, to=4, textvariable=channels_no,
                                        command=lambda: set_no_of_channels(channels_no.get()))
        select_file_btn = tk.Button(buttons, text="open", command=open_dataset)
        plot_button = tk.Button(buttons, text="plot", command=lambda: plot_graph(self.subplot, self.canvas, channels=1))
        clear_plot_btn = tk.Button(buttons, text='clear', command=lambda: clear_plot(self.subplot, self.canvas))

        no_channels_label.pack()
        select_no_channels.pack()
        open_plot_btn.pack()
        select_file_btn.pack()
        plot_button.pack()
        clear_plot_btn.pack()

        channel_sample = tk.Label(channel_samples, text="start point\tend point")
        cycle_time_label = tk.Label(channel_samples, textvariable=cycle_time)

        ch1_sample_start = tk.Entry(channel_samples, foreground='red')
        ch2_sample_start = tk.Entry(channel_samples, foreground='green')
        ch3_sample_start = tk.Entry(channel_samples, foreground='blue')
        ch4_sample_start = tk.Entry(channel_samples, foreground='purple')

        ch1_sample_end = tk.Entry(channel_samples, foreground='red')
        ch2_sample_end = tk.Entry(channel_samples, foreground='green')
        ch3_sample_end = tk.Entry(channel_samples, foreground='blue')
        ch4_sample_end = tk.Entry(channel_samples, foreground='purple')

        cycle_index_start = tk.Entry(channel_samples)
        cycle_index_end = tk.Entry(channel_samples)
        cycle_time_channel_selector = tk.Entry(channel_samples)

        ch1_sample_start.insert(0, config.CH1_SAMPLE_START)
        ch2_sample_start.insert(0, config.CH2_SAMPLE_START)
        ch3_sample_start.insert(0, config.CH3_SAMPLE_START)
        ch4_sample_start.insert(0, config.CH4_SAMPLE_START)
        ch1_sample_end.insert(0, config.CH1_SAMPLE_END)
        ch2_sample_end.insert(0, config.CH2_SAMPLE_END)
        ch3_sample_end.insert(0, config.CH3_SAMPLE_END)
        ch4_sample_end.insert(0, config.CH4_SAMPLE_END)

        set_samples_button = tk.Button(channel_samples, text="set", command=lambda: set_samples_values(
            ch1_sample_start.get(),
            ch2_sample_start.get(),
            ch3_sample_start.get(),
            ch4_sample_start.get(),
            ch1_sample_end.get(),
            ch2_sample_end.get(),
            ch3_sample_end.get(),
            ch4_sample_end.get()
        ))

        calculate_cycle_time_btn = tk.Button(channel_samples, text='calculate', command=lambda: calculate_cycle_time(
            "CH" + cycle_time_channel_selector.get(), cycle_time, int(cycle_index_start.get()),
            int(cycle_index_end.get())))

        channel_sample.grid(column=0, columnspan=2, row=0)

        ch1_sample_start.grid(column=0, row=1)
        ch1_sample_end.grid(column=1, row=1)

        ch2_sample_start.grid(column=0, row=2)
        ch2_sample_end.grid(column=1, row=2)

        ch3_sample_start.grid(column=0, row=3)
        ch3_sample_end.grid(column=1, row=3)

        ch4_sample_start.grid(column=0, row=4)
        ch4_sample_end.grid(column=1, row=4)

        set_samples_button.grid(column=0, columnspan=2, row=5)

        cycle_time_label.grid(column=0, columnspan=2, row=6)
        cycle_time_channel_selector.grid(column=0, columnspan=2, row=7)

        cycle_index_start.grid(column=0, row=8)
        cycle_index_end.grid(column=1, row=8)

        calculate_cycle_time_btn.grid(column=0, columnspan=2, row=9)

    def create_graph(self):
        matplotlib.rc('font', size=8)
        figure = Figure()
        figure.set_facecolor((0, 0, 0, 0))

        self.subplot = figure.add_subplot(111)

        self.subplot.spines['top'].set_visible(False)
        self.subplot.spines['right'].set_visible(False)
        self.subplot.spines['bottom'].set_visible(True)
        self.subplot.spines['left'].set_visible(True)

        self.subplot.spines['bottom'].set_color('#1e1953')
        self.subplot.spines['left'].set_color('#1e1953')
        self.subplot.spines['top'].set_color('#1e1953')
        self.subplot.spines['right'].set_color('#1e1953')

        self.subplot.tick_params(axis='x', colors='#1e1953')
        self.subplot.tick_params(axis='y', colors='#1e1953')

        self.subplot.set_xlabel('TIME (ms)')
        self.subplot.set_ylabel('AMPLITUDE')

        self.canvas = FigureCanvasTkAgg(figure, self.graph_frame)
        self.canvas.draw()

        toolbar_frame = ttk.Frame(self.graph_frame)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        toolbar_frame.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.canvas._tkcanvas.pack(fill=tk.BOTH, expand=True)
