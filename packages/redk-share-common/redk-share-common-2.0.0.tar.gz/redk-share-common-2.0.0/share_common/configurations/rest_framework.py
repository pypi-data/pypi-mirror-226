# 默认基础配置
DEFAULT_REST_FRAMEWORK_BASE = {
    # 1
    # "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # [public] 默认配置
    "DEFAULT_PAGINATION_CLASS": "share_common.utils.pagination.RedkernelPagination",
    "PAGE_SIZE": 10,
}

# 默认session和jwt认证
DEFAULT_REST_FRAMEWORK_AUTHENTICATION = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# 默认权限配置
DEFAULT_REST_FRAMEWORK_PERMISSION = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# session和远程jwt认证
REMOTE_REST_FRAMEWORK_AUTHENTICATION = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        # 'JWTAuthentication',
        "objectApplication.authentication.ObjectJWTAuthentication",
    ),
}


# 远程权限认证
REMOTE_REST_FRAMEWORK_PERMISSION = {
    "DEFAULT_PERMISSION_CLASSES": [
        # 'IsAuthenticated',
        "objectApplication.permissions.RemoteUserAuthPermission"
    ],
}
