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


def get_controls_dir():
	return dir(controls)


def get_controls_draft_dir():
	return dir(controls.draft)


def get_available_controls():
	return get_controls_dir() + get_controls_draft_dir()


def control_has_enum(name):
	return name+"Enum" in get_available_controls()


def get_controls_attr(attr_name):
	if attr_name in get_controls_dir():
		return getattr(controls, attr_name)
	elif attr_name in get_controls_draft_dir():
		return getattr(controls.draft, attr_name)


def get_enum_options(some_control, as_attr=False):
	enum_name = some_control+"Enum"
	out_list = []
	if enum_name in get_available_controls():
		enum_control = get_controls_attr(enum_name)
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


def get_camera_control_type(name):

	if control_has_enum(name):
		return Type.ENUM

	control = get_controls_attr(name)
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

