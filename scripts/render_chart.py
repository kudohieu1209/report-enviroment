#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Template script tạo biểu đồ khoa học chuẩn mực:
- Phù hợp in ấn (300 DPI, font serif đồng bộ với LaTeX)
- Xuất cả file PDF (vector) và PNG (raster) vào figures/charts/
"""

import os
import sys
from pathlib import Path

# Đảm bảo in UTF-8 mượt mà trên Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def setup_academic_style(plt):
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 14,
        'figure.dpi': 300,
        'lines.linewidth': 2.0,
        'grid.alpha': 0.5,
        'grid.linestyle': '--'
    })

def generate_sample_charts(output_dir):
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as e:
        print(f"[ERROR] Thiếu thư viện phụ thuộc: {e}")
        print("[!] Chạy 'pip install matplotlib numpy seaborn' để sử dụng script này.")
        sys.exit(1)

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        setup_academic_style(plt)

        # 1. Biểu đồ Đường (Loss & Accuracy Curve)
        epochs = np.arange(1, 21)
        train_acc = 70 + 25 * (1 - np.exp(-epochs / 4)) + np.random.normal(0, 0.4, 20)
        val_acc = 68 + 24 * (1 - np.exp(-epochs / 5)) + np.random.normal(0, 0.6, 20)

        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.plot(epochs, train_acc, label='Huấn luyện (Train Acc)', color='#1f77b4', marker='o', markersize=4)
        ax.plot(epochs, val_acc, label='Kiểm định (Val Acc)', color='#ff7f0e', linestyle='--', marker='s', markersize=4)
        
        ax.set_title('Đồ thị Độ chính xác qua các Epoch')
        ax.set_xlabel('Số lượng Epoch')
        ax.set_ylabel('Độ chính xác (%)')
        ax.set_ylim(60, 100)
        ax.legend(loc='lower right', frameon=True)
        
        plt.tight_layout()
        fig.savefig(output_dir / 'accuracy_curve.pdf', bbox_inches='tight')
        fig.savefig(output_dir / 'accuracy_curve.png', dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"[+] Đã tạo biểu đồ: {output_dir / 'accuracy_curve.pdf'}")

        # 2. Biểu đồ Cột (Model Comparison)
        models = ['Baseline A', 'Baseline B', 'Transformer-v1', 'Đề xuất (Ours)']
        f1_scores = [82.0, 86.0, 88.5, 91.8]
        colors = ['#aec7e8', '#ffbb78', '#98df8a', '#2ca02c']

        fig, ax = plt.subplots(figsize=(6.5, 4))
        bars = ax.bar(models, f1_scores, color=colors, edgecolor='black', linewidth=0.8, width=0.55)
        
        # Hiển thị giá trị trên đỉnh cột
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax.set_title('So sánh F1-Score giữa các Mô hình')
        ax.set_ylabel('F1-Score (%)')
        ax.set_ylim(75, 96)
        
        plt.tight_layout()
        fig.savefig(output_dir / 'model_comparison.pdf', bbox_inches='tight')
        fig.savefig(output_dir / 'model_comparison.png', dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"[+] Đã tạo biểu đồ: {output_dir / 'model_comparison.pdf'}")
        
    except Exception as e:
        print(f"[ERROR] Lỗi khi tạo biểu đồ: {e}")
        sys.exit(1)

if __name__ == '__main__':
    base_dir = Path(__file__).resolve().parent.parent
    charts_dir = base_dir / 'figures' / 'charts'
    generate_sample_charts(charts_dir)
