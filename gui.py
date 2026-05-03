import tkinter as tk
from tkinter import messagebox
from weather_api import get_weather
from ai_api import get_ai_recommendation
from utils import format_weather_summary

class WeatherWiseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WeatherWise - AI Outfit & Activity Planner")
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(False, False)
        self.build_gui()

    def build_gui(self):
        bg_color = "#f0f4f8"
        title_font = ("Helvetica", 16, "bold")
        label_font = ("Helvetica", 11)
        text_font = ("Helvetica", 10)

        title_label = tk.Label(
            self.root,
            text="WeatherWise - AI Outfit & Activity Planner",
            font=title_font,
            bg="#2d6a9f",
            fg="white",
            padx=10,
            pady=10
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="ew")

        tk.Label(self.root, text="Enter City:", font=label_font, bg=bg_color).grid(
            row=1, column=0, padx=12, pady=6, sticky="w"
        )
        self.city_entry = tk.Entry(self.root, width=30, font=text_font)
        self.city_entry.grid(row=1, column=1, padx=12, pady=6, sticky="w")

        tk.Label(self.root, text="Select Day:", font=label_font, bg=bg_color).grid(
            row=2, column=0, padx=12, pady=6, sticky="w"
        )
        self.day_var = tk.StringVar(value="Today")
        day_frame = tk.Frame(self.root, bg=bg_color)
        day_frame.grid(row=2, column=1, padx=12, pady=6, sticky="w")

        tk.Radiobutton(day_frame, text="Today", variable=self.day_var, value="Today", bg=bg_color, font=text_font).pack(side="left", padx=4)
        tk.Radiobutton(day_frame, text="Tomorrow", variable=self.day_var, value="Tomorrow", bg=bg_color, font=text_font).pack(side="left", padx=4)

        button_frame = tk.Frame(self.root, bg=bg_color)
        button_frame.grid(row=3, column=0, columnspan=2, pady=8)

        tk.Button(
            button_frame,
            text="Get Recommendations",
            font=label_font,
            bg="#2d6a9f",
            fg="white",
            padx=10,
            pady=4,
            command=self.get_recommendations
        ).pack(side="left", padx=8)

        tk.Button(
            button_frame,
            text="Clear",
            font=label_font,
            bg="#e0e0e0",
            padx=10,
            pady=4,
            command=self.clear_fields
        ).pack(side="left", padx=8)

        self.weather_output = self.create_output_box("Weather Summary:", 4)
        self.outfit_output = self.create_output_box("Outfit Suggestion:", 5)
        self.activity_output = self.create_output_box("Activity Suggestions:", 6)
        self.explanation_output = self.create_output_box("Explanation:", 7)

        self.message_var = tk.StringVar(value="Ready.")
        tk.Label(
            self.root,
            textvariable=self.message_var,
            font=("Helvetica", 9, "italic"),
            bg="#dce8f5",
            anchor="w",
            padx=8
        ).grid(row=8, column=0, columnspan=2, sticky="ew", pady=(6, 4))

    def create_output_box(self, label_text, row):
        tk.Label(self.root, text=label_text, font=("Helvetica", 11), bg="#f0f4f8", anchor="w").grid(
            row=row, column=0, padx=12, pady=6, sticky="nw"
        )

        text_box = tk.Text(
            self.root,
            width=45,
            height=3,
            wrap="word",
            font=("Helvetica", 10),
            state="disabled",
            bg="white",
            relief="sunken"
        )
        text_box.grid(row=row, column=1, padx=12, pady=6, sticky="w")
        return text_box

    def set_output(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.config(state="disabled")

    def clear_outputs(self):
        self.set_output(self.weather_output, "")
        self.set_output(self.outfit_output, "")
        self.set_output(self.activity_output, "")
        self.set_output(self.explanation_output, "")

    def get_recommendations(self):
        city = self.city_entry.get().strip()
        day = self.day_var.get()

        if not city:
            messagebox.showerror("Input Error", "Please enter a city name.")
            return

        self.message_var.set("Fetching weather data...")
        self.root.update_idletasks()

        try:
            weather = get_weather(city, day)
            if weather is None:
                self.message_var.set("City not found.")
                messagebox.showerror("City Error", "City not found. Please check the spelling and try again.")
                return

            self.set_output(self.weather_output, format_weather_summary(weather))

            self.message_var.set("Getting AI recommendations...")
            self.root.update_idletasks()

            recommendation = get_ai_recommendation(weather, day)

            self.set_output(self.outfit_output, recommendation["outfit"])
            self.set_output(self.activity_output, recommendation["activities"])
            self.set_output(self.explanation_output, recommendation["explanation"])

            self.message_var.set(f"Done. Showing {day.lower()} recommendations for {city}.")

        except Exception as e:
            self.message_var.set("Error.")
            messagebox.showerror("Program Error", str(e))

    def clear_fields(self):
        self.city_entry.delete(0, tk.END)
        self.day_var.set("Today")
        self.clear_outputs()
        self.message_var.set("Ready.")