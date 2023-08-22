def _ignore_warnings():
    import logging
    import warnings

    logging.captureWarnings(True)
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        message="Deprecated call to `pkg_resources.declare_namespace('google')`.",
    )


__version__ = '0.0.7.dev53'


_ignore_warnings()

from .utils import (
    JinaAPIKeyHeader,
    JinaAuthDependency,
    JinaAuthMiddleware,
    JinaBlobStorage,
)
