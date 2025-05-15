import datetime


class Logger:
    def __init__(self, filename: str):
        self.filename = filename

    def log(self, tag: str, message: str):
        now = datetime.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M:%S")

        msg = f"{t} [{tag}] {message}\n"

        print(msg, end='')

        with open(self.filename, 'a') as file:
            file.write(msg)

    def debug(self, message: str):
        self.log("DEBUG", message)

    def info(self, message: str):
        self.log("INFO", message)

    def warning(self, message: str):
        self.log("WARNING", message)

    def error(self, message: str):
        self.log("ERROR", message)
