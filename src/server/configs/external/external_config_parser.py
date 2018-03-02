from configs.external.external_configure import ExternalConfigure


class ExternalConfigParser(object):
    @staticmethod
    def parse(filename: str) -> ExternalConfigure:
        data = {}
        with open(filename) as file:
            for line in file:
                pair = line.split()
                key: str = pair[0]
                value: str = pair[1]
                data.update({
                    key: value
                })

        listen = 80 if data.get('listen') is None else data['listen']
        cpu_limit = 1 if data.get('cpu_limit') is None else data['cpu_limit']
        thread_limit = 8 if data.get('thread_limit') is None else data['thread_limit']
        document_root = "/var/www/html" if data.get('document_root') is None else data['document_root']

        return ExternalConfigure(listen=listen, cpu_limit=cpu_limit,
                                 thread_limit=thread_limit, document_root=document_root)
