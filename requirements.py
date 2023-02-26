from config_variables import Configuration


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

CH1_OFFSET = 1
CH2_OFFSET = 1
CH3_OFFSET = 1
CH4_OFFSET = 1

CH1_SAMPLE_START, CH1_SAMPLE_END = 0, 5000
CH2_SAMPLE_START, CH2_SAMPLE_END = 0, 5000
CH3_SAMPLE_START, CH3_SAMPLE_END = 0, 5000
CH4_SAMPLE_START, CH4_SAMPLE_END = 0, 5000

COLORS = {
    "RED": "red",
    "GREEN": "green",
    "BLUE": "blue",
    "BLACK": "black",
    "WHITE": "white",
    "SILVER": "silver",
    "GREY": "grey",
    "LIGHT_BLUE": "light blue",
    "LIGHT_GREEN": "#105D19",
    "YELLOW": "yellow",
    "BLUE_HEX": "#006BBD",
    "DARK_BLUE": "#26166E",
    "DARK_GREEN": "dark green",
    "HEX_BLUE": "#519FC6"
}

config = Configuration()
