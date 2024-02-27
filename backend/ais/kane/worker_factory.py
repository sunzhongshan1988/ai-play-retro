from ais.kane.worker.battlecity_nes import BattleCityNesWorker

class Worker_Factory:
    """
    About Worker_Factory is a factory class to get the worker of the game
    """

    @staticmethod
    def get_worker(game_name: str):
        """ Get the worker of the game
        Args:
            game_name (str): The name of the game, it should be the same as the name of the game in the retro environment
        
        Returns:
            Worker: The worker of the game
        """
        workers = {
            "BattleCity-Nes": BattleCityNesWorker
        }

        try:
            return workers[game_name]()
        except KeyError:
            raise ValueError(f"Not found worker for game {game_name}")
