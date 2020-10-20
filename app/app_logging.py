import os
import sys
import logging
import structlog
import time
from collections import OrderedDict
from pythonjsonlogger import jsonlogger

service = 'rhui'

# Standard fields on logging records that we don't want directly inserted into the data dictionary
ignored_fields = ('args', 'asctime', 'created', 'exc_info', 'exc_text',
                  'filename', 'funcName', 'levelname', 'levelno', 'lineno',
                  'module', 'msecs', 'message', 'msg', 'name', 'pathname',
                  'process', 'processName', 'relativeCreated', 'stack_info',
                  'thread', 'threadName', 'extra')


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    lib_dir = os.path.normpath(os.path.split(sys.executable)[0] + '/..')
    cw_dir = os.getcwd()

    def formatTime(self, record, datefmt=None):

        # Return the creation time of the specified LogRecord as formatted text, overriding the
        # superclass version to ensure that millisecond granularity is recorded.

        # The superclass version only has second granularity since that is all time.strftime provides.
        # This method combines the millisecond parts of the time, with the formatted time (to second granularity)
        # to provide a millisecond formatted result.

        date_format = '%Y-%m-%dT%H:%M:%S'
        msec_format = '%s.%03d'
        ct = self.converter(record.created)
        t = time.strftime(date_format, ct)
        return msec_format % (t, record.msecs)

    def add_fields(self, log_record, record, message_dict):
        def map_into(dict_from, old_name, dict_into, new_name):
            if old_name not in dict_from:
                # No old name, ignore it.
                return
            if new_name in dict_into:
                if dict_from[old_name] == dict_into[new_name]:
                    # Delete the old name, it's identical.
                    del dict_from[old_name]
                # Othewise, leave both entries. We don't want to lose data.
            else:
                # Copy the record and delete the old one
                dict_into[new_name] = dict_from[old_name]
                del dict_from[old_name]

        def extract(dict_from, name):
            if name not in dict_from:
                return None
            else:
                val = dict_from[name]
                del dict_from[name]
                return val

        def safe_update(dict_target, dict_source, prefix='_'):
            for key in dict_source:
                new_key = key
                while True:
                    if new_key in dict_target:
                        new_key = prefix + new_key
                    else:
                        dict_target[new_key] = dict_source[key]
                        break

        data = OrderedDict()
        log_record.clear()

        # # Created, Service, Level
        log_record['created'] = record.asctime
        log_record['service'] = service
        log_record['level'] = record.levelname

        # # Process the file name early, because we need it later
        if record.pathname and record.pathname.startswith(self.cw_dir):
            file_name = '(pwd)' + record.pathname[len(self.cw_dir):]
            internal = True
        elif record.pathname and record.pathname.startswith(self.lib_dir):
            file_name = '(python)' + record.pathname[len(self.lib_dir):]
            internal = False
        else:
            file_name = '(no source)'
            internal = True

        # # Event
        if internal:
            if message_dict:
                if 'message' in message_dict:
                    log_record['event'] = message_dict['message']
                    del message_dict['message']
                elif 'event' in message_dict:
                    log_record['event'] = message_dict['event']
                    del message_dict['event']
                else:
                    log_record['event'] = 'No event supplied'
            else:
                log_record['event'] = record.message
        else:
            # we can't rely on the library giving us a static string.
            log_record['event'] = 'External from ' + record.name
            # since we didn't use this, we must map it to data.
            data['message'] = record.message

        # # Context
        # Currently, we don't have enough good data to use for a context
        log_record['context'] = ''

        # # Data
        # Custom field - source
        logger_name = record.name or '(no logger)'
        module = record.module or '(no module)'
        line_no = str(record.lineno) if record.lineno else '(no line)'
        # Uses the file name from the section above
        data['source'] = ':'.join([logger_name, module, file_name, line_no])

        # Raw additions on the main record object
        raw_data = {
            k: v
            for k, v in record.__dict__.items()
            if (k not in ignored_fields
                and not (hasattr(k, 'startswith') and k.startswith('_')))
        }
        safe_update(data, raw_data, 'raw_')
        # Additions through the message dictionary
        safe_update(data, message_dict, 'message_')
        # Additions through the extra key of the main record object
        if hasattr(record, 'extra'):
            safe_update(data, record.extra, 'extra_')
        log_record['data'] = data


def logger_initial_config(log_level=os.getenv('LOG_LEVEL', 'INFO'),
                          ext_log_level=os.getenv('EXT_LOG_LEVEL', 'WARN')):
    format = '(message) (asctime) (levelname) (pathname) (lineno) (module) (funcName)'
    json_handler = logging.StreamHandler(sys.stdout)
    json_handler.setFormatter(CustomJsonFormatter(format))

    logging.basicConfig(
        handlers=[json_handler],
        level=logging.getLevelName(ext_log_level),
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            # structlog.stdlib.PositionalArgumentsFormatter(),
            # structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.render_to_log_kwargs,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logger = structlog.get_logger('respondent-home')
    logger.setLevel(log_level)
    logger.info('logging configured',
                log_level=log_level,
                ext_log_level=ext_log_level)
