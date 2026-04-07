import argparse
import json
import sys
import os
from datetime import datetime

# Добавляем корневую папку в пути, чтобы импортировать модули из 'core'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.agents import AgentNetwork
from core.strategies import get_strategy

def main():
    parser = argparse.ArgumentParser(
        description="🤖 TON Gas Optimizer CLI (Headless Mode)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("--ops", type=int, default=5, 
                        help="Количество операций для пакетной отправки (по умолчанию 5)")
    parser.add_argument("--strategy", type=str, default="default", choices=["default", "aggressive"], 
                        help="Стратегия оптимизации (по умолчанию default)")
    parser.add_argument("--gas", type=int, default=5000, 
                        help="Текущая цена газа в nano-TON (по умолчанию 5000)")
    parser.add_argument("--load", type=int, default=40, 
                        help="Нагрузка на сеть в %% (0-100, по умолчанию 40)")
    parser.add_argument("--balance", type=float, default=0.0, 
                        help="Баланс кошелька в TON (по умолчанию 0.0)")
    parser.add_argument("--output", type=str, default="json", choices=["json", "text"], 
                        help="Формат вывода: json или text (по умолчанию json)")

    args = parser.parse_args()

    # Инициализация компонентов
    strategy = get_strategy(args.strategy)
    network = AgentNetwork()

    # Запуск конвейера агентов
    # Note: run_pipeline возвращает словарь с ключом 'recommendation'
    pipeline_result = network.run_pipeline(args.ops, args.gas, args.load, args.balance)
    recommendation = pipeline_result["recommendation"]

    # Применение стратегии к результатам
    should_batch = strategy.should_batch(args.ops, args.load, args.gas)
    savings = strategy.estimate_savings(args.ops, args.gas, args.load)
    reason = strategy.get_reason(args.ops, args.load, args.gas)

    # Обновляем рекомендацию данными стратегии
    recommendation.update({
        "should_batch": should_batch,
        "savings_percent": savings,
        "reason": reason,
        "timestamp": datetime.now().isoformat(),
        "input_params": vars(args)
    })

    # Вывод результата
    if args.output == "json":
        # Для пайплайнов: чистый JSON
        print(json.dumps(recommendation, indent=2))
    else:
        # Для человека: читаемый текст
        print(f"\n{'='*40}")
        print(f"🤖 TON Gas Optimizer CLI Report")
        print(f"{'='*40}")
        print(f"   📅 Time:      {recommendation['timestamp']}")
        print(f"   🧠 Strategy:  {args.strategy}")
        print(f"    Gas Price: {args.gas} nano")
        print(f"   📊 Load:      {args.load}%")
        print(f"   {'='*40}")
        print(f"   🚀 Action:    {'✅ BATCH OPERATIONS' if should_batch else '❌ SEND SEPARATELY'}")
        print(f"   💰 Savings:   {savings}%")
        print(f"   💡 Reason:    {reason}")
        print(f"   🔒 Confidence:{recommendation.get('confidence', 'N/A')}%")
        print(f"{'='*40}\n")

if __name__ == "__main__":
    main()
