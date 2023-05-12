
import json
from typing import Dict

# contains discord server data, and the voice channels that the user has subscribed to 
class Server: 
    def __init__(self, server_id: str, prefix: str, tracked_voice_channels=[]):
        self.server_id = str(server_id)
        # the voice channels to track for updates
        self.tracked_voice_channels = []
        self.prefix = prefix
        self.tracked_voice_channels = tracked_voice_channels
    def get_server_id(self) -> str:
        return self.server_id
    
    def serialize_data(self): 
        serialized_data = json.dumps({
            self.server_id : {
            'tracked_voice_channels': self.tracked_voice_channels,
            'prefix': self.prefix
            }
        })
        print(serialized_data)
        return serialized_data
    



# contains all the servers that the bot is in
class _ServerManager: 
    def __init__(self):
        self.servers: Dict[str,Server] = {}

    def add_server(self, server: Server):
        self.servers[server.get_server_id()] = server
    
    def get_server(self, server_id):
        if server_id in self.servers:
            return self.servers[server_id]
        else:
            return None
    
    def serialize_servers(self):
        serialized_servers = {}
        for server in self.servers.values():
            serialized_servers.setdefault(server.get_server_id(), server.serialize_data())
        return json.dumps(serialized_servers)
    
    def deserialize_servers(self, raw_data):
        if raw_data is None:
            return
        list_of_server = dict(json.loads(raw_data))
        for key in list_of_server:
            servers = eval(list_of_server[key])
            for a_server in servers:
                server_values = servers[a_server]
                self.servers[key] = Server(key, server_values['prefix'], server_values['tracked_voice_channels'])
    

servers = _ServerManager()