import logging

logging.basicConfig(
    filename="student_mgmt.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)