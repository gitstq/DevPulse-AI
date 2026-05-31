#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevPulse-AI 🚀 - AI驱动的开发者生产力智能分析引擎
AI-Powered Developer Productivity Intelligence Engine

一个轻量级、零依赖的终端工具，通过分析Git提交历史、代码变更模式、
工作时间分布等多维度数据，为开发者提供个性化的生产力洞察和改进建议。

Author: DevPulse Team
Version: 1.0.0
License: MIT
"""

import os
import sys
import json
import re
import subprocess
import argparse
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional, Any
import urllib.request
import urllib.error

__version__ = "1.0.0"
__author__ = "DevPulse Team"

# ANSI颜色代码
COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'dim': '\033[2m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'bg_blue': '\033[44m',
    'bg_green': '\033[42m',
    'bg_yellow': '\033[43m',
}

# 图标
ICONS = {
    'rocket': '🚀',
    'chart': '📊',
    'fire': '🔥',
    'star': '⭐',
    'clock': '⏰',
    'code': '💻',
    'git': '🔀',
    'brain': '🧠',
    'target': '🎯',
    'lightbulb': '💡',
    'warning': '⚠️',
    'check': '✅',
    'cross': '❌',
    'calendar': '📅',
    'user': '👤',
    'trophy': '🏆',
    'zap': '⚡',
}


def color(text: str, color_name: str) -> str:
    """为文本添加ANSI颜色"""
    return f"{COLORS.get(color_name, '')}{text}{COLORS['reset']}"


def icon(name: str) -> str:
    """获取图标"""
    return ICONS.get(name, '')


def print_header(title: str):
    """打印标题"""
    width = 70
    print()
    print(color("═" * width, 'cyan'))
    print(color(f"  {icon('rocket')} {title}", 'bold'))
    print(color("═" * width, 'cyan'))
    print()


def print_section(title: str, icon_name: str = 'star'):
    """打印章节标题"""
    print()
    print(color(f"{icon(icon_name)} {title}", 'bold'))
    print(color("─" * 60, 'dim'))


def print_metric(label: str, value: str, unit: str = "", color_name: str = 'white'):
    """打印指标"""
    print(f"  {label:<25} {color(value + unit, color_name):>20}")


def print_progress_bar(label: str, value: float, max_value: float = 100, width: int = 40):
    """打印进度条"""
    percentage = min(100, max(0, (value / max_value) * 100))
    filled = int(width * percentage / 100)
    bar = '█' * filled + '░' * (width - filled)
    
    if percentage >= 80:
        bar_color = 'green'
    elif percentage >= 50:
        bar_color = 'yellow'
    else:
        bar_color = 'red'
    
    print(f"  {label:<20} {color(bar, bar_color)} {percentage:>5.1f}%")


class GitAnalyzer:
    """Git仓库分析器"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = os.path.abspath(repo_path)
        self.commits: List[Dict[str, Any]] = []
        self.authors: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'commits': 0, 'additions': 0, 'deletions': 0, 'files_changed': 0,
            'commit_times': [], 'commit_messages': []
        })
        
    def run_git_command(self, args: List[str]) -> str:
        """执行Git命令"""
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return ""
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return ""
    
    def is_git_repo(self) -> bool:
        """检查是否为Git仓库"""
        return os.path.exists(os.path.join(self.repo_path, '.git')) or \
               self.run_git_command(['rev-parse', '--git-dir']) != ""
    
    def get_commits(self, days: int = 90) -> List[Dict[str, Any]]:
        """获取提交历史"""
        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # 获取提交日志
        log_format = '%H|%an|%ae|%ad|%s'
        output = self.run_git_command([
            'log', f'--since={since_date}',
            f'--pretty=format:{log_format}',
            '--date=short'
        ])
        
        if not output:
            return []
        
        commits = []
        for line in output.split('\n'):
            if '|' in line:
                parts = line.split('|', 4)
                if len(parts) >= 5:
                    commits.append({
                        'hash': parts[0],
                        'author': parts[1],
                        'email': parts[2],
                        'date': parts[3],
                        'message': parts[4]
                    })
        
        return commits
    
    def get_commit_stats(self, commit_hash: str) -> Dict[str, int]:
        """获取提交统计信息"""
        output = self.run_git_command([
            'show', '--stat', '--format=', commit_hash
        ])
        
        stats = {'additions': 0, 'deletions': 0, 'files_changed': 0}
        
        if output:
            # 解析统计信息
            lines = output.split('\n')
            for line in lines:
                if '|' in line:
                    stats['files_changed'] += 1
                    # 尝试提取行数变化
                    if '+++' in line or '---' in line:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            change_part = parts[1].strip()
                            # 简单的行数估算
                            plus_count = change_part.count('+')
                            minus_count = change_part.count('-')
                            stats['additions'] += plus_count
                            stats['deletions'] += minus_count
        
        return stats
    
    def analyze(self, days: int = 90) -> Dict[str, Any]:
        """分析Git仓库"""
        if not self.is_git_repo():
            return {'error': 'Not a git repository'}
        
        commits = self.get_commits(days)
        
        if not commits:
            return {'error': 'No commits found in the specified time range'}
        
        # 分析提交数据
        daily_commits = defaultdict(int)
        hourly_commits = defaultdict(int)
        weekday_commits = defaultdict(int)
        
        for commit in commits:
            date = commit['date']
            daily_commits[date] += 1
            
            # 解析时间（假设均匀分布）
            try:
                dt = datetime.strptime(date, '%Y-%m-%d')
                weekday_commits[dt.weekday()] += 1
            except:
                pass
            
            author = commit['author']
            self.authors[author]['commits'] += 1
            self.authors[author]['commit_messages'].append(commit['message'])
        
        # 计算统计指标
        total_commits = len(commits)
        unique_authors = len(self.authors)
        avg_commits_per_day = total_commits / days if days > 0 else 0
        
        # 找出最活跃的作者
        top_authors = sorted(
            self.authors.items(),
            key=lambda x: x[1]['commits'],
            reverse=True
        )[:5]
        
        # 计算工作日分布
        weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        weekday_distribution = {
            weekday_names[i]: weekday_commits.get(i, 0)
            for i in range(7)
        }
        
        return {
            'total_commits': total_commits,
            'unique_authors': unique_authors,
            'days_analyzed': days,
            'avg_commits_per_day': round(avg_commits_per_day, 2),
            'daily_commits': dict(daily_commits),
            'weekday_distribution': weekday_distribution,
            'top_authors': [
                {'name': name, 'commits': data['commits']}
                for name, data in top_authors
            ],
            'commits': commits
        }


