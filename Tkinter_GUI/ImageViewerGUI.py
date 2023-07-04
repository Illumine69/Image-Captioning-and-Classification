from my_package.model import ImageCaptioningModel
from my_package.model import ImageClassificationModel
from tkinter import *
from functools import partial
from PIL import ImageTk, Image
from tkinter import filedialog

def fileClick(clicked):
    # function to call when the filebrowser button (Open) is clicked.
    # This function should pop-up a dialog for the user to select an input image file.

    global file_path
    file_path = filedialog.askopenfilename(initialdir = "./data/imgs", title = "Select a File", filetypes = (("jpeg files", "*.jpg"), ("all files", "*.*")))

    if file_path:
        filename = file_path.split("/")[-1]
        inputLabel.config(text=filename)
        img = ImageTk.PhotoImage(Image.open(file_path))
        my_image_label.config(image=img)
        my_image_label.image = img
        my_image_label.grid(row = 1, column = 0, columnspan = 3, padx = 5, pady = 5)



def process(clicked, captioner, classifier):
    # This function will produce the required output when 'Process' button is clicked.
    # Note: It also handles the case if the user clicks on the `Process` button without selecting any image file.
    
    #if image is not selected, return "No image is selected"
    if inputLabel.cget("text") == "":
        print("Select input image first!")
        return
    
    #if captioning is selected, call captioner.predict()
    elif clicked.get() == "Captioning":
        output = captioner(file_path)
        outputLabel_title.configure(text = "Top 3 captions", font = ('bold',18))
        outputLabel.configure(text = '\n' + output[0] + '\n' + output[1] + '\n' + output[2], font = ('bold',15))
    
    #if classification is selected, call classifier.predict()
    elif clicked.get() == "Classification":
        output = classifier(file_path)
        outputLabel_title.configure(text = "Top 3 classes", font = ('bold',18))
        outputLabel.configure(text = f"\n{output[0][1]} - {output[0][0]*100:.5f}%\n{output[1][1]} - {output[1][0]*100:.5f}%\n{output[2][1]} - {output[2][0]*100:.5f}%\n", font = ('bold',15))

    outputLabel_title.grid(pady = 5, padx = 5, row = 0)
    outputLabel.grid(padx = 5, pady = 5, row = 1)
    outputFrame.grid(pady = 5, padx = 5, row = 1, column = 3, columnspan = 2)
    outputFrame.configure(highlightthickness=3, highlightbackground="black")

if __name__ == '__main__':
    
    # Instantiate the root window.
    root = Tk()
    # Provide a title to the root window.
    root.title("GUI for Image Captioning and Classification | Sanskar Mittal | 21CS10057")
    # Instantiate the captioner, classifier models.
    captioner = ImageCaptioningModel()
    classifier = ImageClassificationModel()
    # Declare the variable to store the selected option from the drop-down menu.
    clicked = StringVar()
    clicked.set("Captioning")

    # Declare a text widget to display the input image.
    inputLabel = Label(root, bg = 'white' , bd = 1, relief = SUNKEN, width = 50)
    inputLabel.grid(pady = 5, padx = 5, row = 0, column = 0)

    # Declare the file browser button.
    my_image_label = Label(root)
    fileButton = Button(root, text = "Open", command = partial(fileClick, clicked))
    fileButton.grid(padx = 5, pady = 5, row = 0, column = 1)
    
    # Declare the drop-down button.
    drop = OptionMenu(root, clicked, "Captioning", "Classification", command = lambda x: clicked.set(x))
    drop.grid(padx = 5, pady = 5, row = 0, column = 2)
    # Declare the process button.
    processButton = Button(root, text = "Process", command = partial(process, clicked, captioner, classifier))
    processButton.grid(padx = 5, pady = 5, row = 0, column = 3, sticky = W)
    # Declare the output label.
    outputFrame = LabelFrame(root)
    outputLabel_title = Label(outputFrame)
    outputLabel = Label(outputFrame) 
    
    # Start the main loop.
    root.mainloop()
