# 项目结构说明

本文档详细说明了 FileRenameEditor 项目的文件结构和组织方式。

## 📁 目录结构

```
FileRenameEditor/
├── 📄 核心文件
│   ├── app.py                          # 主应用程序入口
│   ├── main.py                         # 程序启动入口
│   └── simple_main.py                  # 简化版启动入口
│
├── 📂 MVC架构模块
│   ├── models/                         # 数据模型层 (Model)
│   │   ├── __init__.py
│   │   ├── file_manager.py            # 文件管理器
│   │   └── config_manager.py          # 配置管理器
│   │
│   ├── views/                          # 视图层 (View)
│   │   ├── __init__.py
│   │   ├── main_window.py             # 主窗口界面
│   │   └── components/                # UI组件
│   │       ├── __init__.py
│   │       └── mapping_widget.py      # 映射组件
│   │
│   └── controllers/                    # 控制器层 (Controller)
│       ├── __init__.py
│       └── rename_controller.py       # 重命名控制器
│
├── 🔧 功能模块
│   ├── config/                         # 配置模块
│   │   └── __init__.py
│   ├── core/                          # 核心模块
│   │   └── __init__.py
│   ├── gui/                           # GUI模块
│   │   └── __init__.py
│   └── utils/                         # 工具模块
│       └── __init__.py
│
├── 🚀 启动脚本
│   ├── 启动映射工具.bat               # 主启动器（批处理）
│   ├── 启动映射工具.ps1               # 主启动器（PowerShell）
│   ├── 启动工具.bat                   # 通用启动器
│   ├── 启动工具.ps1                   # 通用启动器（PowerShell）
│   ├── 运行程序.bat                   # 直接运行脚本
│   ├── 运行程序.ps1                   # 直接运行脚本（PowerShell）
│   └── 安装检查.bat                   # 环境检查脚本
│
├── 📖 文档文件
│   ├── README.md                      # 项目说明（GitHub主页）
│   ├── PROJECT_STRUCTURE.md           # 项目结构说明（本文件）
│   ├── CONTRIBUTING.md                # 贡献指南
│   ├── CHANGELOG.md                   # 版本变更记录
│   ├── LICENSE                        # MIT许可证
│   ├── 项目说明.md                    # 详细项目说明
│   ├── 使用说明.txt                   # 快速使用指南
│   └── 简单使用说明.txt               # 简化使用说明
│
├── ⚙️ 配置文件
│   ├── requirements.txt               # 依赖包列表
│   ├── setup.py                      # 安装配置
│   └── .gitignore                    # Git忽略文件
│
├── 📂 运行时目录（自动创建）
│   └── mapping_configs/               # 映射配置存储目录
│
└── 🐍 虚拟环境（开发时）
    └── venv/                          # Python虚拟环境
```

## 🏗️ 架构设计

### MVC模式说明

项目采用经典的MVC（Model-View-Controller）架构模式：

#### Model (模型层) - `models/`
负责数据管理和业务逻辑：

- **`file_manager.py`**: 文件操作核心类
  - 文件列表获取
  - 文件重命名操作
  - 目录管理
  - 错误处理

- **`config_manager.py`**: 配置管理类
  - 映射规则保存/加载
  - 配置文件管理
  - 设置持久化

#### View (视图层) - `views/`
负责用户界面和用户交互：

- **`main_window.py`**: 主窗口界面
  - 整体布局管理
  - 用户交互处理
  - 界面更新

- **`components/mapping_widget.py`**: 映射组件
  - 映射规则编辑界面
  - 规则列表管理
  - 实时预览

#### Controller (控制器层) - `controllers/`
负责协调模型和视图：

- **`rename_controller.py`**: 重命名控制器
  - 业务逻辑处理
  - 模型和视图协调
  - 操作流程控制

### 模块化设计

#### 功能模块 - `config/`, `core/`, `gui/`, `utils/`
为未来扩展预留的模块：

- **`config/`**: 配置相关功能
- **`core/`**: 核心业务逻辑
- **`gui/`**: GUI相关工具
- **`utils/`**: 通用工具函数

## 📋 文件说明

### 核心文件

