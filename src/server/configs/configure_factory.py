import configparser
from pathlib import Path

from configs.configure import Configure


class ConfigureFactory(object):

    @staticmethod
    def create() -> Configure:
        config = configparser.ConfigParser()
        if not Path("/etc/httpd.conf").is_file():
            config.read_file(open(r'./default.conf'))
        else:
            config.read_file(open(r'/etc/httpd.conf'))

        port = int(config.get('server-config', 'port'))
        document_root = config.get('server-config', 'document_root')
        file_block_size = int(config.get('server-config', 'file_block_size'))
        cpu_count = int(config.get('server-config', 'cpu_count'))
        read_chunk_size = int(config.get('server-config', 'read_chunk_size'))
        write_chunk_size = int(config.get('server-config', 'write_chunk_size'))

        return Configure(port=port, document_root=document_root, file_block_size=file_block_size,
                         cpu_count=cpu_count, read_chunk_size=read_chunk_size, write_chunk_size=write_chunk_size)
