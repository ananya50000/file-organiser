import time
from watchdog.observers import Observer

from agent.organizer import FileOrganizerAgent
from core.workflow import Workflow
from strategies.types import ImageStrategy
from strategies.types import DocumentStrategy
from strategies.types import AudioStrategy
from strategies.types import VideoStrategy
from strategies.types import CodeStrategy
from tasks.scan import ScanFilesTask
from tasks.classify import ClassifyFilesTask
from tasks.move import MoveFilesTask

from watcher import DownloadHandler

def build_agent():
    wf = Workflow()
    wf.add_task(ScanFilesTask("Scan"))
    wf.add_task(ClassifyFilesTask([
        ImageStrategy(),
        DocumentStrategy(),
        AudioStrategy(),
        CodeStrategy(),
        VideoStrategy()
    ]))
    wf.add_task(MoveFilesTask("Move"))
    return FileOrganizerAgent(wf)

    
if __name__ == "__main__":
    WATCH_DIR = "C:/Users/KDKCD-22/Downloads"
    
    
    agent = build_agent()
    
    agent.organize(WATCH_DIR)
    
    observer = Observer()
    
    observer.schedule(DownloadHandler(agent,WATCH_DIR), WATCH_DIR, recursive=False)
    
    observer.start()
    print(f"Watching directory: {WATCH_DIR}")
    
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
            