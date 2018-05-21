from datetime import datetime
import time


class TracingMiddleware(object):
    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self):
        self.resolver_stats = list()
        self.start_time = None
        self.end_time = None

    def current_timestamp(self):
        return (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()

    def start(self):
        self.start_time = self.current_timestamp()

    def end(self):
        self.end_time = self.current_timestamp()

    @property
    def start_time_str(self):
        return datetime.fromtimestamp(self.start_time).strftime(self.DATETIME_FORMAT)

    @property
    def end_time_str(self):
        return datetime.fromtimestamp(self.end_time).strftime(self.DATETIME_FORMAT)

    @property
    def duration(self):
        if not self.end_time:
            raise ValueError("Tracing has not ended yet!")

        return (self.end_time - self.start_time) * 1e9

    @property
    def tracing_dict(self):
        return dict(
            version=1,
            startTime=self.start_time_str,
            endTime=self.end_time_str,
            duration=self.duration,
            execution=dict(
                resolvers=self.resolver_stats
            )
        )

    def resolve(self, _next, root, info, *args, **kwargs):
        start = self.current_timestamp()
        try:
            return _next(root, info, *args, **kwargs)
        finally:
            end = self.current_timestamp()
            elapsed_ns = (end - start) * 1e9

            stat = {
                "path": info.path,
                "parentType": str(info.parent_type),
                "fieldName": info.field_name,
                "returnType": str(info.return_type),
                "startOffset": (start - self.start_time) * 1e9,
                "duration": elapsed_ns,
            }
            self.resolver_stats.append(stat)
