import asyncio
from ais.kane.kane import Kane


class RetroManager:
    def __init__(self):
        self.retro = {}

    def start_retro(self, ai, game_id, ws):
        if ai in self.retro:
            print(f"AI {ai} is already running.")
            return f"AI {ai} is already running."
        self.retro[ai] = Kane(game_id, ws)
        asyncio.create_task(self.retro[ai].run())

    def stop_retro(self, ai):
        if ai in self.retro:
            self.retro[ai].stop()
            del self.retro[ai]
        else:
            print(f"AI {ai} not run.")
            return f"AI {ai} not run."

retro_manager = RetroManager()