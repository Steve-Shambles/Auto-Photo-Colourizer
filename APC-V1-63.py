"""
Auto Photo colourizer V1.63
Steve Shambles. Updated Feb 2023
stevepython.wordpress.com

Requirements:
pip3 install matplotlib
pip3 install numpy
pip3 install opencv-python
pip3 install pillow
"""
import os
import sys
from tkinter import Button, DISABLED, filedialog, FLAT, Label, LabelFrame
from tkinter import messagebox, Menu, NORMAL, PhotoImage, Tk, Toplevel
import webbrowser as web

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


root = Tk()
root.title('Auto Photo Colourizer V1.63')
root.resizable(False, False)


def msg_box():
    """Custom non-blocking message box."""
    global custom_mbox
    custom_mbox = Toplevel(root)
    custom_mbox.title('APC V1.63. ')
    custom_mbox.attributes('-topmost', 1)  # Bring custom window to front.

    # Remove the toolbar from the msg box.
    # custom_mbox.attributes('-toolwindow', 1) # not linux compatiable
    
    # Iconify msg box if exit X is hit by user, rather than lose the window.
    custom_mbox.protocol('WM_DELETE_WINDOW', custom_mbox.iconify)

    cstm_mb_label = Label(custom_mbox, bg='indianred',
                          text='\n    Auto Photo Colourizer    \n\n'
                          '    Colourizing image....   \n'
                          '\nplease wait...\n')
    cstm_mb_label.grid()

    # Centre it.
    WINDOW_WIDTH = custom_mbox.winfo_reqwidth()
    WINDOW_HEIGHT = custom_mbox.winfo_reqheight()
    POSITION_RIGHT = int(custom_mbox.winfo_screenwidth()/2 - WINDOW_WIDTH/2)
    POSITION_DOWN = int(custom_mbox.winfo_screenheight()/2 - WINDOW_HEIGHT/2)
    custom_mbox.geometry('+{}+{}'.format(POSITION_RIGHT, POSITION_DOWN))

    root.update()


def load_img():
    """Load black and white image via file selector."""
    global users_image
    users_image = ''
    users_image = filedialog.askopenfilename(title='Please select a black and white image to colorize',
                                             filetypes=(('All files', '*.*'),
                                                        ('Jpg', '*.Jpg'),
                                                        ('Png', '*.png'),
                                                        ('Bmp', '*.bmp')),)
    if not users_image:
        return
    if users_image.endswith('.png') or users_image.endswith('.bmp')  \
        or users_image.endswith('.jpg'):

        # Display users original image.
        show_image = cv2.imread(users_image)
        # convert to gray in case sepia or something dodgy like that.
        show_image = cv2.cvtColor(show_image, cv2.COLOR_BGR2GRAY)
        show_image = cv2.resize(show_image, (640, 480))
        cv2.imshow('Img temp resized to 640x480 - no aspect ratio.',
                   show_image)
        cv2.waitKey(300)
        colorize_img_btn.configure(state=NORMAL)
    else:
        messagebox.showerror('File Error!:', 'Error, the file: \n\n'
                             + str(users_image) + '\n\n'
                             'is not a jpg, png or bmp.')


def save_img():
    """Save colourized image via file selector."""
    global colorized

    saved_image = 'noname'
    saved_image = filedialog.asksaveasfilename(title='Type a new name for your colourized image')

    if saved_image == '':
        saved_image = 'noname'

    saved_image = saved_image + str('.jpg')
    cv2.imwrite(saved_image, cv2.cvtColor(colorized, cv2.COLOR_RGB2BGR))
    cv2.destroyAllWindows()
    load_img_btn.configure(state=NORMAL)
    colorize_img_btn.configure(state=DISABLED)
    save_img_btn.configure(state=DISABLED)


def colourize():
    """AI algo to colourize a black and white image."""
    global users_image
    global colorized

    # load_img_btn.configure(state=DISABLED)
    colorize_img_btn.configure(state=DISABLED)

    msg_box()

    # Define Model Paths:
    prototxt = 'colorization_deploy_v2.prototxt'
    model = 'colorization_release_v2.caffemodel'
    points = 'pts_in_hull.npy'

    # Load serialized black and white colorizer model and cluster.
    net = cv2.dnn.readNetFromCaffe(prototxt, model)
    pts = np.load(points)

    # Add the cluster centers as 1x1 convolutions to the model.
    class8 = net.getLayerId('class8_ab')
    conv8 = net.getLayerId('conv8_313_rh')
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype('float32')]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype='float32')]

    # Load the input image, scale it and convert it to Lab.
    image = cv2.imread(users_image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    # Extracting “L”.
    scaled = image.astype('float32') / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_RGB2LAB)
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    # Predicting “a” and “b”.
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    # Creating a colorized Lab photo (L + a + b).
    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

    # Converting to RGB.
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2RGB)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype('uint8')
    plt.imshow(colorized)
    plt.axis('off')

    # Save.
    cv2.imwrite('temp-col-image.jpg',
                cv2.cvtColor(colorized, cv2.COLOR_RGB2BGR))

    # Display colourized image.
    img = cv2.imread('temp-col-image.jpg')
    img = cv2.resize(img, (640, 480))
    cv2.imshow('Colour image resized to 640x480. Original aspect ratio will be used when saved.', img)
    cv2.waitKey(300)
    save_img_btn.configure(state=NORMAL)

    custom_mbox.destroy()


def about_menu():
    """About program msgbox."""
    messagebox.showinfo('APC Program Information',
                        'Auto Photo\n'
                        'Colourizer\n'
                        'V1.63\n\n'
                        'Freeware by\n'
                        'Steve Shambles\n'
                        '(c) Feb 2021-23\n')


