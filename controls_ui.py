import dearpygui.dearpygui as dpg
import camera_controls as cam_ctrl
from libcamera import controls

def apply_changes(sender, app_data, camera):
	print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {camera}")
	control_object = dict()
	for name in camera.camera_controls:
		print(f"Trying to get the following control from UI: {name}")
		try:			
			#item_configuration = dpg.get_item_configuration(name)
			control_type = dpg.get_item_user_data(name)#item_configuration['user_data']
			item_value = dpg.get_value(name)			
			
			print(control_type, item_value)
			
			if control_type == cam_ctrl.Type.ENUM:
				new_value = cam_ctrl.get_selected_enum_option(name, item_value)
				
			elif control_type in [cam_ctrl.Type.BOOL, cam_ctrl.Type.FLOAT, cam_ctrl.Type.INT]:
				new_value = item_value 
	
			control_object[name] = new_value

		except Exception as e:
			# This isn't implemented yet, so we simply pass.
			print(f"{name} not implemented yet, skipping ... Exception: {e}")
	
	camera.set_controls(control_object)
	print(control_object)

def create_controls_ui_for_camera(camera, parent_window):

	with parent_window:
		# values are as follows: [minimum, maximum, default]
		for name, values in camera.camera_controls.items():
			min_value, max_value, default_value = values
			print(f"Creating UI element for: {name} | min: {min_value} | max: {max_value} | default: {default_value}")
				
			control_type = cam_ctrl.get_camera_control_type(name)
			dpg.add_separator()
			dpg.add_text(name)

			if control_type == cam_ctrl.Type.ENUM:
				#create_enum_control_ui(name, parent_window, default_value)
				enum_options = cam_ctrl.get_enum_options(name)
				dpg.add_combo(tag=name, user_data=control_type, items=enum_options, default_value=enum_options[default_value])

			elif control_type == cam_ctrl.Type.BOOL:
				# checkbox
				default_value = False if default_value == None else default_value
				dpg.add_checkbox(tag=name, user_data=control_type, default_value=default_value)


			elif control_type == cam_ctrl.Type.FLOAT:
				default_value = 0 if default_value == None else default_value
				with dpg.group():
					float_source = dpg.add_input_float(tag=name, user_data=control_type, 
															default_value=float(default_value), min_value=float(min_value), max_value=float(max_value))
					dpg.add_slider_float(user_data=control_type,  
															default_value=float(default_value), clamped=True, min_value=float(min_value), max_value=float(max_value),
															source=float_source)

			
			elif control_type == cam_ctrl.Type.INT:
				default_value = 0 if default_value == None else default_value
				with dpg.group():
					int_source = dpg.add_input_int(tag=name, user_data=control_type,  
																default_value=int(default_value), min_value=int(min_value), max_value=int(max_value))
					dpg.add_slider_int(user_data=control_type,  
																default_value=int(default_value), clamped=True, min_value=int(min_value), max_value=int(max_value),
																source=int_source)

		# TODO: Make button larger!
		dpg.add_separator()	
		dpg.add_button(label="Apply changes", callback=apply_changes, user_data=camera)
# add a button at the bottom that will callback and set all the values
