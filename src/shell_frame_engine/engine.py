import time
from pynput import keyboard, mouse
from dataclasses import dataclass
from collections import deque
from threading import Lock

@dataclass
class KeyEvent:
    key: str
    pressed: bool

@dataclass
class MouseEvent:
    x: int
    y: int
    button: str | None
    pressed: bool | None

@dataclass
class SystemInfo:
    frame_rate: int
    delta: float

class EventQueue:
    def __init__(self):
        self._events = deque()
        self._lock = Lock()

    def push(self, event):
        with self._lock:
            self._events.append(event)

    def drain(self):
        with self._lock:
            events = list(self._events)
            self._events.clear()
            return events

class Engine:
    
    def __init__(self):
        pass

    def run(self, main_frame):

        events = EventQueue()
        system_info = SystemInfo(0, 0.0)

        def on_press(key):
            events.push(KeyEvent(str(key), True))

        def on_release(key):
            events.push(KeyEvent(str(key), False))

        def on_click(x, y, button, pressed):
            events.push(MouseEvent(x, y, str(button), pressed))

        def on_move(x, y):
            events.push(MouseEvent(x, y, None, None))

        keyboard.Listener(on_press=on_press, on_release=on_release).start()
        mouse.Listener(on_move=on_move, on_click=on_click).start()

        target_fps = 60
        frame_duration = 1.0 / target_fps

        last_time = time.perf_counter()
        fps_timer = 0
        frames = 0
        frame_rate = 0

        while True:
            now = time.perf_counter()
            dt = now - last_time
            last_time = now

            # ---- YOUR UPDATE LOGIC ----
            main_frame.clear()
            for event in events.drain():
                main_frame.handle_event_recursive(event)

            main_frame.update_recursive(dt)
            main_frame.render()
            # ----------------------------

            frames += 1
            fps_timer += dt

            if fps_timer >= 1.0:
                frame_rate = frames
                frames = 0
                fps_timer = 0

            system_info.frame_rate = frame_rate
            system_info.delta = dt
            main_frame.system_info = system_info

            # ---- FRAME LIMIT ----
            sleep_time = frame_duration - (time.perf_counter() - now)
            if sleep_time > 0:
                time.sleep(sleep_time)