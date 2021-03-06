import configparser
from pathlib import Path

from configs.configure import Configure
from configs.external.external_config_converter import ExternalConfigConverter
from configs.external.external_config_parser import ExternalConfigParser


class FileConfigureFactory(object):

    @staticmethod
    def create() -> Configure:

        if not Path("/etc/httpd.conf").is_file():
            config = configparser.ConfigParser()
            config.read_file(open(r'./default.conf'))
            port = int(config.get('server-config', 'port'))
            document_root = config.get('server-config', 'document_root')
            file_block_size = int(config.get('server-config', 'file_block_size'))
            cpu_count = int(config.get('server-config', 'cpu_count'))
            read_chunk_size = int(config.get('server-config', 'read_chunk_size'))
            write_chunk_size = int(config.get('server-config', 'write_chunk_size'))
            workers = int(config.get('server-config', 'workers'))

            return Configure(port=port, document_root=document_root, file_block_size=file_block_size,
                             cpu_count=cpu_count, read_chunk_size=read_chunk_size, write_chunk_size=write_chunk_size,
                             workers=workers)
        else:

            ext_conf = ExternalConfigParser.parse('/etc/httpd.conf')
            return ExternalConfigConverter.convert(ext_conf)


