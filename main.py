from tkinter import Tk
from app import App


def main():
    root = Tk()

    root.title("waveform plots")
    root.geometry('800x600')

    app = App(root)
    app.run()

    root.mainloop()


if __name__ == "__main__":
    main()
