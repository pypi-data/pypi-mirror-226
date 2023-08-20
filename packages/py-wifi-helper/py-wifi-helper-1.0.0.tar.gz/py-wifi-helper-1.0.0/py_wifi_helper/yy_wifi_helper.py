# -*- encoding: utf-8 -*-

import os
import platform
from enum import Enum

class WIFIAP_SECURITY(Enum):
    pass

class WIFIAP(str, Enum):
    SSID = 'ssid'
    BSSID = 'bssid'
    RSSI = 'rssi'
    IBSS = 'ibbs'
    SECURITY = 'security'
    CHANNEL_BAND = 'channel.band'
    CHANNEL_NUMBER = 'channel.number'
    CHANNEL_WIDTH = 'channel.width'
    RAW = 'raw'

# https://developer.apple.com/documentation/corewlan/cwsecurity?language=objc
class YYWIFISecurityMode(str, Enum):
    SecurityNone = 'SecurityNone'
    SecurityWEP = 'SecurityWEP'
    SecurityWPAPersonal = 'SecurityWPAPersonal'
    SecurityWPAPersonalMixed = 'SecurityWPAPersonalMixed'
    SecurityWPA2Personal = 'SecurityWPA2Personal'
    SecurityPersonal = 'SecurityPersonal'
    SecurityDynamicWEP = 'SecurityDynamicWEP'
    SecurityWPAEnterprise = 'SecurityWPAEnterprise'
    SecurityWPAEnterpriseMixed = 'SecurityWPAEnterpriseMixed'
    SecurityWPA2Enterprise = 'SecurityWPA2Enterprise'
    SecurityEnterprise = 'SecurityEnterprise'
    SecurityWPA3Personal = 'SecurityWPA3Personal'
    SecurityWPA3Enterprise = 'SecurityWPA3Enterprise'
    SecurityWPA3Transition = 'SecurityWPA3Transition'
    SecurityUnknown = 'SecurityUnknown'

class YYOSWIFIHelper:
    def disableEventHandler(self):
        pass
    def enableEventHandler(self, handler: None, debug:bool = False ):
        pass
    def getConnectedAPSSID(self, targetInterface: str | None = None) -> (bool, str | None, str | None):
        pass
    def getInterface(self):
        pass
    def disconnect(self, targetInterface:str | None = None, asyncMode: bool = False, asyncWaitTimeout: int = 15) -> (bool, str):
        pass
    def connectToAP(self, targetSSID:str , targetPassword: str | None = None, targetSecurity: YYWIFISecurityMode | None = None, findSSIDBeforeConnect:bool = False, targetInterface: str | None = None, asyncMode: bool = False, asyncWaitTimeout: int = 15) -> (bool, str):
        pass
    def scanToGetAPList(self, targetInterface:str | None = None):
        pass
    def scanToGetAPListInJSON(self, targetInterface: str | None = None):
        pass

class YYWIFIHelper:
    def __init__(self):
        self._platform = platform.system().lower()
        self._supportPlatform = [ 'darwin' ] 
        #if self._platform == 'linux' and os.path.isdir('/var/run/wpa_supplicant'):
        #    # ubuntu: apt install wpasupplicant ; service wpa_supplicant start ; service wpa_supplicant status
        #    self._supportPlatform.append('linux')
        self._platformInfo = {}
        if self._platform == 'linux':
            if os.path.isfile('/etc/lsb-release'):
                for line in open('/etc/lsb-release').read().split('\n'):
                    keyValue = line.split('=')
                    if len(keyValue) == 2:
                        self._platformInfo[keyValue[0].strip().lower()] = keyValue[1].strip().lower()

            if 'distrib_id' in self._platformInfo:
                if self._platformInfo['distrib_id'] == 'ubuntu' and 'distrib_release' in self._platformInfo:
                    try:
                        if float(self._platformInfo['distrib_release']) >= 22.04:
                            # Step 0 : TODO - Check resource
                            # dkms, nmcli, wireless-tools, lsusb
                            from shutil import which

                            cliCheckPass = True
                            cliList = [
                                    'nmcli', 
                                    #'lsusb', 'iwconfig',
                                    #'wavemon',
                                    #'iwlist',
                            ]
                            for cli in cliList:
                                if which(cli) == None:
                                    print(f"[INFO] cli not found: {cli}")
                                    cliCheckPass = False
    
                            # Step 1 : Add
                            if cliCheckPass:
                                self._supportPlatform.append('ubuntu')
                                self._platform = 'ubuntu'
                    except Exception as e:
                        print(f"{str(e)}")
    
        self._support = self._platform in self._supportPlatform
        if self._support:
            if self._platform == 'darwin':
                from . import my_macos_helper
                self._helper = my_macos_helper.YYMacOSWIFIHelper()
            elif self._platform == 'ubuntu':
                from . import my_ubuntu_helper
                self._helper = my_ubuntu_helper.YYUbuntuWIFIHelper()

        self.eventHandler = None

    def eventCallback(self, info: dict | None = None):
        if self.eventHandler and callable(self.eventHandler):
            self.eventHandler(info)

    def enableEventHandler(self, handlerFunc: None):
        if not self._support:
            print(self._support)
            return
        self.eventHandler = handlerFunc
        self._helper.enableEventHandler(self)

    def disableEventHandler(self):
        if not self._support:
            print(self._support)
            return
        self._helper.disableEventHandler(self)
        self.eventHandler = None

    def getInterface(self):
        if not self._support:
            print(self._support)
            return
        return self._helper.getInterface()

    def getAPList(self, name=None):
        if not self._support:
            print(self._support)
            return
        return self._helper.scanToGetAPList(name)

    def getAPListInJSON(self, name=None):
        if not self._support:
            print(self._support)
            return
        return self._helper.scanToGetAPListInJSON(name)

    def getConnectedAPSSID(self, targetInterface: str | None = None) -> (bool, str | None, str | None):
        if not self._support:
            print(self._support)
            return (False, None, 'NOT SUPPORT')
        return self._helper.getConnectedAPSSID(targetInterface)

    def disconnect(self, targetInterface:str | None = None, asyncMode: bool = False, asyncWaitTimeout: int = 15) -> (bool, str):
        if not self._support:
            print(self._support)
            return (False, None, 'NOT SUPPORT')
        return self._helper.disconnect(targetInterface, asyncMode, asyncWaitTimeout)

    def connectToAP(self, targetSSID:str , targetPassword: str | None = None, targetSecurity: str | None = None, findSSIDBeforeConnect:bool = False, targetInterface: str | None = None, asyncMode: bool = False, asyncWaitTimeout: int = 15) -> (bool, str):
        if not self._support:
            print(self._support)
            return
        return self._helper.connectToAP(targetSSID, targetPassword, targetSecurity, findSSIDBeforeConnect, targetInterface, asyncMode, asyncWaitTimeout)

