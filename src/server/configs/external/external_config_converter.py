from configs.configure import Configure
from configs.external.external_configure import ExternalConfigure


class ExternalConfigConverter(object):

    @staticmethod
    def convert(ext_conf: ExternalConfigure) -> Configure:

        port = ext_conf.listen
        document_root = ext_conf.document_root
        file_block_size = 1024
        cpu_count = ext_conf.cpu_limit
        read_chunk_size = 1024
        write_chunk_size = 1024
        workers = 1024

        return Configure(port=port, document_root=document_root, file_block_size=file_block_size, workers=workers,
                         cpu_count=cpu_count, read_chunk_size=read_chunk_size, write_chunk_size=write_chunk_size)
