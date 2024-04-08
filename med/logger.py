import json
import logging
import re

from decouple import config

LOG = logging.getLogger(__name__)


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    LIGHTGREY = "\033[37m"
    MAGENTA = "\033[35m"


class Log:
    protected_fields = {
        "args",
        "asctime",
        "created",
        "exc_info",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "thread",
        "threadName",
    }

    @staticmethod
    def snake_case(name):
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    @staticmethod
    def _dev_log(title, title_color, exc, data, objects):
        try:
            if config("ENV") == 'development':
                print(f"{title_color}{title}{bcolors.ENDC}")
                if objects:
                    print(f"{bcolors.BOLD}__OBJECTS__{bcolors.ENDC}")
                    try:
                        for obj in objects:
                            if obj:
                                print(
                                    "{}{:<15s} {:<10s}{}".format(
                                        bcolors.OKGREEN,
                                        Log.snake_case(obj._meta.object_name),
                                        str(obj.id),
                                        bcolors.ENDC,
                                    )
                                )
                    except Exception:
                        print(f"{bcolors.OKGREEN}{str(objects)}{bcolors.ENDC}")
                if data:
                    print(f"{bcolors.BOLD}__DATA__{bcolors.ENDC}")
                    try:
                        for key, value in data:
                            json_data = json.dumps({key: value}, indent=2)
                            print(f"{bcolors.OKBLUE}{json_data}{bcolors.ENDC}")
                    except Exception:
                        print(f"{bcolors.OKBLUE}{str(data)}{bcolors.ENDC}")
                if exc:
                    print(f"{bcolors.BOLD}__EXC__{bcolors.ENDC}")
                    print(f"{bcolors.UNDERLINE}{exc}{bcolors.ENDC}")
        except Exception as exc:
            print("DEV LOG ERROR", exc)

    @staticmethod
    def get_extra(exc, data, objects):
        tags = {}
        log_errors = []

        extra = {"exc": exc}

        if objects:
            for obj in objects:
                if obj:
                    try:
                        tags[Log.snake_case(obj._meta.object_name)] = obj.id
                        extra[Log.snake_case(obj._meta.object_name)] = obj.id
                    except Exception:
                        log_errors.append(f"Invalid Object: {obj}")

        extra["sentry_tags"] = tags
        if data:
            try:
                for key, value in data.items():
                    if key != "exc" and key != "sentry_tags":
                        if key in Log.protected_fields:
                            extra[f"ERROR_{key}"] = str(value)
                        else:
                            extra[key] = str(value)
                    else:
                        log_errors.append(f"Invalid Key: {key}")
            except Exception:
                Log.debug("Invalid Data")
                log_errors.append("Invalid Data")

        if len(log_errors) > 0:
            extra["log_errors"] = log_errors

        return extra

    @staticmethod
    def error(title, exc=None, data=None, objects=None):
        title = f"Error: {title}"
        extra = Log.get_extra(exc, data, objects)

        if config("ENV") == 'development':
            Log._dev_log(title, bcolors.FAIL, exc, data, objects)
            if config("SENTRY_LOCAL", cast=bool, default=False):
                LOG.error(title, extra=extra)
        else:
            LOG.error(title, extra=extra)

    @staticmethod
    def warning(title, exc=None, data=None, objects=None):
        title = f"Warning: {title}"
        extra = Log.get_extra(exc, data, objects)

        if config("ENV") == 'development':
            Log._dev_log(title, bcolors.WARNING, exc, data, objects)
            if config("SENTRY_LOCAL", cast=bool, default=False):
                LOG.warning(title, extra=extra)
        else:
            LOG.warning(title, extra=extra)

    @staticmethod
    def info(title, exc=None, data=None, objects=None):
        title = f"Info: {title}"
        extra = Log.get_extra(exc, data, objects)

        if config("ENV") == 'development':
            Log._dev_log(title, bcolors.OKBLUE, exc, data, objects)
            if config("SENTRY_LOCAL", cast=bool, default=False):
                LOG.info(title, extra=extra)
        else:
            LOG.info(title, extra)

    @staticmethod
    def debug(title, exc=None, data=None, objects=None):
        title = f"Debug: {title}"
        extra = Log.get_extra(exc, data, objects)

        if config("ENV") == 'test':
            return

        if config("ENV") == 'development':
            Log._dev_log(title, bcolors.MAGENTA, exc, data, objects)
            if config("SENTRY_LOCAL", cast=bool, default=False):
                LOG.debug(title, extra=extra)
        else:
            LOG.debug(title, extra)
