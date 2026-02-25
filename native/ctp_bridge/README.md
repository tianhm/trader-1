# ctp_bridge_native（简化说明）

`ctp_bridge_native` 是 `trader` 的本地 C++ 扩展，用于通过 pybind11 直连 CTP Thost API。

## 目录结构

- `CMakeLists.txt`：构建入口
- `src/py_module.cpp`：`CtpClient` 导出与回调桥接
- `api/win`、`api/linux`：Thost 头文件与库

## 构建

在 `native/ctp_bridge` 目录下执行 CMake 构建。

当前构建设置：

- C++ 标准：`C++23`
- Windows + MSVC：启用 `/std:c++latest` 与 `/utf-8`

### Windows（MSVC）最小命令

```powershell
cd native/ctp_bridge
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
cmake --build build --config Release
```

### Linux（GCC/Clang）最小命令

```bash
cd native/ctp_bridge
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
```

编译成功后，通常模块输出在：

- Windows：`native/ctp_bridge/build/Release`
- Linux：`native/ctp_bridge/build`

## 配置

在项目根目录 `config.ini` 的 `[CTP_NATIVE]` 段确保：

- `gateway = pybind`
- `module = ctp_bridge_native`
- `module_path = <构建输出目录>`（例如 `native/ctp_bridge/build/Release`）

### `module_path` 推荐写法（按平台）

在 `config.ini` 中可直接写为：

- Windows（Release）

```ini
module_path = native/ctp_bridge/build/Release
```

- Windows（Debug）

```ini
module_path = native/ctp_bridge/build/Debug
```

- Linux（单配置生成器）

```ini
module_path = native/ctp_bridge/build
```

建议优先使用 Release；若你本地是 Debug 构建，请同步把 `module_path` 指到 `Debug` 目录。

## 快速验证

回到项目根目录执行：

- `python test/test_native_queries.py`

可选环境变量：

- `CTP_TEST_WARMUP_SECONDS`：登录预热秒数
- `CTP_TEST_INSTRUMENT`：优先测试合约（若无效会自动回退）
