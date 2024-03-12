import dearpygui.dearpygui as dpg
import camera_controls as camc
from libcamera import controls

enum_list, defaults_list = camc.get_all_modifiable_controls()

def create_enum_control_ui(name, some_parent, default_id):
	enum_options = camc.get_enum_options(name)
	dpg.add_combo(items=enum_options, default_value=enum_options[default_id], label=name, parent=some_parent)

def create_controls_ui_for_camera(camera, parent_window):

	# values are as follows: [minimum, maximum, default]
	for name, values in camera.camera_controls.items():
		min_value, max_value, default_value = values
		print(f"Creating UI element for: {name}")
		control_type = camc.get_camera_control_type(name)

		if control_type == camc.Type.ENUM:
			create_enum_control_ui(name, parent_window, default_value)

		elif control_type == camc.Type.BOOL:
			pass
		elif control_type == camc.Type.FLOAT:
			print(min_value, max_value, default_value)
			default_value = 0 if default_value == None else default_value
			dpg.add_slider_float(label=name, user_data=control_type, parent=parent_window, 
														default_value=float(default_value), clamped=True, min_value=float(min_value), max_value=float(max_value))
