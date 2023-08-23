import logging
from komora_syncer.connections.NetboxConnection import NetboxConnection


logger = logging.getLogger(__name__)


class NetboxCache():
    tenant_cache = {}
    device_cache = {}
    nb = NetboxConnection()
    nb.open()
    nb_client = nb.connection
    
    def __new__(cls):
        raise TypeError("This is a static class")
    
    @staticmethod
    def init_tenant_cache(force=False):
        if NetboxCache.tenant_cache and not force:
            return NetboxCache.tenant_cache
        
        try:
            tenants = NetboxCache.nb_client.tenancy.tenants.all()
            for tenant in tenants:
                if tenant.custom_fields.get("komora_id"):
                    NetboxCache.tenant_cache[tenant.custom_fields.get("komora_id")] = tenant   
        except Exception:
            logger.exception("Unable to initialize tenant cache")
            raise
    
    @staticmethod
    def init_device_cache(force=False):
        if NetboxCache.device_cache and not force:
            return NetboxCache.device_cache
        
        try:
            devices = NetboxCache.nb_client.dcim.devices.all()
            for device in devices:
                if device.custom_fields.get("komora_id"):
                    NetboxCache.device_cache[device.custom_fields.get("komora_id")] = device
        except Exception:
            logger.exception("Unable to initialize device cache")
            raise
                
    @staticmethod
    def get_tenant_cache():
        if not NetboxCache.tenant_cache:
            NetboxCache.init_tenant_cache()
        return NetboxCache.tenant_cache
    
    @staticmethod
    def get_device_cache():
        if not NetboxCache.device_cache:
            NetboxCache.init_device_cache()
        return NetboxCache.device_cache