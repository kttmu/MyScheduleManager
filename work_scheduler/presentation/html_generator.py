"""
HTML Generator Module

HTMLダッシュボードを生成するモジュール
"""

from jinja2 import Template
from ..data.models import DashboardData, Task, Deliverable, Theme


class HTMLGenerator:
    """HTML生成クラス
    
    ダッシュボードデータをHTMLに変換します。
    """
    
    TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Work Scheduler Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .header h1 {
            font-size: 32px;
            margin-bottom: 5px;
        }
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .controls {
            background-color: #ecf0f1;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            display: flex;
            gap: 10px;
        }
        .section-title {
            background-color: #34495e;
            color: white;
            padding: 12px 15px;
            margin-top: 25px;
            margin-bottom: 15px;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .metric-card {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .metric-card-title {
            font-weight: bold;
            font-size: 14px;
            padding: 12px 15px;
            color: white;
        }
        .metric-card.progress .metric-card-title {
            background-color: #3498db;
        }
        .metric-card.stats .metric-card-title {
            background-color: #2ecc71;
        }
        .metric-card.info .metric-card-title {
            background-color: #e74c3c;
        }
        .metric-card-content {
            padding: 15px;
            font-size: 13px;
        }
        .metric-card-content p {
            margin: 8px 0;
        }
        .metric-value {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        }
        .chart-container {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
            min-height: 300px;
        }
        .burndown-chart {
            width: 100%;
            height: auto;
            display: block;
        }
        .chart-legend {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 10px;
            font-size: 13px;
            color: #555;
        }
        .legend-dot {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 6px;
        }
        .list-container {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        .list-header {
            background-color: #ecf0f1;
            padding: 12px 15px;
            font-weight: bold;
            font-size: 13px;
            border-bottom: 1px solid #ddd;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 10px;
        }
        .list-item {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 10px;
            align-items: center;
            font-size: 13px;
        }
        .list-item:last-child {
            border-bottom: none;
        }
        .list-item:hover {
            background-color: #f9f9f9;
        }
        .delayed {
            color: #e74c3c;
            font-weight: bold;
        }
        .in-progress {
            color: #f39c12;
        }
        .completed {
            color: #2ecc71;
        }
        .table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
        }
        .table th {
            background-color: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border-bottom: 2px solid #2c3e50;
        }
        .table td {
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        .table tr:hover {
            background-color: #f9f9f9;
        }
        .status-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
            color: white;
        }
        .status-on-track {
            background-color: #2ecc71;
        }
        .status-at-risk {
            background-color: #f39c12;
        }
        .status-delayed {
            background-color: #e74c3c;
        }
        .trend {
            font-size: 16px;
            font-weight: bold;
        }
        .trend-up {
            color: #2ecc71;
        }
        .trend-stable {
            color: #95a5a6;
        }
        .trend-down {
            color: #e74c3c;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #ecf0f1;
            border-radius: 3px;
            overflow: hidden;
            border: 1px solid #bdc3c7;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #3498db, #2980b9);
            transition: width 0.3s ease;
        }
        .footer {
            background-color: #34495e;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            margin-top: 40px;
            border-radius: 5px;
        }
        .empty-state {
            padding: 30px;
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
        }
        @media (max-width: 768px) {
            .metrics-grid {
                grid-template-columns: 1fr;
            }
            .list-header, .list-item {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 24px;
            }
            .table {
                font-size: 12px;
            }
            .table th, .table td {
                padding: 8px;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Work Scheduler Dashboard</h1>
        <p>Generated: {{ generated_at }}</p>
    </div>
    
    <div class="container">
        <div class="controls">
            [Filter] [Export] [Refresh] [Settings]
        </div>
        
        <div class="section-title">📈 Key Metrics</div>
        <div class="metrics-grid">
            <div class="metric-card progress">
                <div class="metric-card-title">Overall Progress</div>
                <div class="metric-card-content">
                    {{ metrics_progress_html|safe }}
                </div>
            </div>
            <div class="metric-card stats">
                <div class="metric-card-title">Task Statistics</div>
                <div class="metric-card-content">
                    {{ metrics_stats_html|safe }}
                </div>
            </div>
            <div class="metric-card info">
                <div class="metric-card-title">Key Information</div>
                <div class="metric-card-content">
                    {{ metrics_info_html|safe }}
                </div>
            </div>
        </div>
        
        <div class="section-title">📉 Burndown Chart</div>
        <div class="chart-container">
            {{ burndown_chart_html|safe }}
        </div>
        
        <div class="section-title">⚠️ Delayed Tasks & Items</div>
        <div class="list-container">
            <div class="list-header">
                <div>Item Name</div>
                <div>Type</div>
                <div>Days Delayed</div>
            </div>
            {{ delayed_items_html|safe }}
        </div>
        
        <div class="section-title">🔄 In-Progress Tasks & Items</div>
        <div class="list-container">
            <div class="list-header">
                <div>Item Name</div>
                <div>Type</div>
                <div>Progress</div>
            </div>
            {{ in_progress_items_html|safe }}
        </div>
        
        <div class="section-title">🎯 Theme Progress Overview</div>
        <table class="table">
            <thead>
                <tr>
                    <th>Theme Name</th>
                    <th>Status</th>
                    <th>Actual Progress</th>
                    <th>Planned Progress</th>
                    <th>Trend</th>
                </tr>
            </thead>
            <tbody>
                {{ theme_rows_html|safe }}
            </tbody>
        </table>
        
        <div class="footer">
            <p>Work Scheduler v1.0 | Generated: {{ generated_at }}<br>
            © 2026 Project Management System</p>
        </div>
    </div>
</body>
</html>
    """
    
    @staticmethod
    def generate(dashboard_data: DashboardData) -> str:
        """HTMLを生成
        
        Args:
            dashboard_data: ダッシュボードデータオブジェクト
        
        Returns:
            str: 生成されたHTML文字列
        """
        template = Template(HTMLGenerator.TEMPLATE)
        
        # 各セクションのHTMLを生成
        metrics_progress_html = HTMLGenerator._generate_metrics_progress(dashboard_data)
        metrics_stats_html = HTMLGenerator._generate_metrics_stats(dashboard_data)
        metrics_info_html = HTMLGenerator._generate_metrics_info(dashboard_data)
        delayed_items_html = HTMLGenerator._generate_delayed_items(dashboard_data)
        in_progress_items_html = HTMLGenerator._generate_in_progress_items(dashboard_data)
        theme_rows_html = HTMLGenerator._generate_theme_rows(dashboard_data)
        burndown_chart_html = HTMLGenerator._generate_burndown_chart(dashboard_data)
        
        html = template.render(
            metrics_progress_html=metrics_progress_html,
            metrics_stats_html=metrics_stats_html,
            metrics_info_html=metrics_info_html,
            delayed_items_html=delayed_items_html,
            in_progress_items_html=in_progress_items_html,
            theme_rows_html=theme_rows_html,
            burndown_chart_html=burndown_chart_html,
            generated_at=dashboard_data.generated_at.strftime('%Y-%m-%d %H:%M:%S')
        )
        
        return html
    
    @staticmethod
    def _generate_metrics_progress(data: DashboardData) -> str:
        """進捗メトリクスHTML生成"""
        diff = data.overall_progress - data.overall_planned_progress
        diff_color = '#2ecc71' if diff >= 0 else '#e74c3c'
        
        return f"""
        <p><strong>計画進捗:</strong></p>
        <p style="margin-left: 10px; font-size: 16px;">
            <span class="metric-value">{data.overall_planned_progress:.1f}%</span>
        </p>
        <p style="margin-top: 15px;"><strong>実績進捗:</strong></p>
        <p style="margin-left: 10px; font-size: 16px;">
            <span class="metric-value">{data.overall_progress:.1f}%</span>
        </p>
        <p style="margin-top: 15px;"><strong>差分:</strong></p>
        <p style="margin-left: 10px; font-size: 14px; color: {diff_color};">
            {diff:+.1f}%
        </p>
        """
    
    @staticmethod
    def _generate_metrics_stats(data: DashboardData) -> str:
        """タスク統計HTML生成"""
        total = data.total_tasks_count
        completed = data.completed_tasks_count
        in_progress = data.in_progress_tasks_count
        not_started = data.not_started_tasks_count
        
        completed_pct = (completed / total * 100) if total > 0 else 0
        in_progress_pct = (in_progress / total * 100) if total > 0 else 0
        not_started_pct = (not_started / total * 100) if total > 0 else 0
        
        return f"""
        <p>• <strong>Total Tasks:</strong> <span class="metric-value">{total}</span></p>
        <p>• <strong>Completed:</strong> {completed} ({completed_pct:.0f}%)</p>
        <p>• <strong>In Progress:</strong> {in_progress} ({in_progress_pct:.0f}%)</p>
        <p>• <strong>Not Started:</strong> {not_started} ({not_started_pct:.0f}%)</p>
        """
    
    @staticmethod
    def _generate_metrics_info(data: DashboardData) -> str:
        """情報メトリクスHTML生成"""
        delayed_count = data.delayed_tasks_count
        
        return f"""
        <p>• <strong>Last Updated:</strong> {data.generated_at.strftime('%Y-%m-%d')}</p>
        <p>• <strong>Delayed Items:</strong> <span class="delayed">{delayed_count}</span></p>
        <p>• <strong>Status:</strong> Monitoring</p>
        """
    
    @staticmethod
    def _generate_burndown_chart(data: DashboardData) -> str:
        """日付軸付きの累積進捗バーンダウンチャートを生成"""
        from datetime import date

        if data.themes:
            start_date = min(theme.start_date.date() for theme in data.themes)
            end_date = max(theme.end_date.date() for theme in data.themes)
        else:
            start_date = data.generated_at.date()
            end_date = data.generated_at.date()

        current_date = data.generated_at.date()
        if end_date < start_date:
            end_date = start_date

        total_days = (end_date - start_date).days
        if total_days < 1:
            total_days = 1

        width = 760
        height = 320
        margin_left = 60
        margin_right = 40
        margin_top = 40
        margin_bottom = 70
        plot_width = width - margin_left - margin_right
        plot_height = height - margin_top - margin_bottom

        def y(value: float) -> float:
            return margin_top + plot_height * (1 - (value / 100.0))

        def x_for_date(target_date: date) -> float:
            delta = (target_date - start_date).days
            if delta < 0:
                delta = 0
            if delta > total_days:
                delta = total_days
            return margin_left + (delta / total_days) * plot_width

        # 目盛り用の日付ポイントを作成
        date_points = [start_date]
        for ratio in [0.25, 0.5, 0.75]:
            point_date = start_date + (end_date - start_date) * ratio
            date_points.append(point_date)
        if current_date > start_date and current_date < end_date:
            date_points.append(current_date)
        date_points.append(end_date)
        date_points = sorted(set(date_points))

        planned_points = []
        actual_points = []
        axis_labels = []

        for target_date in date_points:
            elapsed_days = max(0, (target_date - start_date).days)
            planned_progress = min(100.0, max(0.0, (elapsed_days / total_days) * 100.0))
            planned_points.append((x_for_date(target_date), y(planned_progress)))

            if target_date <= current_date:
                current_elapsed = max(0, (current_date - start_date).days)
                current_total = max(1, (end_date - start_date).days)
                current_progress = max(0.0, min(100.0, data.overall_progress))
                if current_elapsed <= 0:
                    actual_progress = 0.0
                else:
                    actual_progress = min(100.0, current_progress * (elapsed_days / current_elapsed))
            else:
                remaining_days = max(1, (end_date - current_date).days)
                current_progress = max(0.0, min(100.0, data.overall_progress))
                actual_progress = current_progress + ((100.0 - current_progress) * ((elapsed_days - max(0, (current_date - start_date).days)) / remaining_days))

            actual_points.append((x_for_date(target_date), y(actual_progress)))
            axis_labels.append((x_for_date(target_date), target_date.strftime('%m/%d')))

        planned_polyline = " ".join(f"{x:.1f},{y_val:.1f}" for x, y_val in planned_points)
        actual_polyline = " ".join(f"{x:.1f},{y_val:.1f}" for x, y_val in actual_points)

        current_x = x_for_date(current_date)
        current_progress_display = max(0.0, min(100.0, data.overall_progress))
        current_label = current_date.strftime('%Y-%m-%d')

        chart_svg = [
            f'<svg class="burndown-chart" viewBox="0 0 {width} {height}" role="img" aria-label="Cumulative progress burndown chart">',
            f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"></rect>',
            f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height - margin_bottom}" stroke="#bdc3c7" stroke-width="2"></line>',
            f'<line x1="{margin_left}" y1="{height - margin_bottom}" x2="{width - margin_right}" y2="{height - margin_bottom}" stroke="#bdc3c7" stroke-width="2"></line>',
            f'<line x1="{margin_left}" y1="{y(100)}" x2="{width - margin_right}" y2="{y(100)}" stroke="#eaf2f8" stroke-width="1"></line>',
            f'<line x1="{margin_left}" y1="{y(50)}" x2="{width - margin_right}" y2="{y(50)}" stroke="#eaf2f8" stroke-width="1"></line>',
            f'<line x1="{margin_left}" y1="{y(0)}" x2="{width - margin_right}" y2="{y(0)}" stroke="#eaf2f8" stroke-width="1"></line>',
            f'<polyline points="{planned_polyline}" fill="none" stroke="#3498db" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"></polyline>',
            f'<polyline points="{actual_polyline}" fill="none" stroke="#e74c3c" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"></polyline>',
            f'<line x1="{current_x}" y1="{margin_top}" x2="{current_x}" y2="{height - margin_bottom}" stroke="#e74c3c" stroke-width="2" stroke-dasharray="6 6"></line>',
            f'<text x="{current_x + 6}" y="{margin_top - 10}" font-size="12" fill="#e74c3c">作成日: {current_label}</text>',
        ]

        for x, label in axis_labels:
            chart_svg.append(f'<text x="{x:.1f}" y="{height - margin_bottom + 24}" font-size="12" text-anchor="middle" fill="#34495e">{label}</text>')

        chart_svg.extend([
            '<text x="20" y="60" font-size="12" fill="#34495e">100%</text>',
            '<text x="20" y="170" font-size="12" fill="#34495e">50%</text>',
            '<text x="20" y="285" font-size="12" fill="#34495e">0%</text>',
            f'<circle cx="{current_x}" cy="{y(current_progress_display)}" r="6" fill="#e74c3c"></circle>',
            '<text x="120" y="20" font-size="12" fill="#34495e">累積進捗（初期0% → 最終100%）</text>',
            '</svg>',
        ])

        return "\n".join(chart_svg) + f"""
        <div class="chart-legend">
            <div><span class="legend-dot" style="background:#3498db"></span>計画進捗（累積）</div>
            <div><span class="legend-dot" style="background:#e74c3c"></span>実績進捗（累積）</div>
            <div><span class="legend-dot" style="background:#e74c3c"></span>赤点線: HTML作成日</div>
        </div>
        """

    @staticmethod
    def _generate_delayed_items(data: DashboardData) -> str:
        """遅延アイテムリストHTML生成"""
        if not data.delayed_items:
            return '<div class="empty-state">No delayed items</div>'
        
        html = ""
        for item_type, item in data.delayed_items:
            if isinstance(item, Task):
                name = item.name
                days = item.days_delayed
                html += f'''
                <div class="list-item">
                    <div><strong>{name}</strong></div>
                    <div>Task</div>
                    <div class="delayed">{days} days</div>
                </div>
                '''
        
        return html if html else '<div class="empty-state">No delayed tasks</div>'
    
    @staticmethod
    def _generate_in_progress_items(data: DashboardData) -> str:
        """進行中アイテムリストHTML生成"""
        if not data.in_progress_items:
            return '<div class="empty-state">No in-progress items</div>'
        
        html = ""
        for item_type, item in data.in_progress_items:
            if isinstance(item, Task):
                name = item.name
                progress = item.progress
                html += f'''
                <div class="list-item">
                    <div><strong>{name}</strong></div>
                    <div>Task</div>
                    <div>
                        <div class="progress-bar" style="width: 60px;">
                            <div class="progress-fill" style="width: {progress}%;"></div>
                        </div>
                        {progress:.0f}%
                    </div>
                </div>
                '''
        
        return html if html else '<div class="empty-state">No in-progress tasks</div>'
    
    @staticmethod
    def _generate_theme_rows(data: DashboardData) -> str:
        """テーマ行HTML生成"""
        html = ""
        
        for theme in data.themes:
            status_class = f"status-{theme.status.lower().replace(' ', '-')}"
            
            # トレンド判定
            diff = theme.overall_progress - theme.planned_progress
            if diff >= 0:
                trend = '<span class="trend trend-up">↑</span>'
            elif diff >= -10:
                trend = '<span class="trend trend-stable">→</span>'
            else:
                trend = '<span class="trend trend-down">↓</span>'
            
            html += f'''
            <tr>
                <td><strong>{theme.name}</strong></td>
                <td><span class="status-badge {status_class}">{theme.status}</span></td>
                <td>
                    <div class="progress-bar" style="width: 80px; margin-bottom: 5px;">
                        <div class="progress-fill" style="width: {theme.overall_progress:.1f}%;"></div>
                    </div>
                    {theme.overall_progress:.1f}%
                </td>
                <td>{theme.planned_progress:.1f}%</td>
                <td>{trend}</td>
            </tr>
            '''
        
        return html if html else '<tr><td colspan="5" class="empty-state">No themes</td></tr>'
