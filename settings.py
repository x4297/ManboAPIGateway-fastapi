from private_settings import(
    CommonConfig as _CommonConfig,
    App1Config as _App1Config,
    BaseConfig as _BaseConfig
)


CommonConfig = _CommonConfig
BaseConfig = _BaseConfig


class App1Config(BaseConfig):
    application_name = "app1"

    authentication = _App1Config.authentication

    allowed_ips = _App1Config.allowed_ips

    throttle_ip_limit = 60
    throttle_ip_duration = 300
    throttle_mobile_limit = 1
    throttle_mobile_duration = 60
