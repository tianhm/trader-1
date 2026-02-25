# trader

`trader` 是一个以 **CTP 原生链路** 为核心的交易项目，包含：

- 原生网关（`native/ctp_bridge` + `ctp_native`）
- 策略执行（`strategy`）
- Django 管理与可视化（`dashboard` + `panel`）

## 架构概览

### 核心模块

- `runtime_config.py`：运行时配置入口（仅读取根目录 `config.ini`）
- `ctp_native/`：Python 侧网关与本地消息总线
- `native/ctp_bridge/`：pybind11 C++ 扩展，连接 Thost API
- `strategy/`：交易策略与查询/报单流程
- `dashboard/` + `panel/`：Django 后台与页面展示

### 运行链路（简化）

1. 读取 `config.ini`
2. 初始化 `ctp_bridge_native` 并登录 CTP
3. `ctp_native` 在本地总线上分发请求/回报
4. `strategy` 消费事件并执行策略逻辑

## 快速开始

### 1) 环境准备

- Python 3.14（项目当前使用版本）
- 安装依赖：`requirements.txt`
- Windows 如使用 CTP 原生扩展：需可用 MSVC + CMake

### 2) 配置

编辑项目根目录 `config.ini`，重点检查 `[CTP_NATIVE]`：

- `gateway = pybind`
- `module = ctp_bridge_native`
- `module_path` 指向本地编译输出目录
- 补齐登录参数（`broker_id`、`investor_id`、`password`、`appid`、`authcode` 等）

`module_path` 常用示例：

- Windows Release：`native/ctp_bridge/build/Release`
- Windows Debug：`native/ctp_bridge/build/Debug`
- Linux：`native/ctp_bridge/build`

### 3) 常用命令

- 启动交易主程序：`python main.py`
- Django 检查：`python manage.py check`
- Native 查询烟测：`python test/test_native_queries.py`

### 4) 原生扩展构建（可选）

若需要本地编译 `ctp_bridge_native`：

- Windows（MSVC）：

```powershell
cd native/ctp_bridge
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
cmake --build build --config Release
```

- Linux：

```bash
cd native/ctp_bridge
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
```

详细说明见：`native/ctp_bridge/README.md`

## 目录说明

- `native/ctp_bridge`：C++ 扩展源码与 CMake
- `ctp_native`：Python 网关封装
- `strategy`：策略实现
- `dashboard`、`panel`、`templates`、`static`：Web 展示与后台
