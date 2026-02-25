# coding=utf-8
import configparser
import os
from configparser import MissingSectionHeaderError


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


_DEFAULT_RUNTIME_CONFIG = """[CTP_NATIVE]
gateway = pybind
module = ctp_bridge_native
client_class = CtpClient
module_path = {module_path}
dll_dir = {dll_dir}
trade_front = tcp://180.168.146.187:10001
market_front = tcp://180.168.146.187:10011
broker_id =
investor_id =
password =
appid =
authcode =
userinfo =
ip = 1.2.3.4
mac = 02:03:04:5a:6b:7c
flow_path = {flow_path}
request_timeout_ms = 10000
""".format(
    module_path=os.path.join(REPO_ROOT, 'native', 'ctp_bridge', 'build', 'Release').replace('\\', '/'),
    dll_dir=os.path.join(REPO_ROOT, 'native', 'ctp_bridge', 'api', 'win').replace('\\', '/'),
    flow_path=os.path.join(REPO_ROOT, 'native', 'ctp_bridge', 'flow').replace('\\', '/'),
)


def load_runtime_config() -> configparser.ConfigParser:
    root_config_file = os.path.join(REPO_ROOT, 'config.ini')
    parser = configparser.ConfigParser(interpolation=None)
    parser.read_string(_DEFAULT_RUNTIME_CONFIG)
    if os.path.exists(root_config_file):
        try:
            try:
                parser.read(root_config_file, encoding='utf-8')
            except UnicodeDecodeError:
                parser.read(root_config_file, encoding='gb18030')
        except MissingSectionHeaderError:
            raw = {}
            with open(root_config_file, 'rt', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    s = line.strip()
                    if not s or s.startswith(';') or s.startswith('#') or '=' not in s:
                        continue
                    k, v = s.split('=', 1)
                    raw[k.strip()] = v.strip()
            mapping = {
                'trade': 'trade_front',
                'market': 'market_front',
                'broker': 'broker_id',
                'investor': 'investor_id',
                'passwd': 'password',
                'appid': 'appid',
                'authcode': 'authcode',
                'userinfo': 'userinfo',
                'ip': 'ip',
                'mac': 'mac',
            }
            for src_key, dst_key in mapping.items():
                if src_key in raw:
                    parser.set('CTP_NATIVE', dst_key, raw[src_key])
    return parser


runtime_config = load_runtime_config()
