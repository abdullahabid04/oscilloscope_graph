def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Configuration(object):
    DATA_FRAME = None

    NO_OF_CHANNELS = 4

    CH1_THRESHOLD = 3
    CH2_THRESHOLD = 7
    CH3_THRESHOLD = 5
    CH4_THRESHOLD = 5

    CH1_K_MAX = 25
    CH2_K_MAX = 25
    CH3_K_MAX = 15
    CH4_K_MAX = 15

    CH1_SCALER = 1
    CH2_SCALER = 1
    CH3_SCALER = 1
    CH4_SCALER = 1

    CH1_OFFSET = 0
    CH2_OFFSET = 0
    CH3_OFFSET = 0
    CH4_OFFSET = 0

    CH1_SAMPLE_START = 0
    CH2_SAMPLE_START = 0
    CH3_SAMPLE_START = 0
    CH4_SAMPLE_START = 0

    CH1_SAMPLE_END = 5000
    CH2_SAMPLE_END = 5000
    CH3_SAMPLE_END = 5000
    CH4_SAMPLE_END = 5000
