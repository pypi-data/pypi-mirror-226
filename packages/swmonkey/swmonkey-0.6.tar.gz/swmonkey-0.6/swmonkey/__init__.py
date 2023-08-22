# Delete old files
# Attention: this must preceed the import of logger
from .watchdog import watchdog
from .first_monkey import monkey_test
import threading
from .monitor import monkey_monitor
from .prepare import clean
clean()


DURATION = 10  # Duration in seconds
# DURATION = 60 * 60 * 10  # Duration in seconds
TIME_DIFF_SCALE = 0.1


# Start monitor in a sperated thread
monitor_thread = threading.Thread(target=monkey_monitor, daemon=True)
monitor_thread.start()

# TODO: refactor this
watchdog(monkey_test, DURATION + TIME_DIFF_SCALE * DURATION, DURATION)
