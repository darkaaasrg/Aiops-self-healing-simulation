import random
import logging
import pandas as pd #аналітика даних
from datetime import datetime, timedelta

logging.basicConfig(
    filename='auto_system.log',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

random.seed(42) #фіксує генератор випадкових чисел

TOTAL_SECONDS = 7 * 24 * 3600  # Завод працює 24/7 (7 днів)
NUM_SENSORS = 50 #незалжені датчики

T_DETECT = 0.05
T_AUTO_FIX = 0.5  # 500 мс на авто-лікування!
T_HUMAN_RESPOND = 900  # 15 хв
T_HUMAN_DIAGNOSE = 1200  # 20 хв
T_HUMAN_FIX_HW = 2700  # 45 хв


#програмне ядро
class AIOpsSystem:
    """Клас розумної системи управління, яка приймає алерти та лікує їх."""

    def __init__(self):
        self.name = "AI Self-Healing Module"
        self.knowledge_base = ["SOFTWARE_FREEZE", "MEMORY_LEAK", "CONFIG_ERROR"]

    def process_alert(self, sensor_id, error_type):
        """Головний метод системи: прийняти рішення на основі типу помилки."""

        if error_type in self.knowledge_base:
            return self._auto_heal(sensor_id, error_type)
        else:
            return self._escalate_to_human(sensor_id, error_type)

    def _auto_heal(self, sensor_id, error_type):
        """Внутрішній метод: Система лагодить софт міттєво."""
        logging.warning(f"Sensor_{sensor_id}: Anomaly detected -> {error_type}")
        logging.info(f"System: Found solution in Knowledge Base. Executing remote patch...")

        mttr = T_DETECT + T_AUTO_FIX
        logging.info(f"System: Auto-recovery successful in {T_AUTO_FIX}s. No human needed.")
        return mttr, self.name

    def _escalate_to_human(self, sensor_id, error_type):
        """Внутрішній метод: Система передає складну апаратну задачу людині."""
        logging.error(f"Sensor_{sensor_id}: Hardware broken -> {error_type}. Escalating to Human!")
        logging.info(f"System: Ticket created and assigned to L2 Support.")

        mttr = T_DETECT + T_HUMAN_RESPOND + T_HUMAN_DIAGNOSE + T_HUMAN_FIX_HW
        return mttr, "L2_Support_Engineer"

#апаратна частина
class IoTSensor:
    """Клас датчика, який працює на заводі."""

    def __init__(self, sensor_id):
        self.sensor_id = sensor_id

    def trigger_failure(self, error_type, ai_system):
        """Датчик ламається і сам відправляє алерт до розумної системи.""" #Датчик фіксує збій
        return ai_system.process_alert(self.sensor_id, error_type)



print("Запуск АВТОМАТИЧНОЇ ООП-симуляції (Завод 24/7)...")
logging.info("--- STARTING AIOPS OOP SIMULATION (24/7 OPERATION) ---")

central_system = AIOpsSystem()

sensors = [IoTSensor(sensor_id=i) for i in range(1, NUM_SENSORS + 1)]

incidents = []
current_time = datetime(2026, 3, 2, 0, 0, 0)

for second in range(TOTAL_SECONDS):
    current_time += timedelta(seconds=1)

    if random.random() < 0.00025:
        broken_sensor_id = random.randint(1, NUM_SENSORS)
        is_hardware = random.random() < 0.2
        error_type = "HARDWARE_FAILURE" if is_hardware else "SOFTWARE_FREEZE"

        broken_sensor = sensors[broken_sensor_id - 1]

        mttr, resolved_by = broken_sensor.trigger_failure(error_type, central_system)

        incidents.append({
            'timestamp': current_time,
            'type': error_type,
            'mttr_sec': mttr,
            'resolved_by': resolved_by
        })

df = pd.DataFrame(incidents)
df.to_csv('auto_results.csv', index=False)

print(f"Згенеровано {len(df)} інцидентів. Дані збережено в 'auto_results.csv'")