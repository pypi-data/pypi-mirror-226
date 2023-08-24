from importlib import import_module

from django.conf import settings
from django.db.models import Exists, OuterRef

from allianceauth.services.hooks import get_extension_logger
from allianceauth.authentication.models import CharacterOwnership

logger = get_extension_logger(__name__)

_supported_apps = {
    'add_character': {
        'field_label': 'Add Character (default)',
        'add_character': lambda request, token: None,
        'scopes': ['publicData'],
        'permissions': [],
        'is_character_added': lambda character: CharacterOwnership.objects.filter(character=character).exists(),
        'is_character_added_annotation': Exists(CharacterOwnership.objects.filter(character_id=OuterRef('pk')))
    }
}

_imported = False


def import_apps():
    global _imported
    if not _imported:
        for app in settings.INSTALLED_APPS:
            if app != 'allianceauth':
                try:
                    module = import_module(f'charlink.imports.{app}')
                except ModuleNotFoundError:
                    logger.debug(f"Loading of {app} link: failed")
                else:
                    _supported_apps[app] = {
                        'field_label': module.field_label,
                        'add_character': module.add_character,
                        'scopes': module.scopes,
                        'permissions': module.permissions,
                        'is_character_added': module.is_character_added,
                        'is_character_added_annotation': module.is_character_added_annotation
                    }

                    logger.debug(f"Loading of {app} link: success")

        _imported = True

    return _supported_apps
