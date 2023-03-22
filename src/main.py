import uvicorn

from config import cfg
from log import LOGGING


if __name__ == '__main__':
    uvicorn.run(
        'app:Service',
        reload=cfg.service.debug,
        factory=cfg.service.debug,
        host=cfg.service.host,
        port=cfg.service.port,
        lifespan='on',
        log_level=cfg.service.log_level,
        log_config=LOGGING
    )