#!/usr/bin/env python3
"""
シミュレーション用データ生成スクリプト
/input/0000.datの値を使用して、settings.jsonの設定に基づき
複数のデータファイルをresult/ディレクトリに生成します
"""

import json
import os
import sys
import csv
import math


def main():
    # inputディレクトリの存在確認
    input_dir = "input"
    if not os.path.exists(input_dir):
        print(f"エラー: {input_dir}/ ディレクトリが存在しません", file=sys.stderr)
        sys.exit(1)
    
    # settings.jsonの読み込み
    settings_path = os.path.join(input_dir, "settings.json")
    if not os.path.exists(settings_path):
        print(f"エラー: {settings_path} が存在しません", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        endtime = float(settings["endtime"])
        dt = float(settings["dt"])
        number = int(settings["number"])
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"エラー: settings.jsonの読み込みに失敗しました: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 0000.datの読み込み
    data_path = os.path.join(input_dir, "0000.dat")
    if not os.path.exists(data_path):
        print(f"エラー: {data_path} が存在しません", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(data_path, 'r') as f:
            base_value = float(f.read().strip())
    except (ValueError, IOError) as e:
        print(f"エラー: {data_path}の読み込みに失敗しました: {e}", file=sys.stderr)
        sys.exit(1)
    
    # resultディレクトリの作成
    result_dir = "result"
    os.makedirs(result_dir, exist_ok=True)
    
    # ファイル生成数の計算
    num_files = int(endtime / dt)
    
    print(f"設定情報:")
    print(f"  endtime: {endtime}")
    print(f"  dt: {dt}")
    print(f"  number: {number}")
    print(f"  base_value: {base_value}")
    print(f"  生成ファイル数: {num_files}")
    print()
    
    # 結果サマリー用のリスト
    summary_data = []
    
    # データファイルの生成
    for i in range(1, num_files + 1):
        time = i * dt
        output_path = os.path.join(result_dir, f"{i:04d}.dat")
        
        # 時間発展のシミュレーション（例：減衰振動）
        amplitude = base_value * math.exp(-0.01 * time)
        phase = 2 * math.pi * time
        current_value = amplitude * math.cos(phase)
        
        # 各時間ステップでのデータポイント
        data_points = []
        with open(output_path, 'w') as f:
            for j in range(number):
                # 各データポイントに小さなランダム要素を追加（疑似乱数）
                noise = 0.01 * math.sin(j * 0.1 + time)
                value = current_value + noise
                data_points.append(value)
                f.write(f"{value:.6f}\n")
        
        # 統計情報の計算
        mean_value = sum(data_points) / len(data_points)
        max_value = max(data_points)
        min_value = min(data_points)
        std_dev = math.sqrt(sum((x - mean_value)**2 for x in data_points) / len(data_points))
        
        summary_data.append({
            'step': i,
            'time': time,
            'mean': mean_value,
            'max': max_value,
            'min': min_value,
            'std': std_dev,
            'amplitude': amplitude
        })
        
        if i % 10 == 0 or i == 1:
            print(f"生成完了: {output_path} (time={time:.2f}, mean={mean_value:.4f})")
    
    # result.csvの生成
    csv_path = os.path.join(result_dir, "result.csv")
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['step', 'time', 'mean', 'max', 'min', 'std', 'amplitude']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in summary_data:
            writer.writerow(row)
    
    print()
    print(f"全 {num_files} ファイルの生成が完了しました")
    print(f"結果サマリー: {csv_path}")


if __name__ == "__main__":
    main()