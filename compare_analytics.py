import pandas as pd
import matplotlib.pyplot as plt

print("Завантаження даних симуляцій...")
try:
    df_manual = pd.read_csv('manual_results.csv', parse_dates=['timestamp'])
    df_auto = pd.read_csv('auto_results.csv', parse_dates=['timestamp'])
except FileNotFoundError:
    print("Помилка: Спочатку запустіть файли manual_simulation.py та auto_simulation.py!")
    exit()

df_manual['day'] = df_manual['timestamp'].dt.date
df_auto['day'] = df_auto['timestamp'].dt.date

manual_daily = df_manual.groupby('day')['mttr_sec'].sum() / 3600
auto_daily = df_auto.groupby('day')['mttr_sec'].sum() / 3600

total_manual_hours = df_manual['mttr_sec'].sum() / 3600
total_auto_hours = df_auto['mttr_sec'].sum() / 3600
saved_hours = total_manual_hours - total_auto_hours
efficiency_percent = (saved_hours / total_manual_hours) * 100

print("\n" + "="*65)
print("НАУКОВИЙ ВИСНОВОК: ОЦІНКА ЕФЕКТИВНОСТІ АВТОМАТИЗАЦІЇ (24/7)")
print("="*65)
print(f"Аналіз на основі парадигми AIRS (Automated Incident Response):")
print(f"1. Загальна кількість аварій на заводі за 7 діб: {len(df_manual)}")
print(f"2. Час простою при ручному керуванні: {total_manual_hours:.2f} годин")
print(f"3. Час простою з інноваційною АСУ: {total_auto_hours:.2f} годин\n")
print(f"РЕЗУЛЬТАТ: Розроблена система повністю бере на себе дрібні")
print(f"програмні збої (працюючи навіть вночі), залишаючи людям лише")
print(f"складні апаратні заміни. Це дозволило зекономити {saved_hours:.2f} годин.")
print(f"ЕФЕКТИВНІСТЬ ПІДВИЩЕНА НА: {efficiency_percent:.2f}%!")
print("="*65)

plt.figure(figsize=(11, 6))

plt.plot(manual_daily.index, manual_daily.values,
         marker='o', color='#e74c3c', linewidth=2.5, label='Традиційна парадигма (Ручна обробка інцидентів)')

plt.plot(auto_daily.index, auto_daily.values,
         marker='s', color='#2ecc71', linewidth=2.5, label='Інноваційна АСУ (Zero-Touch Self-Healing)')

plt.fill_between(manual_daily.index, auto_daily.values, manual_daily.values, color='green', alpha=0.15)

plt.title('Аналіз Downtime в режимі 24/7: Людина vs Автоматизована АСУ', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Дні проведення дослідження', fontsize=12)
plt.ylabel('Щодобовий час простою обладнання (Години)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.ylim(bottom=0, top=max(manual_daily.values) + 2)

plt.legend(fontsize=11)
plt.tight_layout()

plt.savefig('final_24_7_comparison.png', dpi=300)
print("\n-> Спільний графік збережено у 'final_24_7_comparison.png'")
plt.show()