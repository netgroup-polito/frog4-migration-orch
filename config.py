from exception import WrongConfigurationFile
import configparser

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Configuration(object, metaclass=Singleton):

    def __init__(self):
        self.conf_file = "config/default-config.ini"

        self.inizialize()

    def inizialize(self):

        configParser = configparser.SafeConfigParser()
        configParser.read(self.conf_file)

        try:

            #self._LOG_FILE = configParser.get('logging','log_file')
            #self._LOG_LEVEL = configParser.get('logging','log_level')

            self._ORCH_ADDRESS = configParser.get('orchestrator','address')
            self._ORCH_PORT = configParser.get('orchestrator','port')

            self._CONFIGURATION_ORCH_ADDRESS = configParser.get('configuration-orchestrator','address')
            self._CONFIGURATION_ORCH_PORT = configParser.get('configuration-orchestrator','port')

            self._EXECUTION = configParser.get('orchestrator','execution')

            self._USERNAME = configParser.get('debug-info','username')
            self._PASSWORD = configParser.get('debug-info','password')

            self._GRAPHS_PATH = configParser.get('graphs','graphs_path')


        except Exception as ex:
            raise WrongConfigurationFile(str(ex))

    """
    @property
    def LOG_FILE(self):
        return self._LOG_FILE

    @property
    def LOG_LEVEL(self):
        return self._LOG_LEVEL
    """

    @property
    def ORCH_ADDRESS(self):
        return self._ORCH_ADDRESS

    @property
    def ORCH_PORT(self):
        return self._ORCH_PORT

    @property
    def CONFIGURATION_ORCH_ADDRESS(self):
        return self._CONFIGURATION_ORCH_ADDRESS

    @property
    def CONFIGURATION_ORCH_PORT(self):
        return self._CONFIGURATION_ORCH_PORT

    @property
    def EXECUTION(self):
        return self._EXECUTION

    @property
    def USERNAME(self):
        return self._USERNAME

    @property
    def PASSWORD(self):
        return self._PASSWORD

    @property
    def GRAPHS_PATH(self):
        return self._GRAPHS_PATH

