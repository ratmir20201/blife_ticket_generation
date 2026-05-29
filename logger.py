import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M",
    encoding="utf-8",
    handlers=[
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)
