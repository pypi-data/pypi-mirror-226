import re

MAX_ID_LENGTH = 256
ID_REGEX = r"^[a-zA-Z0-9][a-zA-Z0-9_.-]{0," + re.escape(str(MAX_ID_LENGTH - 1)) + r"}$"
deviceID_regex = ID_REGEX
"DeviceIDs must follow this pattern"
recordingID_regex = ID_REGEX
"RecordingIDs must follow this pattern"

MAX_MARKER_COUNT = 1000
"Max number of markers currently allowed to be attached to metadata"
