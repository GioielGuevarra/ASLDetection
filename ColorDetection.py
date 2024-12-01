import cv2
import numpy as np
import pandas as pd
import pickle
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from sklearn.neighbors import KNeighborsClassifier

# Load the color dataset
df = pd.read_csv('colors.csv')  # Assuming your CSV contains columns: red, green, blue, name

# Prepare the data (RGB values as features, Color Name as label)
X = df[['red', 'green', 'blue']].values
y = df['name'].values

# Train a KNN model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

# Save the model
with open('color_model.pkl', 'wb') as f:
    pickle.dump(knn, f)

# Load the model
with open('color_model.pkl', 'rb') as f:
    knn = pickle.load(f)

# Initialize webcam
cap = cv2.VideoCapture(0)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Load custom fonts
        self.font_vt323_title = ctk.CTkFont(family="VT323", size=42, weight="bold")  # Ensure the font is installed on your system
        self.font_vt323 = ctk.CTkFont(family="VT323", size=24, weight="bold")  # Ensure the font is installed on your system
        self.font_matolha = ctk.CTkFont(family="Matolha", size=16)  # Ensure the font is installed on your system

        # configure window
        self.title("8Bit Color Detection")
        self.geometry("1300x800")
        self.configure(fg_color="#000000")  # Change the background color of the window
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # Create a frame for the title: Row 0,1
        self.title_frame = ctk.CTkFrame(self, width=800, height=50, fg_color="#fdbc44", border_color="black", border_width=1, corner_radius=0)
        self.title_frame.grid(row=0, column=0, rowspan=2, columnspan=2, padx=2, pady=2, sticky="nsew")

        self.title_label = ctk.CTkLabel(self.title_frame, text="COLOR DETECTION?!?! COLOR DETECTION?!?! COLOR DETECTION?!?! COLOR DETECTION?!?!", font=self.font_vt323_title, fg_color="transparent", text_color="black")
        self.title_label.pack(fill="both", expand=True)

        # Create a frame for the webcam: Row 2,3,4
        self.webcam_frame = ctk.CTkFrame(self, width=800, height=400, fg_color="#fefefa", border_color="black", border_width=1, corner_radius=0)  # Change the background color of the frame
        self.webcam_frame.grid(row=2, column=0, rowspan=3, columnspan=2, padx=1, pady=0, sticky="nsew")

        # Create a label to display the webcam feed
        self.webcam_label = ctk.CTkLabel(self.webcam_frame, text="", width=780, height=340)  # Adjusted size to show border
        self.webcam_label.pack(padx=10, pady=10, fill="both", expand=True)

        # Create a frame for the color name and place it above the picked color screen: Row 0,1
        self.color_name_frame = ctk.CTkFrame(self, width=400, height=50, fg_color="#fefefa", border_color="black", border_width=1, corner_radius=0)  # Change the background color of the frame
        self.color_name_frame.grid(row=0, rowspan=2, column=2, padx=1, pady=2, sticky="nsew")

        self.color_name_label = ctk.CTkLabel(self.color_name_frame, text="", font=self.font_vt323, fg_color="transparent", text_color="black")  # Use VT323 font
        self.color_name_label.pack(fill="both", expand=True)

        # Create a frame for the picked color: Row 2
        self.picked_color_frame = ctk.CTkFrame(self, width=400, height=200, fg_color="#fefefa", border_color="black", border_width=1, corner_radius=0)  # Change the background color of the frame
        self.picked_color_frame.grid(row=2, column=2, padx=0, pady=0, sticky="nsew")

        # Create a label to display the picked color
        self.picked_color_label = ctk.CTkLabel(self.picked_color_frame, text="", width=380, height=180)  # Adjusted size to show border
        self.picked_color_label.pack(padx=10, pady=10, fill="both", expand=True)

        # Create a frame for the hex code: Row 3
        self.hex_code_frame = ctk.CTkFrame(self, width=400, height=100, fg_color="#fefefa", border_color="black", border_width=1, corner_radius=0)  # Change the background color of the frame
        self.hex_code_frame.grid(row=3, column=2, padx=0, pady=1, sticky="nsew")

        self.hex_code_label = ctk.CTkLabel(self.hex_code_frame, text="", font=self.font_matolha, text_color="black")  # Use Matolha font
        self.hex_code_label.place(relx=0.5, rely=0.5, anchor="center")

        # Create a frame for the RGB value: Row 4
        self.rgb_value_frame = ctk.CTkFrame(self, width=400, height=100, fg_color="#fefefa", border_color="black", border_width=1, corner_radius=0)  # Change the background color of the frame
        self.rgb_value_frame.grid(row=4, column=2, padx=0, pady=1, sticky="nsew")

        self.rgb_value_label = ctk.CTkLabel(self.rgb_value_frame, text="", font=self.font_matolha, text_color="black")  # Use Matolha font
        self.rgb_value_label.place(relx=0.5, rely=0.5, anchor="center")

        # Create a pause button
        self.pause_button = ctk.CTkButton(self, text="''PAUSE!''", command=self.toggle_pause, width=400, height=100, font=self.font_vt323_title, text_color="black", fg_color="#fdbc44", hover_color="#dfa92e", corner_radius=0, border_color="black", border_width=2)  # Use VT323 font
        self.pause_button.grid(row=5, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")

        self.paused = False

        # Create an exit button
        self.exit_button = ctk.CTkButton(self, text="->EXIT?!", command=self.exit_program, width=400, height=100, font=self.font_vt323_title, text_color="white", fg_color="#9D0910", hover_color="#780000", corner_radius=0, border_color="black", border_width=2)  # Use VT323 font
        self.exit_button.grid(row=5, column=2, padx=0, pady=0, sticky="nsew")

        self.paused = False

        # Bind the spacebar key to the toggle_pause function
        self.bind("<space>", self.toggle_pause_event)

        self.update_frame()

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.configure(text="''RESUME>''" if self.paused else "''PAUSE!''")

    def toggle_pause_event(self, event):
        self.toggle_pause()

    def update_frame(self):
        if not self.paused:
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, _ = frame_rgb.shape
                center_x, center_y = width // 2, height // 2
                center_rgb = frame_rgb[center_y, center_x]
                r, g, b = int(center_rgb[0]), int(center_rgb[1]), int(center_rgb[2])
                color_name = knn.predict([[r, g, b]])[0]
                hex_code = '#{:02x}{:02x}{:02x}'.format(r, g, b)

                # Update the labels
                self.color_name_label.configure(text=f"'{color_name}'")
                self.hex_code_label.configure(text=f"Hex Code: {hex_code}")
                self.rgb_value_label.configure(text=f"RGB Value: [{r}, {g}, {b}]")

                # Update the picked color label
                self.picked_color_label.configure(bg_color=hex_code)

                # Draw a green cross in the center of the frame
                cv2.line(frame_rgb, (center_x - 10, center_y), (center_x + 10, center_y), (0, 255, 0), 1)
                cv2.line(frame_rgb, (center_x, center_y - 10), (center_x, center_y + 10), (0, 255, 0), 1)

                # Convert the frame to ImageTk format
                img = Image.fromarray(frame_rgb)
                imgtk = ctk.CTkImage(light_image=img, size=(800, 600))
                self.webcam_label.imgtk = imgtk
                self.webcam_label.configure(image=imgtk)

        self.after(10, self.update_frame)

    def exit_program(self):
        cap.release()
        self.destroy()

# Run the application
app = App()
app.mainloop()