| 文件 | 作用 | 说明 |
|------|------|------|
| `app.py` | 主应用程序 | 应用程序主类，MVC架构的入口点 |
| `main.py` | 启动入口 | 程序启动入口，调用app.py |
| `simple_main.py` | 简化入口 | 简化版启动入口，用于快速测试 |

### 启动脚本

| 脚本 | 平台 | 作用 |
|------|------|------|
| `启动映射工具.bat` | Windows | 主启动器（批处理版本） |
| `启动映射工具.ps1` | Windows | 主启动器（PowerShell版本） |
| `安装检查.bat` | Windows | 环境检查和诊断工具 |

### 文档文件

| 文件 | 作用 | 目标用户 |
|------|------|----------|
| `README.md` | 项目主页 | GitHub用户 |
| `PROJECT_STRUCTURE.md` | 结构说明 | 开发者 |
| `CONTRIBUTING.md` | 贡献指南 | 贡献者 |
| `CHANGELOG.md` | 版本记录 | 所有用户 |
| `项目说明.md` | 详细说明 | 中文用户 |

## 🔄 数据流

### 用户操作流程

```
用户操作 → View → Controller → Model → 文件系统
    ↑                              ↓
    ← View ← Controller ← Model ← 结果反馈
```

### 具体流程

1. **用户选择文件夹** → `MainWindow` → `RenameController` → `FileManager`
2. **用户设置规则** → `MappingWidget` → `RenameController` → `ConfigManager`
3. **用户预览效果** → `MainWindow` → `RenameController` → `FileManager`
4. **用户执行重命名** → `MainWindow` → `RenameController` → `FileManager`

## 🎯 设计原则

### 1. 单一职责原则
每个类和模块都有明确的单一职责：
- `FileManager`: 只负责文件操作
- `ConfigManager`: 只负责配置管理
- `MappingWidget`: 只负责映射规则编辑

### 2. 开闭原则
系统对扩展开放，对修改封闭：
- 可以轻松添加新的重命名规则类型
- 可以添加新的UI组件
- 可以扩展配置管理功能

### 3. 依赖倒置原则
高层模块不依赖低层模块，都依赖于抽象：
- Controller依赖Model和View的接口
- 具体实现可以替换

### 4. 接口隔离原则
客户端不应该依赖它不需要的接口：
- 每个组件只暴露必要的接口
- 避免臃肿的接口设计

## 🚀 扩展指南

### 添加新功能

1. **确定功能位置**：
   - 数据相关 → `models/`
   - 界面相关 → `views/`
   - 逻辑相关 → `controllers/`

2. **创建新文件**：
   ```python
   # 在相应目录下创建新文件
   # 遵循现有的命名规范
   ```

3. **更新导入**：
   ```python
   # 在__init__.py中添加导入
   # 在app.py中集成新功能
   ```

### 添加新组件

1. **创建组件类**：
   ```python
   class NewWidget:
       def __init__(self, parent):
           self.parent = parent
           self.setup_ui()
   ```

2. **集成到主界面**：
   ```python
   # 在MainWindow中添加组件
   self.new_widget = NewWidget(self)
   ```

## 📝 开发规范

### 命名规范
- **文件名**: 使用小写字母和下划线 (`file_manager.py`)
- **类名**: 使用大驼峰命名 (`FileManager`)
- **函数名**: 使用小写字母和下划线 (`get_file_list`)
- **变量名**: 使用小写字母和下划线 (`file_path`)

### 代码组织
- 每个文件包含一个主要类
- 相关功能放在同一个模块中
- 使用类型提示提高代码可读性

### 文档规范
- 每个类和方法都有文档字符串
- 使用Google风格的文档字符串
- 重要功能添加使用示例

## 🔍 调试和测试

### 调试技巧
1. 使用Python内置的`logging`模块
2. 在关键位置添加断点
3. 使用IDE的调试功能

### 测试建议
1. 为每个模块编写单元测试
2. 测试边界条件和异常情况
3. 使用模拟对象测试文件操作

---

这个项目结构设计遵循了软件工程的最佳实践，具有良好的可维护性、可扩展性和可测试性。
