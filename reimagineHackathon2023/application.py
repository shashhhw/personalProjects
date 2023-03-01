import pickle
import customtkinter
import os

from tkintermapview import TkinterMapView

class App(customtkinter.CTk):

    APP_NAME = "CHIPMaps"
    WIDTH = 800
    HEIGHT = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=MAROON)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0, fg_color=GOLD)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============
        self.frame_left.grid_rowconfigure(6, weight=1)
        
        self.introduction = customtkinter.CTkLabel(self.frame_left, text="Welcome to\nChipMaps!", text_color = GOLD, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.introduction.grid(row=0, column=0, padx=0, pady=(10, 10))

        self.current = customtkinter.CTkLabel(self.frame_left, text="Current Location", text_color = GOLD, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.current.grid(row=1, column=0, padx=0, pady=(0, 0))
        
        # Origin Location
        origin = customtkinter.StringVar()

        self.origin_options = customtkinter.CTkComboBox(self.frame_left, values=["Engineering Building", "Northwest Apartments"], variable=self.origin)
        self.origin_options.grid(row=2, column=0, padx=0, pady=(10, 10))
        self.origin_options.bind("<<ComboboxSelected>>", self.on_select_origin)

        self.origin_location_button = customtkinter.CTkButton(self.frame_left, text="Select Above Option", text_color = MAROON, fg_color = GOLD, command=self.get_selected_origin)
        self.origin_location_button.grid(row=3, column=0, padx=0, pady=(10, 10))

        # Destination Location
        destination = customtkinter.StringVar()

        self.destination_options = customtkinter.CTkComboBox(self.frame_left, values=["Engineering Building", "Northwest Apartments"], variable=self.destination)
        self.destination_options.grid(row=4, column=0, padx=0, pady=(10, 10))
        self.destination_options.bind("<<ComboboxSelected>>", self.on_select_origin)

        self.destination_location_button = customtkinter.CTkButton(self.frame_left, text="Select Above Option", text_color = MAROON, fg_color = GOLD, command=self.get_selected_destination)
        self.destination_location_button.grid(row=5, column=0, padx=0, pady=(10, 10))

    def on_select_origin(self):

        return self.origin_location.set()

    def get_selected_origin(self):

        return self.origin_location.get()

    def on_select_destination(self):

        return self.destination_location.set()

    def get_selected_destination(self):

        return self.destination_location.get()
    

    def start(self):
        self.mainloop()

def main():

    global MAROON, GOLD

    MAROON = "#6A0032"
    GOLD = "#FFC82E"

    # Clear terminal
    os.system("clear")

    # Get the stored file information form backend
    with open('backend_file_information.pickle', 'rb') as handle:
        backendFile = pickle.load(handle)
    
    origin = backendFile["Origin"]
    destination = backendFile["Destination"]
    instructions = backendFile["Instructions"]
    path = backendFile["Paths"]
    locationsOnMap = backendFile["Path Locations"]

    # Create a widget using customtkinter
    customtkinter.set_default_color_theme("blue")

    # Initialize 
    ChipMap = App()


    ChipMap.start()


if __name__ == "__main__":
    main()