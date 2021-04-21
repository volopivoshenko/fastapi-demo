"""
Configuration.
"""

import os


class Configuration:
    """
    Configuration.
    """

    STAGE: str = os.getenv("STAGE")
    VERSION: str = "1.0"

    PATH_TO_XGB_MODEl: str = "resources/models/xgboost.joblib"
    PATH_TO_XGB_FEATURES_SAMPLE: str = "resources/models/xgboost-features-sample.json"

    def __init__(self):
        """
        Initialize.
        """

        self.ARTIFACTORY_URL = "I am dummy URL"

        self.XGB_MODEL_URL = f"{self.ARTIFACTORY_URL}/xgboost.joblib"
        self.XGB_FEATURES_SAMPLE_URL = f"{self.ARTIFACTORY_URL}/xgboost-features-sample.json"
