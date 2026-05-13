import argparse
import pandas as pd
from experiment import run_honest_experiment, run_attack_experiment


def main():
   parser = argparse.ArgumentParser()
   parser.add_argument("--n", type=int, default=5)
   parser.add_argument("--t", type=int, default=3)
   args = parser.parse_args()

   # Честный сценарий
   print("=== ЧЕСТНЫЙ СЦЕНАРИЙ ===")
   honest = run_honest_experiment(args.n, args.t)
   print(f"Шамир:      {honest['shamir_correct_%']:.2f}% корректных восстановлений")
   print(f"Фельдман:   {honest['feldman_correct_%']:.2f}% корректных восстановлений")

   print("\n=== АТАКИ ===")
   results = []
   for attack in ["random", "zero", "increment", "noop"]:
       res = run_attack_experiment(args.n, args.t, attack)
       print(f"Атака '{attack}': "
             f"Шамир сломан = {res['shamir_broken_%']:.2f}%, "
             f"Фельдман обнаружил = {res['feldman_detect_%']:.2f}%")
       results.append(res)

   # Сохраняем в файл
   df = pd.DataFrame(results)
   df.to_csv("results.csv", index=False)
   print("\n=== ФАЙЛ РЕЗУЛЬТАТОВ ===")
   print("Результаты сохранены в results.csv")
   print("\nТаблица результатов:")
   print(df.to_string(index=False, float_format="%.2f"))


if __name__ == "__main__":
   main()

