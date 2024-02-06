import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import array

dpg.create_context()

#def exit(_sender, _data):
#    dpg.stop_dearpygui()

texture_data = []
raw_data = []
def update_texture_data(width, height):
    for i in range(0, width*height):
        texture_data.append(128 / 255)
        texture_data.append(0)
        texture_data.append(255 / 255)
        texture_data.append(255 / 255)
    raw_data = array.array('f', texture_data)

update_texture_data(100, 100)

with dpg.texture_registry(show=False):
    dpg.add_raw_texture(width=100, height=100, default_value=raw_data, format=dpg.mvFormat_Float_rgba, tag="Camera texture")

with dpg.window(tag="Camera window"):
    dpg.add_image(texture_tag="Camera texture", tag="Camera image", show=False)
    dpg.add_loading_indicator(tag="Loading", radius=30)

dpg.create_viewport(title='telescopium')
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Camera window", True)
dpg.toggle_viewport_fullscreen()

def init_custom_data():
    h = dpg.get_viewport_client_height()
    w = dpg.get_viewport_client_width()
#    print(h,w)
    update_texture_data(w, h)
    dpg.configure_item("Camera texture", width=w, height=h)
    dpg.configure_item("Camera image", width=w, height=h, show=True)
    dpg.delete_item("Loading")

# remove the border so that the camera feed is full screen
with dpg.theme() as global_theme:
    with dpg.theme_component():
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0, category=dpg.mvThemeCat_Core)
dpg.bind_theme(global_theme)

# wait 10 frames for the fullscreen to be fully setup
dpg.set_frame_callback(10, init_custom_data) 
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()

# TODO:
# - view camera real-time
# - take a photo
# - modify camera settings (iso, etc)
# - save camera presets
# - view taken photos

