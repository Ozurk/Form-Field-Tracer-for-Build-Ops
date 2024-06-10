import pyautogui as pya
import time
import pyscreeze
import tkinter
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageGrab


def save_ok_image():
    # Check if there is an image in the clipboard
    try:
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            # Ask the user where to save the image
            file_path = 'pics/ok.png'
            if file_path:
                # Save the image to the specified path
                img.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
            else:
                messagebox.showwarning("Cancelled", "Image save cancelled.")
        else:
            messagebox.showerror("Error", "No image found in the clipboard.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")


def save_target_image():
    # Check if there is an image in the clipboard
    try:
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            # Ask the user where to save the image
            file_path = 'pics/target.png'
            if file_path:
                # Save the image to the specified path
                img.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
            else:
                messagebox.showwarning("Cancelled", "Image save cancelled.")
        else:
            messagebox.showerror("Error", "No image found in the clipboard.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")


class TextBoxDrawer:
    def __init__(self):
        self.overshoot_height_entry = None
        self.main_frame = None
        self.overshoot_width = None
        self.overshoot_height = None
        self.confidence_entry = None
        self.ok_image = None
        self.target_image = None
        self.root = None
        self.create_application()

    def create_application(self):
        self.root = tkinter.Tk()
        self.root.title('Textbox Maker GUI')
        self.main_frame = tkinter.Frame(self.root, bg="#a8a8a8")

        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        self.main_frame.pack()

        self.target_image = tkinter.Button(self.main_frame, text="Save Target Image From Clipboard",
                                           command=save_target_image, relief="groove", borderwidth=5, bg="#84cc34")
        self.target_image.grid(row=0, column=0, sticky=tkinter.NSEW, padx=10, pady=10)

        self.ok_image = tkinter.Button(self.main_frame, text="Save 'Ok' Image From Clipboard", command=save_ok_image,
                                       relief="groove", borderwidth=5, bg="#84cc34")
        self.ok_image.grid(row=0, column=1, sticky=tkinter.NSEW, padx=10, pady=10)

        confidence_label = tkinter.Label(self.main_frame, text="Enter the confidence percentage for the target image:")
        confidence_label.grid(row=1, column=0, columnspan=2, sticky=tkinter.NSEW)

        confidence_variable = tkinter.StringVar()
        confidence_variable.set("85")

        self.confidence_entry = tkinter.Spinbox(self.main_frame, from_=50, to=100, increment=1,
                                                textvariable=confidence_variable,
                                                justify=tkinter.CENTER)
        self.confidence_entry.grid(row=2, column=0, columnspan=2, sticky=tkinter.NSEW)

        overshoot_height_variable = tkinter.StringVar()
        overshoot_height_variable.set("0")
        overshoot_height_label = tkinter.Label(self.main_frame, text="Enter the overshoot height distance in pixels")
        overshoot_height_label.grid(row=3, column=0, columnspan=2, sticky=tkinter.NSEW)

        self.overshoot_height_entry = tkinter.Spinbox(self.main_frame, from_=0, to=100, increment=1,
                                                      textvariable=overshoot_height_variable,
                                                      justify=tkinter.CENTER)
        self.overshoot_height_entry.grid(row=4, column=0, columnspan=2, sticky=tkinter.NSEW)

        overshoot_width_label = tkinter.Label(self.main_frame, text="Enter the overshoot width distance in pixels")
        overshoot_width_label.grid(row=5, column=0, columnspan=2, sticky=tkinter.NSEW)
        self.overshoot_width = tkinter.Spinbox(self.main_frame, from_=0, to=100, increment=1, justify=tkinter.CENTER)
        self.overshoot_width.grid(row=6, column=0, columnspan=2, sticky=tkinter.NSEW)

        start_button = tkinter.Button(self.main_frame, text="Start", command=self.start_textbox_maker)
        start_button.grid(row=7, column=0, columnspan=2, sticky=tkinter.NSEW)
        credits = tkinter.Label(self.main_frame, text="Created By Hunter Metzger", bg='black', fg='white',
                                          anchor=tkinter.SW)
        credits.grid(row=9, column=0, columnspan=2, sticky=tkinter.NSEW)
        help_button = tkinter.Button(self.main_frame, bitmap="question")
        help_button.grid(self.main_frame, row=8)
        self.main_frame.bind('<Return>', self.start_textbox_maker)

    def create_textbox(self):
        all_textboxes = list(
            pya.locateAllOnScreen("pics/target.png", confidence=int(self.confidence_entry.get()) / 100))
        textbox = all_textboxes[0]
        height = textbox.height
        width = textbox.width

        pya.moveTo(textbox.left + 2, textbox.top)
        pya.click()
        pya.dragTo(textbox.left + width + int(self.overshoot_width.get()),
                   textbox.top + height + int(self.overshoot_height.get()),
                   3, pya.easeOutQuad)
        # set over or under shoot above
        time.sleep(.5)

        pya.moveTo(pya.locateOnScreen("pics/ok.png", confidence=.8))
        pya.click()
        for textboxes in all_textboxes:
            print(textboxes)
            self.create_textbox()

    def run_mainloop(self):
        self.root.mainloop()

    def start_textbox_maker(self, event=None):
        try:
            attempts = 0
            while attempts < 25:
                try:
                    self.create_textbox()
                except pyscreeze.ImageNotFoundException:
                    pya.scroll(-100)
                    attempts += 1
                    print("Attempt number: " + str(attempts) + " \nWill quit after 25 failed attempts")
                    time.sleep(.25)
                except pya.ImageNotFoundException:
                    pya.scroll(-150)
                    attempts += 1
                    print("Attempt number: " + str(attempts) + " \nWill quit after 25 failed attempts")
                    time.sleep(.25)
        except ValueError:
            messagebox.showerror("error", "Please fill out all the fields.\n(Hint: 90)")


def force_quit():
    quit()


if __name__ == "__main__":
    application = TextBoxDrawer()
    application.run_mainloop()
