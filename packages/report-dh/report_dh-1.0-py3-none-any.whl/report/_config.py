import argparse
from . import _internal
from ._data import parse


def config():
    parser = argparse.ArgumentParser(description='Pytest Report Portal Wrapper')
    parser.add_argument('--host', '-H', required=True, help='host:ip or domain name (Example: localhost:8080)')
    parser.add_argument('--bearer-uuid', '-u', required=True, help='Auth bearer UUID')
    parser.add_argument('--project-name', '-p', required=True, help='Report Portal project name')
    parser.add_argument('--launch-name', '-l', default='new launch' ,help='New launch name ( default is "new launch" )')

    args = parser.parse_args()
    _internal.Data.endpoint = args.host
    _internal.Data.launch_name = args.launch_name
    _internal.Data.uuid = args.bearer_uuid
    _internal.Data.project = args.project_name
    _internal.Data.update_url()
    _internal.Data.update_headers()


if __name__ == '__main__':
    data = config()
    parse()

