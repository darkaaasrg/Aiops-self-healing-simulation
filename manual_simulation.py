import random
import logging
import pandas as pd
from datetime import datetime, timedelta

logging.basicConfig(
    filename='manual_system.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

random.seed(42)

TOTAL_SECONDS = 7 * 24 * 3600  # 24/7
NUM_SENSORS = 50

T_DETECT = 0.05
T_HUMAN_RESPOND = 900  # 15 хв (Диспетчер помітив помилку)
T_HUMAN_DIAGNOSE = 1200  # 20 хв (Інженер шукає причину)
T_HUMAN_FIX_SW = 600  # 10 хв (Інженер вручну рестартає софт)
T_HUMAN_FIX_SW = 600  # 10 хв (Інженер вручну рестартає софт)
T_HUMAN_FIX_HW = 2700  # 45 хв (Інженер міняє залізо)


class HumanDispatcher:
    """Клас традиційної підтримки. Тут немає бази знань і авто-лікування.
    Усе роблять люди, тому це займає багато часу."""

    def process_alert(self, sensor_id, error_type):
        """Диспетчер приймає алерт і передає інженеру (завжди довго)."""

        logging.warning(f"Dashboard: Sensor_{sensor_id} showing anomaly -> {error_type}")
        logging.info(f"Dispatcher: Noticed error. Created Ticket #INC-{random.randint(1000, 9999)}.")
        logging.info(f"Dispatcher: Assigned ticket to L2 Support. Delay: {T_HUMAN_RESPOND}s.")

        if error_type == "SOFTWARE_FREEZE":
            # Інженер лагодить софт (повільно)
            mttr = T_DETECT + T_HUMAN_RESPOND + T_HUMAN_DIAGNOSE + T_HUMAN_FIX_SW
            logging.info(f"L2_Support: Manually restarted software. Total time: {mttr}s.")
            return mttr, "L2_Support_Engineer"

        elif error_type == "HARDWARE_FAILURE":
            # Інженер міняє залізо (ще повільніше)
            mttr = T_DETECT + T_HUMAN_RESPOND + T_HUMAN_DIAGNOSE + T_HUMAN_FIX_HW
            logging.error(f"L2_Support: Replaced broken hardware. Total time: {mttr}s.")
            return mttr, "L2_Support_Engineer"


class IoTSensor:
    """Клас датчика. Абсолютно такий самий, як і в АСУ."""

    def __init__(self, sensor_id):
        self.sensor_id = sensor_id

    def trigger_failure(self, error_type, support_system):
        """Датчик ламається і відправляє алерт на дашборд диспетчера."""
        return support_system.process_alert(self.sensor_id, error_type)


print("Запуск РУЧНОЇ ООП-симуляції (Завод 24/7)...")
logging.info("--- STARTING TRADITIONAL MANUAL OOP SIMULATION ---")

helpdesk = HumanDispatcher()

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

        mttr, resolved_by = broken_sensor.trigger_failure(error_type, helpdesk)

        incidents.append({
            'timestamp': current_time,
            'type': error_type,
            'mttr_sec': mttr,
            'resolved_by': resolved_by
        })

df = pd.DataFrame(incidents)
df.to_csv('manual_results.csv', index=False)

print(f"Згенеровано {len(df)} інцидентів. Дані збережено в 'manual_results.csv'")