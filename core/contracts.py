from typing import Protocol

class TrackerRule(Protocol):
    def add_viewer(self, viewer):
        pass

    def alert_viewers(self):
        pass

class ScreenRule(Protocol):
    def update_colors(self, raw_status, done_status):
        pass