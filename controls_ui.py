import dearpygui.dearpygui as dpg
import camera_controls as camc

enum_list, defaults_list = camc.get_modifiable_controls()

def create_enum_controls_ui_elements(some_parent):
    for enum in enum_list:
        enum_options = camc.get_enum_options(enum)
        dpg.add_combo(items=enum_options, label=enum, parent=some_parent)


def create_controls_window(root):
    with dpg.window(tag="Controls window", parent=root) as controls_window:
        create_enum_controls_ui_elements(controls_window)


def add_camera_control_ui_element(some_parent):
    return dpg.add_slider_int(label="This is a test", parent=some_parent)
