import time 
from collections import defaultdict
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
from kube_lintd.linter import lint_file

last_linted = {}

def lint_file_debounced(path):
    now = time.time()
    if path in last_linted and now - last_linted[path] < 1:
        return  # Skip duplicate trigger within 1 second
    last_linted[path] = now
    lint_file(path)

class YAMLChangeHandler(FileSystemEventHandler):
    def __init__(self, debounce_seconds=1.0):
        self.last_run = defaultdict(float)
        self.debounce = debounce_seconds

    def _should_lint(self, path):
        now = time.time()
        last = self.last_run[path]
        if now - last < self.debounce:
            return False
        self.last_run[path] = now
        return True

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith((".yaml", ".yml")):
            if self._should_lint(event.src_path):
                lint_file_debounced(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith((".yaml", ".yml")):
            if self._should_lint(event.src_path):
                print(f"\n🔁 Detected change in {event.src_path}")
                lint_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith((".yaml", ".yml")):
            if self._should_lint(event.src_path):
                print(f"\n🆕 New file detected: {event.src_path}")
                lint_file(event.src_path)

def watch_directory(path):
    print(f"👀 Watching directory: {path}")
    event_handler = YAMLChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

