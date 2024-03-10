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
                controls_with_enum.append(control)
            else:
                controls_with_defaults.append(control)

    
    return controls_with_enum, controls_with_defaults
