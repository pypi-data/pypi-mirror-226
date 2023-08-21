import platform, pkg_resources

from CheeseType import System

class System:
    def __init__(self):
        systems = {
            'Windows': 'WINDOWS',
            'Linux': 'LINUX',
            'Darwin': 'MACOS'
        }
        system = platform.system()
        if system in systems:
            self.SYSTEM: System = System(systems[system])
        else:
            self.SYSTEM: System = System('OTHER')

        self.PYTHON_VERSION: str = platform.python_version()
        try:
            self.CHEESEAPI_VERSION: str = pkg_resources.get_distribution('CheeseAPI').version
        except:
            self.CHEESEAPI_VERSION: str = None
