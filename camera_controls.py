from picamera2 import Picamera2
from libcamera import controls


# loop through all available camera controls

def get_available_controls():
    return dir(controls)

def control_has_enum(some_control):
    name = some_control.name
    return name+"Enum" in get_available_controls()

def get_modifiable_controls():
    # TODO: find better way to identify available controls
    control_class = type(controls.Lux)
    controls_with_enum = []
    controls_with_defaults = []
    for control_as_string in get_available_controls():
        control = getattr(controls, control_as_string)
        # if this is a valid control
        if type(control) == control_class:
            if control_has_enum(control):
                controls_with_enum.append(control_as_string)
            else:
                controls_with_defaults.append(control_as_string)

    return controls_with_enum, controls_with_defaults

def get_enum_options(some_control):
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
                out_list.append(option_name)
            
    return out_list
    
