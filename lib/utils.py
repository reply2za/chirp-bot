

def trim_voice_channel_name(voice_channel_name: str) -> str:
    voice_channel_trimmed = ''
    for vc in voice_channel_name.split(' '):
            if vc.strip() != '':
                voice_channel_trimmed += f"{vc} "
    return voice_channel_trimmed