
class Config:
    def __init__(self) -> None:
        self.server_ip = "127.0.0.1"
        self.server_port = 7532
        self.screen_width = 1080
        self.screen_height = 720

        self.config_filename = "config"

        self.read_config()

    def read_config(self):
        with open(self.config_filename, "r") as f:
            for line in f.readlines():
                tokens = line.split(":")

                if tokens[0] == "server-ip":
                    self.server_ip = tokens[1].rstrip("\n")
                elif tokens[0] == "server-port":
                    self.server_port = int(tokens[1])
                elif tokens[0] == "screen-width":
                    self.screen_width = int(tokens[1])
                elif tokens[0] == "screen-height":
                    self.screen_height = int(tokens[1])
