import paramiko
from contextlib import contextmanager

host = "eu1.freegamehost.xyz"
port = 2022
username = "dep1con.dc332229"
password = "depicon 617 *"

class interactiveSFTPCclient:
    def __init__(self, host, port, username, password=None, private_key_path=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.private_key_path = private_key_path
        self.sftp_client = None
        self.transport = None

    def connect(self):
        try:
            # First initializing the ssh transport mechanism
            self.transport = paramiko.Transport((self.host, self.port))
            if (self.private_key_path is not None) and (self.private_key_path != ""):
                # i use ed25519 keys by default, but i will implement key algorithm change feature later
                private_key = paramiko.Ed25519Key.from_private_key_file(self.private_key_path)
                self.transport.connect(username=self.username, pkey=private_key)

            else:
                self.transport.connect(username=self.username, password=self.password)

            #then we create the sftp client from the transport
            self.sftp_client = paramiko.SFTPClient.from_transport(self.transport)
            print("Connected to the server successfully.")
            print(self.sftp_client.listdir())
        except Exception as e:
            print(f"Failed to connect: {e}")

    def disconnect(self):
        if self.sftp_client:
            self.sftp_client.close()
        if self.transport:
            self.transport.close()
        print("Disconnected from the server.")

    def list_files(self, path="."):
        if self.sftp_client:
            try:
                return self.sftp_client.listdir(path)
            except Exception as e:
                print(f"Failed to list files: {e}")
        else:
            print("Not connected to the server.")
    # @contextmanager
    # def sftp_session(self):
    #     try:
    #         self.connect()
    #         yield
    #     finally:
    #         self.disconnect()

if __name__ == "__main__":
    sftpClient = interactiveSFTPCclient(host, port, username, password)
    sftpClient.connect()
    while True:
        input("Press q or exit to disconnect...")
        if (input().lower() in ["q", "exit"]):
            sftpClient.disconnect()
            break
