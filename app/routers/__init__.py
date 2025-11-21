from fastapi import APIRouter

from . import user

router = APIRouter()

router.include_router(user.router)


# 추가 고려 가능
# import importlib
# import pkgutil

# # 3. gpt - 동적 자동스캔방식
# for _, module_name, _ in pkgutil.iter_modules(__path__):
#     module = importlib.import_module(f"{__name__}.{module_name}")
#     if hasattr(module, "router"):
#         router.include_router(module.router)
