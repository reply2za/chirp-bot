from lib.logger import logger


with open("pyproject.toml", "r") as f:
    version = None
    for line in f.readlines():
        if "version" in line:
            version = line.split("=")[1].strip().replace('"', "")
            break
    if version is None:
        logger.error("version not found in pyproject.toml")


def trim_voice_channel_name(voice_channel_name: str) -> str:
    voice_channel_trimmed = ''
    for vc in voice_channel_name.split(' '):
            if vc.strip() != '':
                voice_channel_trimmed += f"{vc} "
    return voice_channel_trimmed