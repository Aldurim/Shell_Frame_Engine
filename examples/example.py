from shell_frame_engine.shell_frame import *

def main():
    main_frame = Frame(20, 70)

    # Each Frame can render Text
    main_frame.text = "╔[ Main Frame ]"

    # Each Frame has an update routine that can be defined
    def main_frame_update(delta):
        main_frame.text = "╔[ Main Frame ]" +(main_frame.width - 15 - 12) * "═" +"[ FPS: " + str(main_frame.system_info.frame_rate) + " ]"
    main_frame.update = main_frame_update

    engine = Engine()
    engine.run(main_frame)