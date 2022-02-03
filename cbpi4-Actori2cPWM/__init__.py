
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *
from cbpi.api.dataclasses import NotificationAction, NotificationType

##### Actor requirements #####
import time
import board
from adafruit_motorkit import MotorKit
###############################

logger = logging.getLogger(__name__)


@parameters([
    Property.Select(label="elementNumber", options=[1,2,3,4], description="number between 1 and 4"),
    Property.Number(label="frequency", configurable=True)
])
class i2cPWMActor(CBPiActor):
    
    # create a default object, no changes to I2C address or frequency
    kit = MotorKit(i2c=board.I2C())
    
    def __init__(self, cbpi, id, props):
        super(i2cPWMActor, self).__init__(cbpi, id, props)
        self.elementNumber = int(self.props.get("elementNumber", 1))
        self.state = False

    async def on(self, power=0):
        self.power = int(power)
        if self.elementNumber == 1:
            kit.motor1.throttle = self.power * 0.01
        elif self.elementNumber == 2:
            kit.motor2.throttle = self.power * 0.01
        elif self.elementNumber == 3:
            kit.motor3.throttle = self.power * 0.01
        elif self.elementNumber == 4:
            kit.motor4.throttle = self.power * 0.01
        self.state = True

    async def off(self):
        if self.elementNumber == 1:
            kit.motor1.throttle = 0
        elif self.elementNumber == 2:
            kit.motor2.throttle = 0
        elif self.elementNumber == 3:
            kit.motor3.throttle = 0
        elif self.elementNumber == 4:
            kit.motor4.throttle = 0
        logger.info("ACTOR %s OFF " % self.id)
        self.state = False

    def get_state(self):
        return self.state
    
    async def run(self):
        pass


def setup(cbpi):
    cbpi.plugin.register("i2cPWM", i2cPWMActor)
    pass