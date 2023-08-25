from .base_config import LDAP
from .base_config import DevConfig as DevBaseConfig


class DevConfig(DevBaseConfig):
    ldap = LDAP(host="ldap.meka.rs")
    # user = "freenit.models.ldap.user"
