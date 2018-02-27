from configs.configure import Configure


class SrcConfigureFactory(object):

    @staticmethod
    def create() -> Configure:
        port = 8080
        document_root = "/home/anton/dev/tp/tp-highload/tests/static"
        file_block_size = 1024
        cpu_count = 4
        read_chunk_size = 1024
        write_chunk_size = 1024
        workers = 1

        return Configure(port=port, document_root=document_root, file_block_size=file_block_size, workers=workers,
                         cpu_count=cpu_count, read_chunk_size=read_chunk_size, write_chunk_size=write_chunk_size)
