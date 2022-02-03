
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

    def on_start(self):
        self.power = 100
        self.state = False
        # Initiate kit object
        self.kit = MotorKit(i2c=board.I2C())
        
        if self.props.get("elementNumber", 1) == 1:
            self.motor = self.kit.motor1
        elif self.props.get("elementNumber", 1) == 2:
            self.motor = self.kit.motor2
        elif self.props.get("elementNumber", 1) == 3:
            self.motor = self.kit.motor3
        elif self.props.get("elementNumber", 1) == 4:
            self.motor = self.kit.motor4 
        self.state = False
        pass

    async def on(self, power=None):
        if power is not None:
            self.power = int(power)
        self.motor.throttle = power * 0.01
        self.state = True
        await self.cbpi.actor.actor_update(self.id,self.power)

    async def off(self):
        self.motor.throttle = 0
        logger.info("ACTOR %s OFF " % self.id)
        self.state = False
        await self.cbpi.actor.actor_update(self.id,0)

    def get_state(self):
        return self.state
    
    async def run(self):
        while self.running == True:
            await asyncio.sleep(1)


def setup(cbpi):
    cbpi.plugin.register("i2cPWM", i2cPWMActor)
    pass