def open_prg_dir():
    """File browser to view contents of program folder."""
    cwd = os.getcwd()
    web.open(cwd)


##def visit_blog():
##    """Visit my old python blog."""
##    web.open('https://stevepython.wordpress.com/')


##def contact_me():
##    """Go to the contact page on my blog."""
##    web.open('https://stevepython.wordpress.com/contact/')


def help_text():
    """Show help msg box."""
    web.open('apc-help.txt')


def donate_me():
    """User splashes the cash here!"""
    web.open("https:\\paypal.me/photocolourizer")


def visit_github():
    """View source code of APC and my other Python projects at GitHub."""
    web.open("https://github.com/steve-shambles")


def exit_apc():
    """Yes-no requestor to exit program."""
    ask_yn = messagebox.askyesno('Question',
                                 'Quit APC?')
    if ask_yn is False:
        return
    root.destroy()
    sys.exit()


def color_folder_of_imgs():
    """Colourize a folder of users images automatically and save."""
    global users_image
    users_image = None

    # Open the tk folder requestor.
    folder_slctd = ''
    folder_slctd = filedialog.askdirectory(title='Please select a folder of images')

    if not folder_slctd:
        return
    load_img_btn.configure(state=DISABLED)
    files = os.listdir(folder_slctd)

    for file in files:
        users_image = folder_slctd + '/' + file
        if file.endswith('.png') or file.endswith('.bmp')  \
           or file.endswith('.jpg'):

            colourize()

            fname = (os.path.basename(users_image))
            new_fname = (os.path.splitext(fname)[0])

            save_img_btn.configure(state=DISABLED)
            save_img = folder_slctd + '/' + new_fname + '-colorized.jpg'
            cv2.imwrite(save_img, cv2.cvtColor(colorized, cv2.COLOR_RGB2BGR))
            cv2.destroyAllWindows()

    load_img_btn.configure(state=NORMAL)
    messagebox.showinfo('Information', 'Batch operation complete')
    web.open(folder_slctd)


# Insert logo.
logo_frame = LabelFrame(root)
logo_frame.grid(padx=5, pady=5)

logo_image = Image.open('pc-panel-340x125.png')
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = Label(logo_frame, image=logo_photo)
logo_label.logo_image = logo_photo
logo_label.grid(padx=2, pady=2)

# Buttons.
btns_frame = LabelFrame(root)
btns_frame.grid(padx=10, pady=10)

# Note. making btns relief=flat removes ugly button surround.
load_img_btn = Button(btns_frame, command=load_img)
photo = PhotoImage(file='buttons/load-img-btn.png')
load_img_btn.config(image=photo, relief=FLAT,
                    width='80', height='40')
load_img_btn.grid(pady=15, padx=15, column=0, row=0)

colorize_img_btn = Button(btns_frame, command=colourize)
PHOTO2 = PhotoImage(file='buttons/colourize-btn.png')
colorize_img_btn.config(image=PHOTO2, relief=FLAT,
                        width='80', height='40')
colorize_img_btn.grid(pady=15, padx=15, column=1, row=0)

save_img_btn = Button(btns_frame, command=save_img)
PHOTO3 = PhotoImage(file='buttons/save-img-btn.png')
save_img_btn.config(image=PHOTO3, relief=FLAT,
                    width='80', height='40')
save_img_btn.grid(pady=15, padx=15, column=2, row=0)

# pre-load icons for drop-down menu.
help_icon = ImageTk.PhotoImage(file='icons/help-16x16.ico')
about_icon = ImageTk.PhotoImage(file='icons/about-16x16.ico')
blog_icon = ImageTk.PhotoImage(file='icons/blog-16x16.ico')
exit_icon = ImageTk.PhotoImage(file='icons/exit-16x16.ico')
donation_icon = ImageTk.PhotoImage(file='icons/donation-16x16.ico')
github_icon = ImageTk.PhotoImage(file='icons/github-16x16.ico')
contact_icon = ImageTk.PhotoImage(file='icons/contact-16x16.ico')
folder_icon = ImageTk.PhotoImage(file='icons/folder-16x16.ico')
prg_fldr_icon = ImageTk.PhotoImage(file='icons/prg-fldr-16x16.ico')

# Drop-down menu.
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Menu', menu=file_menu)

file_menu.add_command(label='Help', compound='left',
                      image=help_icon, command=help_text)
file_menu.add_command(label='About', compound='left',
                      image=about_icon, command=about_menu)
file_menu.add_separator()
file_menu.add_command(label='Auto colourize folder of images',
                      compound='left',
                      image=folder_icon, command=color_folder_of_imgs)
file_menu.add_command(label='Open program Folder', command=open_prg_dir,
                      compound='left',
                      image=prg_fldr_icon)
file_menu.add_separator()
file_menu.add_command(label='Python source code on GitHub', compound='left',
                      image=github_icon, command=visit_github)
file_menu.add_command(label='Make a small donation via PayPal',
                      compound='left',
                      image=donation_icon, command=donate_me)
file_menu.add_separator()
file_menu.add_command(label='Exit', compound='left',
                      image=exit_icon, command=exit_apc)
root.config(menu=menu_bar)

root.eval('tk::PlaceWindow . Center')
root.protocol("WM_DELETE_WINDOW", exit_apc)

# Check help.txt available, if not disbale help iyem in menu.
help_file = os.path.isfile('apc-help.txt')
if not help_file:
    file_menu.entryconfig(0, state=DISABLED)

# Disable these buttons at startup.
colorize_img_btn.configure(state=DISABLED)
save_img_btn.configure(state=DISABLED)

root.mainloop()
