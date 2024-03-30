import numpy as np
import dearpygui.dearpygui as dpg
import controls_ui as cam_ui
from picamera2 import Picamera2
from cv2 import cvtColor, COLOR_YUV420p2RGBA
from time import strftime
#from picamera2.converters import YUV420_to_RGB

# TODO:
# - view camera real-time x
# - take a photo
# - modify camera settings (iso, etc) x
# - make the camera window zoomable (by using a node editor?)
# - save camera presets
# - view taken photos

w,h,d = 320, 240, 4
raw_data = np.ones((h,w,d), dtype=np.float32)
#np.set_printoptions(threshold=np.inf)
picam2 = None


def exit(_sender, _data):
	dpg.stop_dearpygui()


def update_raw_texture():
		global raw_data, picam2
		lores_frame = picam2.capture_array("lores")
		new_frame = cvtColor(lores_frame, COLOR_YUV420p2RGBA)
		h2, w2, d2 = new_frame.shape
		raw_data[:h2, :w2] = new_frame[:,:] / 255


def setup_camera():
	global picam2
	picam2 = Picamera2()
	still_config = picam2.create_still_configuration(lores={"size": (320, 240)})
#	picam2.align_configuration(still_config)
	picam2.configure(still_config)
	picam2.start()

	update_raw_texture()


def setup_theme():
	# remove the border so that the camera feed is full screen
	with dpg.theme() as no_padding:
		with dpg.theme_component():
			dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0, category=dpg.mvThemeCat_Core)
	dpg.bind_item_theme(cam_window, no_padding)

	# Increase font size, this will make things blurry
	# However, it is needed in order to be able to click
	# And properly see stuff on the tiny RPi screen
	# TODO: Add a new, larger font? (scaling is blurry)
	dpg.set_global_font_scale(2)


# this is called once we have the size of full screen
def init_custom_data():
	h = dpg.get_viewport_client_height()
	w = dpg.get_viewport_client_width()
	dpg.configure_item("Camera texture", width=w, height=h)
	dpg.configure_item("Camera image", width=w, height=h, show=True)
	dpg.delete_item("Loading")

# setting up DearPyGui
dpg.create_context()
dpg.create_viewport(title='telescopium')
dpg.setup_dearpygui()

with dpg.texture_registry(show=False):
	dpg.add_raw_texture(width=320, height=240, default_value=raw_data, format=dpg.mvFormat_Float_rgba, tag="Camera texture")

# Setup camera window 
with dpg.window(tag="Camera window") as cam_window:
	dpg.add_image(texture_tag="Camera texture", tag="Camera image", show=False)
	dpg.add_loading_indicator(tag="Loading", radius=30)

dpg.show_viewport()
dpg.set_primary_window("Camera window", True)
dpg.toggle_viewport_fullscreen()

setup_theme()

setup_camera()
assert(not picam2 is None)
# Camera control window and other camera-related UI
controls_window = dpg.window(tag="Controls window", label="Controls", width=450, height=600)
cam_ui.create_controls_ui_for_camera(picam2, controls_window)

def take_a_picture():
	filename = strftime("images/" + "%Y%m%d-%H%M%S") + '.png'
	picam2.capture_file(filename, format="png")

with dpg.window(tag="Capture window", label="Capture") as capture_window:
	dpg.add_button(label="Take a picture", callback=take_a_picture)

# wait 10 frames for the fullscreen to be fully setup before grabbing size (a bit hacky)
dpg.set_frame_callback(10, init_custom_data)

# main loop
while dpg.is_dearpygui_running():

	update_raw_texture()
	dpg.render_dearpygui_frame()

dpg.destroy_context()


