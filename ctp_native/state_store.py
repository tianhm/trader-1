# coding=utf-8
import os
import threading
import time
from typing import Any

from appdirs import AppDirs
import orjson


class NativeStateStore:
    def __init__(self):
        self._lock = threading.RLock()
        self._kv: dict[str, Any] = {}
        self._expire_at: dict[str, float] = {}
        dirs = AppDirs('trader')
        self._cache_dir = dirs.user_cache_dir
        self._snapshot_file = os.path.join(self._cache_dir, 'native_state.json')
        self._load_snapshot()

    def _load_snapshot(self):
        if not os.path.exists(self._snapshot_file):
            return
        try:
            with open(self._snapshot_file, 'rt', encoding='utf-8') as f:
                data = orjson.loads(f.read())
            if isinstance(data, dict):
                self._kv.update(data.get('kv', {}))
                expire_at = data.get('expire_at', {})
                if isinstance(expire_at, dict):
                    self._expire_at.update({str(k): float(v) for k, v in expire_at.items()})
        except Exception:
            # 快照损坏不应阻塞主流程
            pass

    def dump_snapshot(self):
        try:
            if not os.path.exists(self._cache_dir):
                os.makedirs(self._cache_dir)
            payload = {
                'kv': self._kv,
                'expire_at': self._expire_at,
            }
            with open(self._snapshot_file, 'wb') as f:
                f.write(orjson.dumps(payload))
        except Exception:
            # 快照失败不影响交易流程
            pass

    def _is_expired(self, key: str) -> bool:
        expire_at = self._expire_at.get(key)
        if expire_at is None:
            return False
        if expire_at <= time.time():
            self._kv.pop(key, None)
            self._expire_at.pop(key, None)
            return True
        return False

    def get(self, key: str, default: Any = None):
        with self._lock:
            if self._is_expired(key):
                return default
            return self._kv.get(key, default)

    def set(self, key: str, value: Any, ex: int | None = None):
        with self._lock:
            self._kv[key] = value
            if ex is not None:
                self._expire_at[key] = time.time() + ex
            else:
                self._expire_at.pop(key, None)

    def delete(self, key: str):
        with self._lock:
            self._kv.pop(key, None)
            self._expire_at.pop(key, None)


state_store = NativeStateStore()
