class Config(object):
    """
    Általános konfiguráció
    """

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Fejlesztési konfiguráció
    """

    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Éles konfiguráció
    """

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = False


class TestingConfig(Config):
    """
    Teszt konfiguráció
    """

    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
