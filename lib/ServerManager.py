
import json
from typing import Dict

from lib.SheetDatabase import sheet_database

# contains discord server data, and the voice channels that the user has subscribed to 
class Server: 
    def __init__(self, server_id: str, prefix: str, tracked_voice_channels: dict={}):
        self.server_id = str(server_id)
        # the voice channels to track for updates
        self.prefix = prefix
        self.tracked_voice_channels = tracked_voice_channels
    def get_server_id(self) -> str:
        return self.server_id
    
    def serialize_data(self): 
        serialized_data = json.dumps({
        'server_id': self.server_id,
        'tracked_voice_channels': self.tracked_voice_channels,
        'prefix': self.prefix
    
        })
        return serialized_data

    def track_voice_channel(self, voice_channel_id: str, channel_id: str):
        if not isinstance(voice_channel_id, str):
            voice_channel_id = str(voice_channel_id)
        if not isinstance(channel_id, str):
            channel_id = str(channel_id)
        self.tracked_voice_channels.setdefault(voice_channel_id, {'txt_channel_id': channel_id})
        self._save()

    def untrack_voice_channel(self, voice_channel_id: str) -> bool:
        if not isinstance(voice_channel_id, str):
            voice_channel_id = str(voice_channel_id)
        existing_vc = self.tracked_voice_channels.pop(voice_channel_id)
        self._save()
        return existing_vc is not None

    def _save(self):
        sheet_database.set_data(servers.serialize_servers())
    



# contains all the servers that the bot is in
class _ServerManager: 
    def __init__(self):
        self.servers: Dict[str,Server] = {}

    def add_server(self, server: Server):
        self.servers[str(server.get_server_id())] = server
        sheet_database.set_data(servers.serialize_servers())
    
    def get_server(self, server_id):
        if not isinstance(server_id, str):
            server_id = str(server_id)
        if server_id in self.servers:
            return self.servers[server_id]
        else:
            return None
    
    def serialize_servers(self):
        serialized_servers = {}
        for server in self.servers.values():
            serialized_servers.setdefault(str(server.get_server_id()), server.serialize_data())
        return json.dumps(serialized_servers)
    
    def deserialize_servers(self, raw_data):
        if raw_data is None:
            return
        list_of_server = dict(json.loads(raw_data))
        for key in list_of_server:
            server = eval(list_of_server[key])
            self.servers[key] = Server(key, server['prefix'], server['tracked_voice_channels'])
    

servers = _ServerManager()