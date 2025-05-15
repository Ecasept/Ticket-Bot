import datetime


class Logger:
    def __init__(self, filename: str):
        self.filename = filename

    def log(self, level: str, tag: str, message: str):
        now = datetime.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M:%S")

        msg = f"{t} [{level}] <{tag}> {message}\n"

        print(msg, end='')

        with open(self.filename, 'a') as file:
            file.write(msg)

    def debug(self, tag: str, message: str):
        self.log("DEBUG", tag, message)

    def info(self, tag: str, message: str):
        self.log("INFO", tag, message)

    def warning(self, tag: str, message: str):
        self.log("WARNING", tag, message)

    def error(self, tag: str, message: str):
        self.log("ERROR", tag, message)
