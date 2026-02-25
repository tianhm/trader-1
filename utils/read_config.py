# coding=utf-8
#
# Copyright 2016 timercrack
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import sys
import os
import xml.etree.ElementTree as ET
import configparser
from configparser import MissingSectionHeaderError
from appdirs import AppDirs

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_example = """# trader configuration file
[MSG_CHANNEL]
request_pattern = MSG:CTP:REQ:*
request_format = MSG:CTP:REQ:{}
trade_response_prefix = MSG:CTP:RSP:TRADE:
trade_response_format = MSG:CTP:RSP:TRADE:{}:{}
market_response_prefix = MSG:CTP:RSP:MARKET:
market_response_format = MSG:CTP:RSP:MARKET:{}:{}
weixin_log = MSG:LOG:WEIXIN

[TRADE]
command_timeout = 5
ignore_inst = WH,bb,JR,RI,RS,LR,PM,im
transport = native

[CTP_NATIVE]
gateway = pybind
module = ctp_bridge_native
client_class = CtpClient
module_path = __MODULE_PATH__
dll_dir = __DLL_DIR__
trade_front = tcp://180.168.146.187:10001
market_front = tcp://180.168.146.187:10011
broker_id = 9999
investor_id = 123456
password = passwd
appid = xxx
authcode = xxx
userinfo = xxx
ip = 1.2.3.4
mac = 02:03:04:5a:6b:7c
flow_path = __FLOW_PATH__
request_timeout_ms = 10000

[MYSQL]
host = 127.0.0.1
port = 3306
db = QuantDB
user = quant
password = 123456

[QuantDL]
api_key = 123456

[Tushare]
token = 123456

[LOG]
level = DEBUG
format = %(asctime)s %(name)s [%(levelname)s] %(message)s
weixin_format = [%(levelname)s] %(message)s
"""
config_example = config_example.replace('__MODULE_PATH__', os.path.join(REPO_ROOT, 'native', 'ctp_bridge', 'build', 'Release').replace('\\', '/'))
config_example = config_example.replace('__DLL_DIR__', os.path.join(REPO_ROOT, 'native', 'ctp_bridge', 'api', 'win').replace('\\', '/'))
config_example = config_example.replace('__FLOW_PATH__', os.path.join(REPO_ROOT, 'native', 'ctp_bridge', 'flow').replace('\\', '/'))

app_dir = AppDirs('trader')
root_config_file = os.path.join(REPO_ROOT, 'config.ini')

if not os.path.exists(root_config_file):
    with open(root_config_file, 'wt', encoding='utf-8') as f:
        f.write(config_example)
    print('create config file:', root_config_file)

config_file = root_config_file

config = configparser.ConfigParser(interpolation=None)
config.read_string(config_example)


def _load_config_with_legacy_support(cfg: configparser.ConfigParser, path: str):
    try:
        try:
            cfg.read(path, encoding='utf-8')
        except UnicodeDecodeError:
            cfg.read(path, encoding='gb18030')
    except MissingSectionHeaderError:
        # 兼容 backend-ctp 老格式（无 section header 的 key=value）
        raw = {}
        with open(path, 'rt', encoding='utf-8', errors='ignore') as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith(';') or s.startswith('#') or '=' not in s:
                    continue
                k, v = s.split('=', 1)
                raw[k.strip()] = v.strip()

        # CTP native
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
                cfg.set('CTP_NATIVE', dst_key, raw[src_key])


_load_config_with_legacy_support(config, config_file)

ctp_errors = {}
ctp_xml_path = os.path.join(REPO_ROOT, 'utils', 'error.xml')
for error in ET.parse(ctp_xml_path).getroot():
    ctp_errors[int(error.attrib['value'])] = error.attrib['prompt']
