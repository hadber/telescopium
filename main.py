import argparse
import numpy as np
import dearpygui.dearpygui as dpg
import io

dpg.create_context()

#def exit(_sender, _data):
#	dpg.stop_dearpygui()

w,h,d = 320, 240, 4
raw_data = np.ones((h,w,d), dtype=np.float32)

np.set_printoptions(threshold=np.inf)
#print(raw_data)

def update_raw_texture():
		global raw_data, picam2
		new_frame = picam2.capture_array()
		h2, w2, d2 = new_frame.shape
		raw_data[:h2, :w2] = new_frame[:,:] / 255
#		print(raw_data)

#if __name__ == "__main__":
parser = argparse.ArgumentParser(description="Transform your Raspberry Pi into a camera for taking pictures of the night sky")
parser.add_argument('guionly', 
					metavar='g', 
					type=bool, 
					default=False, 
					nargs='?', 
					help='Run telescopium with GUI only (no camera - for debug purposes without a Pi)')
args = parser.parse_args()
picam2 = None

if not args.guionly:
	from picamera2 import Picamera2
	picam2 = Picamera2()
	picam2.configure(picam2.create_preview_configuration({"size": (320, 240)}))
	picam2.start()

	cam_data =	picam2.capture_array()
	print(np.shape(cam_data))

with dpg.texture_registry(show=False):
	dpg.add_raw_texture(width=320, height=240, default_value=raw_data, format=dpg.mvFormat_Float_rgba, tag="Camera texture")

with dpg.window(tag="Camera window") as cam_window:
	dpg.add_image(texture_tag="Camera texture", tag="Camera image", show=False)
	dpg.add_loading_indicator(tag="Loading", radius=30)

dpg.create_viewport(title='telescopium')
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Camera window", True)
dpg.toggle_viewport_fullscreen()

# this is called once we have the size of full screen
def init_custom_data():
	h = dpg.get_viewport_client_height()
	w = dpg.get_viewport_client_width()
#	update_texture_data(w, h)
	dpg.configure_item("Camera texture", width=w, height=h)
	dpg.configure_item("Camera image", width=w, height=h, show=True)
	dpg.delete_item("Loading")


# Style


# remove the border so that the camera feed is full screen
with dpg.theme() as no_padding:
	with dpg.theme_component():
		dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0, category=dpg.mvThemeCat_Core)
dpg.bind_item_theme(cam_window, no_padding)
#dpg.bind_theme(global_theme)

# Increase font size, this will make things blurry
# However, it is needed in order to be able to click
# And properly see stuff on the tiny RPi screen
# TODO: Add a new, larger font?
dpg.set_global_font_scale(2)


#Style end

if not args.guionly:
		import controls_ui as cam_ui
	 
		controls_window = dpg.window(tag="Controls window", label="Controls", width=450, height=600)
		cam_ui.create_controls_ui_for_camera(picam2, controls_window)

# wait 10 frames for the fullscreen to be fully setup (a bit hacky)
dpg.set_frame_callback(10, init_custom_data)

# main loop
while dpg.is_dearpygui_running():

	if not args.guionly:
		update_raw_texture()

	dpg.render_dearpygui_frame()


dpg.destroy_context()

# TODO:
# - view camera real-time x
# - take a photo
# - modify camera settings (iso, etc) x
# - save camera presets
# - view taken photos

# sensor modes RPi HQ Cam
"""
[{'bit_depth': 10,
	'crop_limits': (696, 528, 2664, 1980),
	'exposure_limits': (31, 2147483647, None),
	'format': SRGGB10_CSI2P,
	'fps': 120.05,
	'size': (1332, 990),
	'unpacked': 'SRGGB10'},
 {'bit_depth': 12,
	'crop_limits': (0, 440, 4056, 2160),
	'exposure_limits': (60, 667244877, None),
	'format': SRGGB12_CSI2P,
	'fps': 50.03,
	'size': (2028, 1080),
	'unpacked': 'SRGGB12'},
 {'bit_depth': 12,
	'crop_limits': (0, 0, 4056, 3040),
	'exposure_limits': (60, 674181621, None),
	'format': SRGGB12_CSI2P,
	'fps': 40.01,
	'size': (2028, 1520),
	'unpacked': 'SRGGB12'},
 {'bit_depth': 12,
	'crop_limits': (0, 0, 4056, 3040),
	'exposure_limits': (114, 674191602, None),
	'format': SRGGB12_CSI2P,
	'fps': 10.0,
	'size': (4056, 3040),
	'unpacked': 'SRGGB12'}]
"""
