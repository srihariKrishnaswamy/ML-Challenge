import tkinter as tk
import os
from PIL import ImageTk, Image
import subprocess
import signal
import shutil
import sys
from threading import Thread
from queue import Empty, Queue
import datetime

image_path = os.path.join(os.path.dirname(__file__), "./assets/NewBanner.jpg")
min_width = 600
min_height = 600
videos_path = os.path.join(os.path.dirname(__file__), "videos/")
def_output_folder = "out"

#code for terminal streaming adapted from https://stackoverflow.com/questions/665566/redirect-command-line-results-to-a-tkinter-gui
def iter_except(function, exception):
    try:
        while True:
            yield function()
    except exception:
        return

class GUI:
    def __init__(self):
        #non tk vars
        self.possible_vids = self.determine_possible_videos()
        self.entered_vids = []
        self.detection_logging_process = None
        #tk vars
        self.model_name = "seventh.pt"
        self.root = tk.Tk()
        self.root.title("SeaScout Organisim Detector")
        self.root.geometry(str(min_width) + "x" + str(min_height))
        self.root.minsize(min_width, min_height)
        self.root.resizable(False, True)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        #cmd remdering stuff
        self.cmd_output_buffer = Queue(maxsize=1024)

        parent_frame = tk.Frame(self.root)
        parent_frame.grid(column=0, row=0, sticky="news")
        parent_frame.columnconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(4, weight=1)

        img = Image.open(image_path)
        img.thumbnail((min_width, min_height))
        photo_img = ImageTk.PhotoImage(img)
        img_label = tk.Label(parent_frame, image=photo_img)
        img_label.grid(row=0, column=0)

        topframe = tk.LabelFrame(parent_frame,
                                 text="Select Input Videos",
                                 padx=30,
                                 pady=10)
        topframe.columnconfigure(1, minsize=80)
        topframe.grid(row=1, column=0, sticky="ew")

        video_label = tk.Label(
            topframe,
            text="Enter video files to process (must be in appropriate folder)"
        )
        video_label.grid(row=0, column=0, sticky="w")

        self.names_entry = tk.Entry(topframe, width=40)
        self.names_entry.grid(row=1, column=0, sticky="w")

        enter_name_button = tk.Button(topframe,
                                      text="Enter Video",
                                      command=self.enter_video)
        enter_name_button.grid(row=1, column=1, sticky="e", padx=(20, 10))

        possible_vids_label = tk.Label(topframe,
                                       font=("TkDefaultFont", 12),
                                       text="Options: " +
                                       str(self.possible_vids),
                                       wraplength=350)
        possible_vids_label.grid(row=2, column=0, sticky="w")

        self.status_label_txt = tk.StringVar(value="No videos entered")
        self.status_label = tk.Label(topframe,
                                     font=("TkDefaultFont", 12),
                                     textvariable=self.status_label_txt,
                                     wraplength=350)
        self.status_label.grid(row=3, column=0, sticky="w")

        secondframe = tk.LabelFrame(parent_frame,
                                    text="Output",
                                    padx=15,
                                    pady=15)
        secondframe.grid(row=2, column=0, sticky="ew")

        self.output_label_txt = tk.StringVar(
            value="Output video(s) & spreadsheet will be at: " +
            self.determine_output_path())
        self.output_label = tk.Label(secondframe,
                                     textvariable=self.output_label_txt,
                                     wraplength=550)
        self.output_label.pack()

        thirdframe = tk.LabelFrame(parent_frame,
                                   text="ML-Configuration",
                                   padx=10,
                                   pady=5)
        thirdframe.grid(row=3, column=0, sticky="ew")

        self.model_location_txt = tk.StringVar(value="Model location: " + os.path.join(os.path.dirname(__file__), "iterations/" + self.model_name))
        model_location = tk.Label(
            thirdframe,
            textvariable=self.model_location_txt,
            wraplength=460)
        model_location.grid(row=0, column=0, sticky="ew")

        self.new_model_entry = tk.Entry(thirdframe, width=40)
        self.new_model_entry.grid(row=1, column=0, sticky="ew")

        self.new_model_button = tk.Button(thirdframe, text="Enter New Model Name", command=self.handle_model_input)
        self.new_model_button.grid(row=1, column=1, sticky="ew")

        # SHOWING STDOUT ON TKINTER
        fourthframe = tk.LabelFrame(parent_frame, pady=10)
        fourthframe.grid(row=4, column=0, sticky="news")
        fourthframe.columnconfigure(0, weight=1)
        fourthframe.rowconfigure(0, weight=1)
        parent_frame.rowconfigure(4, weight=1)

        # self.cmd_label = tk.Label(fourthframe, text="   ", font=(None, 200))
        # self.cmd_label.pack(ipadx=4, padx=4, ipady=4, pady=4, fill='both')

        self.cmd_output_area = tk.Text(fourthframe, bd=0, height=6)
        self.cmd_output_area.grid(column=1, row=1, sticky="news")
        self.cmd_output_area.tag_config("errorstring", foreground="#CC0000")
        self.cmd_output_area.tag_config("infostring", foreground="#008800")

        self.update(self.cmd_output_buffer)

        fifthframe = tk.LabelFrame(parent_frame, pady=5)
        fifthframe.grid(row=5, column=0, sticky="news")

        self.start_inference_button = tk.Button(fifthframe,
                                    text="Start Inference",
                                    command=self.start_inference)
        self.start_inference_button.pack(expand=True, fill='x')

        kill_inference = tk.Button(fifthframe,
                                   text="Kill Running Inference(s)",
                                   command=self.kill_inference)
        kill_inference.pack(expand=True, fill='x')

        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.mainloop()

    def handle_model_input(self):
        new_model = self.new_model_entry.get()
        if new_model != "" and os.path.exists(os.path.join("./iterations", new_model)):
            self.model_name = new_model
            self.model_location_txt.set("Model location: " + os.path.join(os.path.dirname(__file__), "iterations/" + self.model_name))
        else:
            self.model_location_txt.set("Model does not exist with name: " + str(new_model) + ", still using " + str(self.model_name))
        self.new_model_entry.delete(0, tk.END)

    def start_inference(self):
        if self.detection_logging_process == None and len(self.entered_vids) > 0:
            self.status_label_txt.set(
                "Videos being processed")
            args_list = ["python", "master_detect_data.py", "--model", "--videos"]
            args_list.insert(3, self.model_name)
            args_list.extend(self.entered_vids)
            print(args_list)
            self.entered_vids = []
            self.detection_logging_process = subprocess.Popen(
                args_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
            reader_thread = Thread(target=self.cmd_reader_thread, args=[self.cmd_output_buffer])
            reader_thread.daemon = True # Flags as a daemon thread, so it will close at shutdown
            reader_thread.start()
            self.output_label_txt.set(self.determine_output_path())
            self.wipe_yolo_output()

    def kill_inference(self):
        if self.detection_logging_process != None and self.detection_logging_process.poll() is None:
            pid = self.detection_logging_process.pid
            os.killpg(os.getpgid(pid), signal.SIGKILL)
            self.status_label_txt.set("Inference killed early")
            self.wipe_yolo_output()
            self.detection_logging_process = None
            self.add_cmd_output("Inference killed by user: No excel file or resulting videos generated")

    def determine_output_path(self):
        if os.path.exists(os.path.join(os.path.dirname(__file__), "output")):
            output_list = os.listdir(
                os.path.join(os.path.dirname(__file__), "output/"))
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
                return str(
                    os.path.join(os.path.dirname(__file__), "output/out1"))
            else:
                return str(
                    os.path.join(os.path.dirname(__file__), "output/" +
                                 def_output_folder + str(max)) + "/")
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
            if os.path.exists(os.path.join(videos_path, entered_vid)):
                print("Successful add!")
                if entered_vid in self.entered_vids:
                    self.status_label_txt.set(
                        "Video already entered (Entered videos: " +
                        str(self.entered_vids) + ")")
                else:
                    self.entered_vids.append(entered_vid)
                    self.status_label_txt.set("Entered videos: " +
                                              str(self.entered_vids))
            else:
                self.status_label_txt.set("File does not exist in " +
                                          videos_path)
        else:
            self.status_label_txt.set("Invalid format (must be a video)")

    def wipe_yolo_output(self):
        if os.path.exists("runs"):
            shutil.rmtree("runs")
        if os.path.exists("sourceVid.txt"):
            os.remove("sourceVid.txt")
        if os.path.exists("detections.xlsx"):
            os.remove("detections.xlsx")
        if os.path.exists("output_path_log.txt"):
            os.remove("output_path_log.txt")

    def quit(self):
        self.kill_inference()
        self.root.destroy()

    # Adapted from https://stackoverflow.com/questions/665566/redirect-command-line-results-to-a-tkinter-gui
    def cmd_reader_thread(self, cmd_output_buffer: Queue):
        "Reads the command output while the inference subprocess is running."
        try:
            with self.detection_logging_process.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    cmd_output_buffer.put(line)
        finally:
            cmd_output_buffer.put(None)  # signal that the process is completed
    
    # Adapted from last year's deepsea-detector
    def add_cmd_output(self, str, tags=None):
        """Add a line of text to the cmd output. If tags is None then
        self.get_default_tags will be used to assign tags to the line"""
        self.cmd_output_area.insert(tk.INSERT, str, tags)
        self.cmd_output_area.see(tk.END)

    # Adapted from last year's deepsea-detector
    def update(self, cmd_output_buffer: Queue):
        "Update loop for the InferenceUI."

        if self.detection_logging_process is not None:  # We are currently running inference
            # Dump buffer into the cmd output text area
            for line in iter_except(cmd_output_buffer.get_nowait, Empty):
                if line:
                    # Update command output with new line
                    self.add_cmd_output(line)
            
            # Check if process finished, if so
            returncode = self.detection_logging_process.poll()
            if returncode is not None:
                if returncode == 0:
                    self.add_cmd_output("\nInference job finished successfully \n")
                if self.detection_logging_process.poll() > 0:
                    self.add_cmd_output("\nERROR: Inference job encountered an error. \n")
            
                self.detection_logging_process = None

        # Disable Run Inference button if there's an existing process running. - should be unnecesary now
        # if self.detection_logging_process:
        #     self.start_inference_button["state"]="disabled"
        # else:
        #     self.start_inference_button["state"]="enabled"

        # Run next update
        self.root.after(40, self.update, cmd_output_buffer)
    

GUI()