import tkinter as tk
import os
from PIL import ImageTk, Image
import subprocess
image_path = os.path.join(os.path.dirname(__file__), "./assets/splash.jpg")
min_width = 600
min_height = 580
videos_path = os.path.join(os.path.dirname(__file__), "videos/")
def_output_folder = "out"
class GUI:
    def __init__(self):
        #non tk vars
        self.possible_vids = self.determine_possible_videos()
        self.entered_vids = []
        #tk vars
        self.model_path = "iterations/seventh.pt"
        self.root = tk.Tk()
        self.root.title("Classifier")
        self.root.geometry(str(min_width)+"x"+str(min_height))
        self.root.minsize(min_width,min_height)
        self.root.resizable(False, True)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        parent_frame = tk.Frame(self.root)

        parent_frame.grid(column=0, row=0, sticky="news")
        parent_frame.columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(4, weight=1)

        img = Image.open(image_path)
        img.thumbnail((min_width,min_height))
        photo_img = ImageTk.PhotoImage(img)
        img_label = tk.Label(parent_frame, image=photo_img)
        img_label.grid(row=0, column=0)

        topframe = tk.LabelFrame(parent_frame, text="Select Input Videos", padx=30, pady=10)
        topframe.columnconfigure(1, minsize=80)
        topframe.grid(row=1, column=0, sticky="ew")

        video_label = tk.Label(topframe, text="Enter video files to process (must be in appropriate folder)")
        video_label.grid(row=0, column=0, sticky="w")

        self.names_entry = tk.Entry(topframe, width=40)
        self.names_entry.grid(row=1, column=0, sticky="w")

        enter_name_button = tk.Button(topframe, text="Enter Video", command=self.enter_video)
        enter_name_button.grid(row=1, column=1, sticky="e", padx=(20, 10))

        possible_vids_label = tk.Label(topframe, font=("TkDefaultFont", 12), text="Options: " + str(self.possible_vids), wraplength=350)
        possible_vids_label.grid(row=2, column=0, sticky="w")

        self.status_label_txt = tk.StringVar(value="No videos entered")
        self.status_label = tk.Label(topframe, font=("TkDefaultFont", 12), textvariable=self.status_label_txt, wraplength=350)
        self.status_label.grid(row=3, column=0, sticky="w")

        secondframe = tk.LabelFrame(parent_frame, text="Output", padx=15, pady=15)
        secondframe.grid(row=2, column=0, sticky="ew")

        self.output_label_txt = tk.StringVar(value="Output video(s) & spreadsheet will be at: " + self.determine_output_path())
        self.output_label = tk.Label(secondframe, textvariable=self.output_label_txt, wraplength=550)
        self.output_label.pack()

        thirdframe = tk.LabelFrame(parent_frame, text="ML-Configuration", padx=10, pady=5)
        thirdframe.grid(row=3, column=0, sticky="ew")

        gpu_checkbox = tk.Checkbutton(thirdframe, text="Use GPU")
        gpu_checkbox.pack()

        model_location = tk.Label(thirdframe, text="Model location: " + os.path.join(os.path.dirname(__file__),self.model_path), wraplength=550) 
        model_location.pack()

        fourthframe = tk.LabelFrame(parent_frame, pady=5)
        fourthframe.grid(row=4, column=0, sticky="news")

        start_inference = tk.Button(fourthframe, text="Start Inference", command=self.start_inference)
        start_inference.pack(expand=True, fill='x')

        kill_inference = tk.Button(fourthframe, text="Kill Running Inference(s)", command=self.kill_inference)
        kill_inference.pack(expand=True, fill='x')
        # make the frame height start out at exactly the right size

        self.root.mainloop()
    
    def start_inference(self):
        self.status_label_txt.set("Videos being processed") #figure out why this doesn't show
        args_list = ["python", "master_detect_data.py", "--videos"]
        args_list.extend(self.entered_vids)
        print(args_list)
        self.entered_vids = []
        subprocess.run(args_list)
        self.output_label_txt.set(self.determine_output_path())
        # delete folders if needed
    
    def kill_inference(self):
        print()

    def determine_output_path(self): 
        if os.path.exists(os.path.join(os.path.dirname(__file__), "output")):
            output_list = os.listdir(os.path.join(os.path.dirname(__file__), "output/"))
            max = 0
            print(output_list)
            for folder in output_list:
                if len(folder) == len(def_output_folder):
                    max = 2
                elif folder[3:len(folder)] == def_output_folder:
                    folder_num = int(folder[3:len(folder)])
                    if folder_num > max:
                        max = folder_num + 1
            if max == 0:
                return str(os.path.join(os.path.dirname(__file__), "output/out1"))
            else:
                return str(os.path.join(os.path.dirname(__file__), "output/" + def_output_folder + str(max)) + "/")
        else:
            return str(os.path.join(os.path.dirname(__file__), "output/out1"))
    
    def determine_possible_videos(self):
        files = os.listdir(videos_path)
        final_list = []
        for file in files:
            if file[-4:] == ".mp4":
                final_list.append(file)
        return final_list
    
    def enter_video(self):
        entered_vid = self.names_entry.get()
        self.names_entry.delete(0, tk.END)
        if entered_vid[-4:] == ".mp4":
            if os.path.exists(os.path.join(videos_path,entered_vid)):
                print("Successful add!")
                if entered_vid in self.entered_vids:
                    self.status_label_txt.set("Video already entered (Entered videos: " + str(self.entered_vids) + ")")
                else:
                    self.entered_vids.append(entered_vid)
                    self.status_label_txt.set("Entered videos: " + str(self.entered_vids))
            else:
                self.status_label_txt.set("File does not exist in " + videos_path)
        else:
            self.status_label_txt.set("Invalid format (must be a video)")
    
GUI()