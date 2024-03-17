from picamera2 import Picamera2
from libcamera import controls, ControlType
from enum import Enum

class Type(Enum):
	BOOL = 0
	ENUM = 1
	FLOAT = 2	
	INT = 3
	RECT = 4
	NONE = 5

# loop through all available camera controls
def get_available_controls():
	return dir(controls)

def control_has_enum(name):
	return name+"Enum" in get_available_controls()

def get_all_modifiable_controls():
	# TODO: find better way to identify available controls
	control_class = type(controls.Lux)
	controls_with_enum = []
	controls_with_defaults = []
	for control_as_string in get_available_controls():
		control = getattr(controls, control_as_string)
		# if this is a valid control
		if type(control) == control_class:
			if control_has_enum(control.name):
				controls_with_enum.append(control_as_string)
			else:
				controls_with_defaults.append(control_as_string)

	return controls_with_enum, controls_with_defaults

def get_enum_options(some_control, as_attr=False):
	enum_name = some_control+"Enum"
	out_list = []
	if enum_name in get_available_controls():
		enum_control = getattr(controls, enum_name)
		enum_options_list = dir(enum_control)
		_type = type(getattr(enum_control, enum_options_list[0]))
	   
		# because we can't iterate through controls, we have to
		# iterate through strings and grab the attribute
		for option_name in enum_options_list:
			option_val = getattr(enum_control, option_name)
			if type(option_val) == _type:
				if(as_attr):
					out_list.append(option_val)
				else:
					out_list.append(option_name)
			
	return out_list


def get_selected_enum_option(some_control, enum_option):
	# TODO: please redo this
	enums_str =	get_enum_options(some_control)
	enum_pos = enums_str.index(enum_option)
	return get_enum_options(some_control, True)[enum_pos]

#return get_enum_options[enum_option]

def get_camera_control_type(name):
	
	# there is currently a problem with NoiseReductionMode 
	# which is actually set from draft.NoiseReductionModeEnum
	# TODO: add an exception for it or simply ignore it.
	if not name in get_available_controls():
		return Type.NONE

	if control_has_enum(name):
		return Type.ENUM

	control = getattr(controls, name)
	ctype = control.type

	if ctype == ControlType.Bool:
		return Type.BOOL
	elif ctype ==  ControlType.Float:
		return Type.FLOAT
	elif ctype in [ControlType.Integer32, ControlType.Integer64]:
		return Type.INT
	elif ctype ==  ControlType.Rectangle:
		return Type.RECT
	
	return Type.NONE

#def get_camera_controls_list(camera):
#	camera.camera_controls
