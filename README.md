<div align="center">

# 🚀 DevPulse-AI

**AI驱动的开发者生产力智能分析引擎**

*AI-Powered Developer Productivity Intelligence Engine*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange)]()
[![GLM-5.1](https://img.shields.io/badge/AI-GLM--5.1-purple)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

## 🌐 Language / 语言

- **[English](#english)** - For English documentation
- **[简体中文](#简体中文)** - 中文文档
- **[繁體中文](#繁體中文)** - 繁體中文文檔

---

<a name="english"></a>
# 🇬🇧 English

## 🎉 Introduction

**DevPulse-AI** is a lightweight, zero-dependency terminal tool that analyzes developers' Git commit history, code change patterns, working time distribution, and other multi-dimensional data to provide personalized productivity insights and improvement suggestions.

### ✨ Key Features

- 🚀 **Zero Dependencies** - Pure Python standard library implementation, no installation required
- 🧠 **AI-Powered Insights** - Integrated with GLM-5.1 API for intelligent analysis and suggestions
- 📊 **Multi-dimensional Analysis** - Git history, code complexity, working hours, coding habits
- 🔒 **Privacy First** - Local analysis, data never uploaded, supports offline mode
- 🎨 **Beautiful TUI Dashboard** - Elegant terminal visualization interface
- 🌐 **Multi-language Support** - English, Simplified Chinese, Traditional Chinese

### 🚀 Quick Start

#### Requirements

- Python 3.8 or higher
- Git repository
- (Optional) GLM-5.1 API key for AI features

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/DevPulse-AI.git
cd DevPulse-AI

# Run directly (no installation needed)
python devpulse.py
```

#### Usage

```bash
# Analyze current directory
python devpulse.py

# Analyze specific repository
python devpulse.py -p /path/to/your/repo

# Analyze last 30 days
python devpulse.py -d 30

# Disable AI analysis
python devpulse.py --no-ai
```

#### Environment Variables

```bash
# Optional: Set GLM-5.1 API key for AI features
export GLM_API_KEY="your-api-key-here"
```

### 📖 Detailed Usage Guide

#### Analysis Dimensions

1. **Git Repository Analysis**
   - Total commits and daily average
   - Active contributors ranking
   - Weekday distribution of commits
   - Commit message patterns

2. **Code Statistics**
   - Lines of code by language
   - Comment ratio analysis
   - File count and distribution
   - Code quality indicators

3. **Productivity Scoring**
   - Commit frequency score (0-25)
   - Code volume score (0-25)
   - Documentation quality score (0-25)
   - Consistency score (0-25)
   - Overall grade (S/A/B/C/D/F)

4. **AI-Powered Insights**
   - Personalized improvement suggestions
   - Coding habit analysis
   - Work-life balance recommendations
   - Best practice guidance

### 💡 Design Philosophy

DevPulse-AI was born from the need to help developers better understand their coding patterns and productivity trends. Unlike complex IDE plugins or cloud-based analytics tools, DevPulse-AI:

- **Respects Privacy** - All analysis happens locally
- **Zero Setup** - Single Python file, run instantly
- **AI Enhanced** - Optional GLM-5.1 integration for deeper insights
- **Developer Friendly** - Terminal-native, Unix philosophy

### 📦 Deployment

Since DevPulse-AI is a pure Python script, deployment is simple:

```bash
# Make executable
chmod +x devpulse.py

# Add to PATH
sudo ln -s $(pwd)/devpulse.py /usr/local/bin/devpulse

# Run from anywhere
devpulse -p ~/my-project
```

### 🤝 Contributing

We welcome contributions! Please feel free to submit issues and pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
# 🇨🇳 简体中文

## 🎉 项目介绍

**DevPulse-AI** 是一个轻量级、零依赖的终端工具，通过分析开发者的Git提交历史、代码变更模式、工作时间分布等多维度数据，为开发者提供个性化的生产力洞察和改进建议。

### ✨ 核心特性

- 🚀 **零依赖设计** - 纯Python标准库实现，无需安装任何依赖
- 🧠 **AI驱动洞察** - 集成GLM-5.1 API，提供智能分析和建议
- 📊 **多维度分析** - Git历史、代码复杂度、工作时间、编码习惯
- 🔒 **隐私优先** - 本地分析，数据不上传，支持离线模式
- 🎨 **精美TUI仪表盘** - 优雅的终端可视化界面
- 🌐 **多语言支持** - 简体中文、繁体中文、English

### 🚀 快速开始

#### 环境要求

- Python 3.8 或更高版本
- Git 仓库
- （可选）GLM-5.1 API密钥以启用AI功能

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/DevPulse-AI.git
cd DevPulse-AI

# 直接运行（无需安装）
python devpulse.py
```

#### 使用方法

```bash
# 分析当前目录
python devpulse.py

# 分析指定仓库
python devpulse.py -p /path/to/your/repo

# 分析最近30天
python devpulse.py -d 30

# 禁用AI分析
python devpulse.py --no-ai
```

#### 环境变量

```bash
# 可选：设置GLM-5.1 API密钥以启用AI功能
export GLM_API_KEY="your-api-key-here"
```

### 📖 详细使用指南

#### 分析维度

1. **Git仓库分析**
   - 总提交数和日均提交
   - 活跃贡献者排名
   - 工作日提交分布
   - 提交信息模式分析

2. **代码统计**
   - 各编程语言代码行数
   - 注释比例分析
   - 文件数量和分布
   - 代码质量指标

3. **生产力评分**
   - 提交频率评分 (0-25)
   - 代码产出评分 (0-25)
   - 文档质量评分 (0-25)
   - 提交一致性评分 (0-25)
   - 综合等级 (S/A/B/C/D/F)

4. **AI智能洞察**
   - 个性化改进建议
   - 编码习惯分析
   - 工作与生活平衡建议
   - 最佳实践指导

### 💡 设计思路

DevPulse-AI 的诞生源于帮助开发者更好地理解自己的编码模式和生产力趋势的需求。与复杂的IDE插件或基于云的分析工具不同，DevPulse-AI：

- **尊重隐私** - 所有分析都在本地进行
- **零配置** - 单个Python文件，即刻运行
- **AI增强** - 可选的GLM-5.1集成，提供更深入的洞察
- **开发者友好** - 终端原生，遵循Unix哲学

### 📦 打包与部署

由于 DevPulse-AI 是纯Python脚本，部署非常简单：

```bash
# 添加可执行权限
chmod +x devpulse.py

# 添加到PATH
sudo ln -s $(pwd)/devpulse.py /usr/local/bin/devpulse

# 从任何地方运行
devpulse -p ~/my-project
```

### 🤝 贡献指南

我们欢迎贡献！请随时提交问题和拉取请求。

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开拉取请求

### 📄 开源协议

本项目采用 MIT 协议开源 - 详情请参阅 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
# 🇹🇼 繁體中文

## 🎉 專案介紹

**DevPulse-AI** 是一個輕量級、零依賴的終端工具，通過分析開發者的Git提交歷史、代碼變更模式、工作時間分佈等多維度數據，為開發者提供個性化的生產力洞察和改進建議。

### ✨ 核心特性

- 🚀 **零依賴設計** - 純Python標準庫實現，無需安裝任何依賴
- 🧠 **AI驅動洞察** - 集成GLM-5.1 API，提供智能分析和建議
- 📊 **多維度分析** - Git歷史、代碼複雜度、工作時間、編碼習慣
- 🔒 **隱私優先** - 本地分析，數據不上傳，支持離線模式
- 🎨 **精美TUI儀表盤** - 優雅的終端可視化界面
- 🌐 **多語言支持** - 簡體中文、繁體中文、English

### 🚀 快速開始

#### 環境要求

- Python 3.8 或更高版本
- Git 倉庫
- （可選）GLM-5.1 API密鑰以啟用AI功能

#### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/DevPulse-AI.git
cd DevPulse-AI

# 直接運行（無需安裝）
python devpulse.py
```

#### 使用方法

```bash
# 分析當前目錄
python devpulse.py

# 分析指定倉庫
python devpulse.py -p /path/to/your/repo

# 分析最近30天
python devpulse.py -d 30

# 禁用AI分析
python devpulse.py --no-ai
```

#### 環境變量

```bash
# 可選：設置GLM-5.1 API密鑰以啟用AI功能
export GLM_API_KEY="your-api-key-here"
```

### 📖 詳細使用指南

#### 分析維度

1. **Git倉庫分析**
   - 總提交數和日均提交
   - 活躍貢獻者排名
   - 工作日提交分佈
   - 提交信息模式分析

2. **代碼統計**
   - 各編程語言代碼行數
   - 註釋比例分析
   - 文件數量和分佈
   - 代碼質量指標

3. **生產力評分**
   - 提交頻率評分 (0-25)
   - 代碼產出評分 (0-25)
   - 文檔質量評分 (0-25)
   - 提交一致性評分 (0-25)
   - 綜合等級 (S/A/B/C/D/F)

4. **AI智能洞察**
   - 個性化改進建議
   - 編碼習慣分析
   - 工作與生活平衡建議
   - 最佳實踐指導

### 💡 設計思路

DevPulse-AI 的誕生源於幫助開發者更好地理解自己的編碼模式和生產力趨勢的需求。與複雜的IDE插件或基於雲的分析工具不同，DevPulse-AI：

- **尊重隱私** - 所有分析都在本地進行
- **零配置** - 單個Python文件，即刻運行
- **AI增強** - 可選的GLM-5.1集成，提供更深入的洞察
- **開發者友好** - 終端原生，遵循Unix哲學

### 📦 打包與部署

由於 DevPulse-AI 是純Python腳本，部署非常簡單：

```bash
# 添加可執行權限
chmod +x devpulse.py

# 添加到PATH
sudo ln -s $(pwd)/devpulse.py /usr/local/bin/devpulse

# 從任何地方運行
devpulse -p ~/my-project
```

### 🤝 貢獻指南

我們歡迎貢獻！請隨時提交問題和拉取請求。

1. Fork 本倉庫
2. 創建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打開拉取請求

### 📄 開源協議

本專案採用 MIT 協議開源 - 詳情請參閱 [LICENSE](LICENSE) 文件。

---

<div align="center">

**Made with ❤️ by DevPulse Team**

[⭐ Star this repo](https://github.com/gitstq/DevPulse-AI) | [🐛 Report Issue](https://github.com/gitstq/DevPulse-AI/issues) | [🤝 Contribute](https://github.com/gitstq/DevPulse-AI/pulls)

</div>
