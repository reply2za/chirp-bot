from lib.events.CommandErrorEvent import command_error_event
from lib.events.MessageCreatedEvent import message_created_event
from lib.events.ReadyEvent import ready_event
from lib.events.VoiceStateUpdateEvent import voice_state_update


def load_events():
    command_error_event.enable_event()
    message_created_event.enable_event()
    voice_state_update.enable_event()
    ready_event.enable_event()
