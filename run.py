import logging
import logging.config
import os

import yaml
from app import app

logger = logging.getLogger(__name__)

def setup_logging(
    default_path='logging.yaml',
    default_level=logging.INFO
):
    """Setup logging configuration in anomaly_detection"""
    path = default_path
    print(default_path)
    fopen = open(default_path)
    fopen.close()
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
        raise SystemExit(0)


if __name__ == '__main__':
    setup_logging()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
