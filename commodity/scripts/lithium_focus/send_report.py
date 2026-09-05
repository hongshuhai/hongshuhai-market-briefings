#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用 SMTP 发送脚本 —— 商品晨报 / 硅链专题 / 锂链专题 三报共用

用法:
  python3 send_report.py --title 商品晨报 --date 2026-09-01 --html outputs/commodity_morning_2026_09_01.html
  python3 send_report.py --title 硅链专题 --date 2026-09-01 --html outputs/silicon_focus_2026_09_01.html
  python3 send_report.py --title 锂链专题 --date 2026-09-01 --html outputs/lithium_focus_2026_09_01.html

发送链路:
  smtp.qq.com:465 SSL, 授权码从 macOS Keychain 取 'QQMailAuthCode' (必须 .strip('<>'))
  收件人 hongshuhai@foxmail.com, 不抄送不 BCC
  标题格式统一: 【{title}】YYYY-MM-DD (Frank 2026-08-26 确认, 只一段不加后缀)
"""
import argparse
import smtplib
import ssl
import subprocess
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from pathlib import Path

SMTP_HOST = 'smtp.qq.com'
SMTP_PORT = 465
SMTP_USER = 'hongshuhai@foxmail.com'
TO = 'hongshuhai@foxmail.com'


def main():
    ap = argparse.ArgumentParser(description='SMTP 发送商品系报告')
    ap.add_argument('--title', required=True, help='标题前缀, 如 商品晨报/硅链专题/锂链专题')
    ap.add_argument('--date', required=True, help='主键日期 YYYY-MM-DD')
    ap.add_argument('--html', required=True, help='HTML 文件路径')
    args = ap.parse_args()

    subject = f'【{args.title}】{args.date}'
    html_path = Path(args.html)
    if not html_path.exists():
        print(f'❌ HTML 不存在: {html_path}')
        sys.exit(1)
    html_body = html_path.read_text(encoding='utf-8')
    print(f'HTML bytes: {len(html_body.encode("utf-8"))}')

    # 从 macOS Keychain 取 QQ 邮箱授权码 (记忆: 必须 .strip('<>'))
    auth_raw = subprocess.check_output(
        ['security', 'find-generic-password', '-s', 'QQMailAuthCode', '-w'],
        text=True
    ).strip()
    password = auth_raw.strip('<>')
    if not password:
        print('❌ 授权码为空, 请检查 Keychain QQMailAuthCode')
        sys.exit(1)
    print(f'Auth code retrieved, length={len(password)}')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = TO
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))

    ctx = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=30) as server:
            server.login(SMTP_USER, password)
            server.send_message(msg)
        print(f'✅ 邮件已发送: {TO}')
        print(f'主题: {subject}')
    except Exception as e:
        print(f'❌ 发送失败: {e}')
        print('回退方案: mcp__qq-mail__SendMessage (注意 to 数组包装 bug) 或留在 outputs/ 备份交付')
        raise


if __name__ == '__main__':
    main()
