""" Django backend for file upload. """
from __future__ import absolute_import

import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.urls import reverse

from .base import BaseBackend


class Backend(BaseBackend):
    """
    Manage openassessment student files uploaded using the default django storage settings.
    """
    def get_upload_url(self, key, content_type):
        """
        Return the URL pointing to the ORA2 django storage upload endpoint.
        """
        return reverse("openassessment-django-storage", kwargs={'key': key})

    def get_download_url(self, key):
        """
        Return the django storage download URL for the given key.

        Returns None if no file exists at that location.
        """
        path = self._get_file_path(key)
        print("DOWNLOAD_PATH =======> " + path)
        print("PATH_EXIST =======> " + default_storage.exists(path))
        if default_storage.exists(path):
            return default_storage.url(path)
        return None

    def upload_file(self, key, content):
        """
        Upload the given file content to the keyed location.
        """
        path = self._get_file_path(key)
        saved_path = default_storage.save(path, ContentFile(content))
        return saved_path

    def remove_file(self, key):
        """
        Remove the file at the given keyed location.

        Returns True if the file exists, and was removed.
        Returns False if the file does not exist, and so was not removed.
        """
        path = self._get_file_path(key)
        if default_storage.exists(path):
            default_storage.delete(path)
            return True
        return False

    def _get_file_name(self, key):
        """
        Returns the name of the keyed file.

        Since the backend storage may be folders, or it may use pseudo-folders,
        make sure the filename doesn't include any path separators.
        """
        file_name = key.replace("..", "").strip("/ ")
        file_name = file_name.replace(os.sep, "_")
        return file_name

    def _get_file_path(self, key):
        """
        Returns the path to the keyed file, including the storage prefix.
        """
        path = self._get_key_name(self._get_file_name(key))
        return path
