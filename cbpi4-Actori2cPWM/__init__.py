
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
    
    def __init__(self, cbpi, id, props):
        super(i2cPWMActor, self).__init__(cbpi, id, props)
        
        kit = MotorKit(i2c=board.I2C())
        self.elementNumber = int(self.props.get("elementNumber", 1))
        
        if self.elementNumber == 1:
            self.motor = kit.motor1
        elif self.elementNumber == 2:
            self.motor = kit.motor2
        elif self.elementNumber == 3:
            self.motor = kit.motor3
        elif self.elementNumber == 4:
            self.motor = kit.motor4 
        self.state = False

    async def on(self, power=0):
        self.power = int(power)
        self.motor.throttle = self.power * 0.01
        self.state = True
        self.push_update()

    async def off(self):
        self.motor.throttle = 0
        logger.info("ACTOR %s OFF " % self.id)
        self.state = False
        self.push_update()

    def get_state(self):
        return self.state
    
    async def run(self):
        pass


def setup(cbpi):
    cbpi.plugin.register("i2cPWM", i2cPWMActor)
    pass