class CodeAnalyzer:
    """代码分析器"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        
    def analyze_code_complexity(self) -> Dict[str, Any]:
        """分析代码复杂度"""
        stats = {
            'total_files': 0,
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'languages': defaultdict(lambda: {'files': 0, 'lines': 0})
        }
        
        # 文件扩展名到语言的映射
        lang_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.jsx': 'React', '.tsx': 'React TS', '.java': 'Java',
            '.go': 'Go', '.rs': 'Rust', '.cpp': 'C++', '.c': 'C',
            '.h': 'C/C++ Header', '.hpp': 'C++ Header', '.cs': 'C#',
            '.rb': 'Ruby', '.php': 'PHP', '.swift': 'Swift',
            '.kt': 'Kotlin', '.scala': 'Scala', '.r': 'R',
            '.m': 'Objective-C', '.mm': 'Objective-C++',
            '.html': 'HTML', '.css': 'CSS', '.scss': 'SCSS',
            '.less': 'Less', '.vue': 'Vue', '.svelte': 'Svelte',
            '.sh': 'Shell', '.bash': 'Bash', '.zsh': 'Zsh',
            '.ps1': 'PowerShell', '.sql': 'SQL', '.md': 'Markdown',
            '.json': 'JSON', '.xml': 'XML', '.yaml': 'YAML',
            '.yml': 'YAML', '.toml': 'TOML', '.ini': 'INI',
        }
        
        exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 
                       'venv', 'dist', 'build', '.idea', '.vscode',
                       'target', 'out', 'bin', 'obj'}
        
        try:
            for root, dirs, files in os.walk(self.repo_path):
                # 排除目录
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in lang_map:
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = f.readlines()
                                
                            line_count = len(lines)
                            stats['total_files'] += 1
                            stats['total_lines'] += line_count
                            
                            # 统计代码行、注释行、空行
                            code_lines = 0
                            comment_lines = 0
                            blank_lines = 0
                            
                            for line in lines:
                                stripped = line.strip()
                                if not stripped:
                                    blank_lines += 1
                                elif stripped.startswith('#') or stripped.startswith('//') or \
                                     stripped.startswith('/*') or stripped.startswith('*') or \
                                     stripped.startswith('<!--'):
                                    comment_lines += 1
                                else:
                                    code_lines += 1
                            
                            stats['code_lines'] += code_lines
                            stats['comment_lines'] += comment_lines
                            stats['blank_lines'] += blank_lines
                            
                            # 按语言统计
                            lang = lang_map[ext]
                            stats['languages'][lang]['files'] += 1
                            stats['languages'][lang]['lines'] += line_count
                            
                        except Exception:
                            pass
        except Exception as e:
            return {'error': str(e)}
        
        # 转换languages为普通dict
        stats['languages'] = dict(stats['languages'])
        
        # 计算代码质量指标
        if stats['total_lines'] > 0:
            stats['comment_ratio'] = round(stats['comment_lines'] / stats['total_lines'] * 100, 2)
        else:
            stats['comment_ratio'] = 0
        
        return stats


class ProductivityAnalyzer:
    """生产力分析器"""
    
    def __init__(self, git_data: Dict[str, Any], code_data: Dict[str, Any]):
        self.git_data = git_data
        self.code_data = code_data
        
    def calculate_productivity_score(self) -> Dict[str, Any]:
        """计算生产力评分"""
        scores = {}
        
        # 提交频率评分 (0-25)
        avg_commits = self.git_data.get('avg_commits_per_day', 0)
        if avg_commits >= 5:
            scores['commit_frequency'] = 25
        elif avg_commits >= 3:
            scores['commit_frequency'] = 20
        elif avg_commits >= 1:
            scores['commit_frequency'] = 15
        elif avg_commits >= 0.5:
            scores['commit_frequency'] = 10
        else:
            scores['commit_frequency'] = 5
        
        # 代码量评分 (0-25)
        code_lines = self.code_data.get('code_lines', 0)
        if code_lines >= 10000:
            scores['code_volume'] = 25
        elif code_lines >= 5000:
            scores['code_volume'] = 20
        elif code_lines >= 1000:
            scores['code_volume'] = 15
        elif code_lines >= 500:
            scores['code_volume'] = 10
        else:
            scores['code_volume'] = 5
        
        # 注释质量评分 (0-25)
        comment_ratio = self.code_data.get('comment_ratio', 0)
        if comment_ratio >= 20:
            scores['documentation'] = 25
        elif comment_ratio >= 10:
            scores['documentation'] = 20
        elif comment_ratio >= 5:
            scores['documentation'] = 15
        elif comment_ratio >= 2:
            scores['documentation'] = 10
        else:
            scores['documentation'] = 5
        
        # 一致性评分 (0-25) - 基于工作日分布
        weekday_dist = self.git_data.get('weekday_distribution', {})
        if weekday_dist:
            values = list(weekday_dist.values())
            if values:
                avg = sum(values) / len(values)
                variance = sum((x - avg) ** 2 for x in values) / len(values)
                consistency = max(0, 25 - variance / 10)
                scores['consistency'] = round(min(25, consistency))
            else:
                scores['consistency'] = 10
        else:
            scores['consistency'] = 10
        
        # 总分
        total_score = sum(scores.values())
        
        return {
            'total_score': total_score,
            'scores': scores,
            'grade': self._get_grade(total_score)
        }
    
    def _get_grade(self, score: int) -> str:
        """根据分数获取等级"""
        if score >= 90:
            return 'S'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 50:
            return 'D'
        else:
            return 'F'
    
    def generate_insights(self) -> List[str]:
        """生成洞察建议"""
        insights = []
        
        # 基于提交频率
        avg_commits = self.git_data.get('avg_commits_per_day', 0)
        if avg_commits < 1:
            insights.append(f"{icon('warning')} 提交频率较低，建议保持更频繁的代码提交习惯")
        elif avg_commits > 10:
            insights.append(f"{icon('fire')} 提交非常活跃！注意保持提交的质量和原子性")
        else:
            insights.append(f"{icon('check')} 提交频率良好，保持这个节奏")
        
        # 基于注释比例
        comment_ratio = self.code_data.get('comment_ratio', 0)
        if comment_ratio < 5:
            insights.append(f"{icon('warning')} 代码注释比例较低，建议增加文档说明")
        elif comment_ratio > 30:
            insights.append(f"{icon('lightbulb')} 注释丰富，但注意避免过度注释")
        else:
            insights.append(f"{icon('check')} 代码文档比例适中")
        
        # 基于工作日分布
        weekday_dist = self.git_data.get('weekday_distribution', {})
        weekend_commits = weekday_dist.get('周六', 0) + weekday_dist.get('周日', 0)
        weekday_commits = sum(v for k, v in weekday_dist.items() if k not in ['周六', '周日'])
        
        if weekend_commits > weekday_commits / 2:
            insights.append(f"{icon('warning')} 周末提交较多，注意保持工作与生活平衡")
        
        # 基于代码量
        code_lines = self.code_data.get('code_lines', 0)
        if code_lines > 50000:
            insights.append(f"{icon('trophy')} 代码量庞大，考虑进行模块化重构")
        
        return insights


class AIAnalyzer:
    """AI分析器 - 集成GLM-5.1 API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GLM_API_KEY')
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    def analyze_with_ai(self, git_data: Dict[str, Any], code_data: Dict[str, Any], 
                       productivity_data: Dict[str, Any]) -> str:
        """使用AI分析数据"""
        if not self.api_key:
            return "未配置GLM API密钥，跳过AI分析。设置 GLM_API_KEY 环境变量以启用AI功能。"
        
        # 构建提示词
        prompt = self._build_prompt(git_data, code_data, productivity_data)
        
        try:
            # 调用GLM-5.1 API
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            data = {
                'model': 'glm-5.1',
                'messages': [
                    {'role': 'system', 'content': '你是一个专业的开发者生产力分析专家。请基于提供的数据给出简洁、实用的分析和建议。使用中文回复。'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 1000
            }
            
            req = urllib.request.Request(
                self.api_url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                return "AI分析失败：无法解析响应"
                
        except urllib.error.HTTPError as e:
            return f"AI分析失败：HTTP {e.code} - {e.reason}"
        except Exception as e:
            return f"AI分析失败：{str(e)}"
    
    def _build_prompt(self, git_data: Dict[str, Any], code_data: Dict[str, Any],
                     productivity_data: Dict[str, Any]) -> str:
        """构建AI提示词"""
        prompt = f"""请分析以下开发者生产力数据，给出3-5条简洁的洞察和建议：

## Git提交数据
- 总提交数：{git_data.get('total_commits', 0)}
- 分析天数：{git_data.get('days_analyzed', 0)}
- 日均提交：{git_data.get('avg_commits_per_day', 0)}
- 活跃作者数：{git_data.get('unique_authors', 0)}

## 代码统计
- 总文件数：{code_data.get('total_files', 0)}
- 代码行数：{code_data.get('code_lines', 0)}
- 注释比例：{code_data.get('comment_ratio', 0)}%
- 主要语言：{', '.join(list(code_data.get('languages', {}).keys())[:5])}

## 生产力评分
- 总分：{productivity_data.get('total_score', 0)}/100
- 等级：{productivity_data.get('grade', 'N/A')}

请给出：
1. 整体评价（1-2句话）
2. 3-5条具体改进建议
3. 鼓励性结语
"""
        return prompt


class DevPulse:
    """DevPulse主类"""
    
    def __init__(self, repo_path: str = ".", api_key: Optional[str] = None):
        self.repo_path = repo_path
        self.git_analyzer = GitAnalyzer(repo_path)
        self.code_analyzer = CodeAnalyzer(repo_path)
        self.ai_analyzer = AIAnalyzer(api_key)
        
    def run(self, days: int = 90, use_ai: bool = True):
        """运行完整分析"""
        # 打印欢迎信息
        self._print_welcome()
        
        # Git分析
        print_section("Git仓库分析", "git")
        git_data = self.git_analyzer.analyze(days)
        
        if 'error' in git_data:
            print(f"  {icon('cross')} {color(git_data['error'], 'red')}")
            return
        
        self._print_git_stats(git_data)
        
        # 代码分析
        print_section("代码统计分析", "code")
        code_data = self.code_analyzer.analyze_code_complexity()
        
        if 'error' in code_data:
            print(f"  {icon('cross')} {color(code_data['error'], 'red')}")
        else:
            self._print_code_stats(code_data)
        
        # 生产力分析
        print_section("生产力评分", "trophy")
        productivity_analyzer = ProductivityAnalyzer(git_data, code_data)
        productivity_data = productivity_analyzer.calculate_productivity_score()
        self._print_productivity_score(productivity_data)
        
        # 洞察建议
        print_section("智能洞察", "brain")
        insights = productivity_analyzer.generate_insights()
        for insight in insights:
            print(f"  {insight}")
        
        # AI分析
        if use_ai:
            print_section("AI深度分析", "lightbulb")
            ai_result = self.ai_analyzer.analyze_with_ai(git_data, code_data, productivity_data)
            print(f"  {ai_result}")
        
        # 打印结束信息
        print()
        print(color("═" * 70, 'cyan'))
        print(color(f"  {icon('rocket')} 分析完成！继续加油，成为更优秀的开发者！", 'green'))
        print(color("═" * 70, 'cyan'))
        print()
    
    def _print_welcome(self):
        """打印欢迎信息"""
        print()
        print(color("╔" + "═" * 68 + "╗", 'cyan'))
        print(color("║" + " " * 20 + f"{icon('rocket')} DevPulse-AI v{__version__}" + " " * 21 + "║", 'cyan'))
        print(color("║" + " " * 10 + "AI驱动的开发者生产力智能分析引擎" + " " * 16 + "║", 'dim'))
        print(color("╚" + "═" * 68 + "╝", 'cyan'))
        print()
    
    def _print_git_stats(self, data: Dict[str, Any]):
        """打印Git统计"""
        print_metric("总提交数", str(data.get('total_commits', 0)), "", 'green')
        print_metric("分析天数", str(data.get('days_analyzed', 0)), "天", 'blue')
        print_metric("日均提交", str(data.get('avg_commits_per_day', 0)), "次", 'yellow')
        print_metric("活跃作者", str(data.get('unique_authors', 0)), "人", 'magenta')
        
        # 工作日分布
        print()
        print(f"  {color('工作日提交分布:', 'bold')}")
        weekday_dist = data.get('weekday_distribution', {})
        max_commits = max(weekday_dist.values()) if weekday_dist else 1
        for day, count in weekday_dist.items():
            print_progress_bar(f"    {day}", count, max_commits)
        
        # 最活跃作者
        top_authors = data.get('top_authors', [])
        if top_authors:
            print()
            print(f"  {color('最活跃贡献者:', 'bold')}")
            for i, author in enumerate(top_authors[:3], 1):
                medal = ['🥇', '🥈', '🥉'][i-1] if i <= 3 else f"{i}."
                print(f"    {medal} {author['name']}: {color(str(author['commits']), 'yellow')} 次提交")
    
    def _print_code_stats(self, data: Dict[str, Any]):
        """打印代码统计"""
        print_metric("代码文件数", str(data.get('total_files', 0)), "个", 'green')
        print_metric("代码总行数", str(data.get('total_lines', 0)), "行", 'blue')
        print_metric("有效代码", str(data.get('code_lines', 0)), "行", 'cyan')
        print_metric("注释行数", str(data.get('comment_lines', 0)), "行", 'yellow')
        print_metric("注释比例", str(data.get('comment_ratio', 0)), "%", 'magenta')
        
        # 语言分布
        languages = data.get('languages', {})
        if languages:
            print()
            print(f"  {color('编程语言分布:', 'bold')}")
            sorted_langs = sorted(languages.items(), key=lambda x: x[1]['lines'], reverse=True)
            max_lines = sorted_langs[0][1]['lines'] if sorted_langs else 1
            for lang, stats in sorted_langs[:8]:
                print_progress_bar(f"    {lang}", stats['lines'], max_lines)
    
    def _print_productivity_score(self, data: Dict[str, Any]):
        """打印生产力评分"""
        total_score = data.get('total_score', 0)
        grade = data.get('grade', 'N/A')
        scores = data.get('scores', {})
        
        # 打印总分和等级
        grade_colors = {'S': 'cyan', 'A': 'green', 'B': 'blue', 'C': 'yellow', 'D': 'magenta', 'F': 'red'}
        grade_color = grade_colors.get(grade, 'white')
        
        print()
        print(f"  {color('生产力总分:', 'bold')} {color(str(total_score), grade_color)} / 100")
        print(f"  {color('综合等级:', 'bold')} {color(f'【 {grade} 】', grade_color)}")
        print()
        
        # 打印各维度评分
        print(f"  {color('各维度评分:', 'bold')}")
        for category, score in scores.items():
            category_names = {
                'commit_frequency': '提交频率',
                'code_volume': '代码产出',
                'documentation': '文档质量',
                'consistency': '提交一致性'
            }
            name = category_names.get(category, category)
            print_progress_bar(f"    {name}", score, 25)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='DevPulse-AI - AI驱动的开发者生产力智能分析引擎',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          # 分析当前目录
  %(prog)s -p /path/to/repo         # 分析指定仓库
  %(prog)s -d 30                    # 分析最近30天
  %(prog)s --no-ai                  # 禁用AI分析

环境变量:
  GLM_API_KEY    # GLM-5.1 API密钥（可选）
        """
    )
    
    parser.add_argument('-p', '--path', default='.',
                       help='仓库路径 (默认: 当前目录)')
    parser.add_argument('-d', '--days', type=int, default=90,
                       help='分析天数 (默认: 90)')
    parser.add_argument('--no-ai', action='store_true',
                       help='禁用AI分析')
    parser.add_argument('--version', action='version',
                       version=f'DevPulse-AI v{__version__}')
    
    args = parser.parse_args()
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print(f"{icon('cross')} 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 运行分析
    try:
        devpulse = DevPulse(args.path)
        devpulse.run(days=args.days, use_ai=not args.no_ai)
    except KeyboardInterrupt:
        print(f"\n\n{icon('warning')} 用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n{icon('cross')} 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
