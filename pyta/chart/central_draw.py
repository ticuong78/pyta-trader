import logging

from .chart import Chart

logger = logging.getLogger(__name__)

class CentralDraw():
    charts = []

    def __init__(self):
        pass

    def register_chart(self, chart: Chart):
        if chart == None:
            logger.warning("Should not register null chart")
            return

        self.charts.append(chart)