import matplotlib.pyplot as plt
import numpy as np
import time
import json
import os
from matplotlib.widgets import Button

class FreehandPolygonDemo:
    def __init__(self):
        self.image = None
        self.fig, self.ax = None, None
        self.polygon = []
        self.timestamps = {
            "first_click": None,
            "save_clicked": None
        }

    def load_image(self, image_path):
        self.image = plt.imread(image_path)
        self.show()

    def show(self):
        self.fig, self.ax = plt.subplots()
        self.ax.imshow(self.image)
        self.ax.axis('off')
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        
        save_btn_ax = self.fig.add_axes([0.81, 0.05, 0.1, 0.075])
        save_button = Button(save_btn_ax, 'Save')
        save_button.on_clicked(self.on_save_clicked)
        
        plt.show()

    def on_press(self, event):
        if event.inaxes != self.ax: return  # Ignore clicks outside the axes
        if self.timestamps["first_click"] is None:
            self.timestamps["first_click"] = time.time()
        self.polygon.append((event.xdata, event.ydata))
        self.ax.plot(event.xdata, event.ydata, 'ro-')  # Mark the point
        self.fig.canvas.draw()

    def on_release(self, event):
        if len(self.polygon) > 1:
            x, y = zip(*self.polygon)
            self.ax.plot(x, y, 'r-')  # Draw lines between points
            self.fig.canvas.draw()

    def on_save_clicked(self, event):
        self.timestamps["save_clicked"] = time.time()
        self.save_data()

    def save_data(self):
        file_path = os.path.join(os.getcwd(), "polygon_data.json")
        data = {
            "polygon": self.polygon,
            "timestamps": self.timestamps
        }
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {file_path}")

# Example usage:
demo = FreehandPolygonDemo()
demo.load_image("path_to_your_image.jpg")
