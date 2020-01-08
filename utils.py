import sys
import logging
from typing import Optional

LOGGING_LEVELS = {
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'warning': logging.WARNING,
    'error': logging.ERROR,
}


def generate_logger(name: str = "", level: str = 'info',
                    format: str = '%(filename)s - %(lineno)d - %(message)s') -> logging.Logger:
    try:
        logger = logging.getLogger(name or __file__ + "_logger")
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(format))
        logger.addHandler(handler)
        logger.setLevel(LOGGING_LEVELS[level])
        return logger
    except Exception as e:
        raise Exception(f"Failed to generate logger: {e}")


UTIL_LOGGER = generate_logger('UtilLogger')


def connect_wifi(ssid: str, password: Optional[str] = None) -> bool:
    UTIL_LOGGER.debug(f"connecting to {ssid}")
    if sys.platform == 'linux':
        from wireless import Wireless
        Wireless().connect(ssid=ssid, password=password)
    elif sys.platform == 'win32' or sys.platform == 'cygwin':
        import winwifi
        winwifi.WinWiFi.connect(ssid)
    else:
        UTIL_LOGGER.error(f"Can't auto-connect to wifi on {sys.platform}")
        return False
    return True
