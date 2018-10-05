"""
experiment.py
"""
from datetime import datetime
from typing import List

class Run():
    def __init__(self, start_time: datetime, end_time: datetime,
                 fan: float = None, paddle_amplitude: float = None,
                 paddle_frequency: float = None,
                 water_depth: float = None) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.fan = fan
        self.paddle_amplitude = paddle_amplitude
        self.paddle_frequency = paddle_frequency

RunsList = List[Run]

class Experiment():
    def __init__(self, name: str, runs: RunsList = []) -> None:
        self.name = name
        self.runs = runs

    def add_run(self, run: Run) -> None:
        self.runs.append(run)
