

try:
    from robot.libraries.BuiltIn import BuiltIn
    from robot.libraries.BuiltIn import _Misc
    import robot.api.logger as logger
    from robot.api.deco import keyword

    import requests
    import uuid
    from TrackerDB import *

    ROBOT = False

except Exception:
    ROBOT = False
