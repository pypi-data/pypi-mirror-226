# -*- coding: utf-8 -*-
# MinIO Python Library for Amazon S3 Compatible Cloud Storage,
# (C) 2015, 2016, 2017 MinIO, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
fano-oss-py-sdk - A fork of minio-py with some modifications.

    >>> from minio import Minio
    >>> client = Minio(
    ...     "192.168.4.19:9000",
    ...     access_key="accesskey",
    ...     secret_key="secretkey",
    ...     secure=False,
    ...     external_host="https://sample.fano.ai",
    ...     contextual_path=True,
    ... )

    >>> result = client.presigned_get_object("example", "test", is_external=True)
    >>> print(result)

:copyright: (C) 2015-2020 MinIO, Inc., 2023 Fanolabs 
:license: Apache 2.0, see LICENSE for more details.
"""

__title__ = "fano-oss-py-sdk"
__author__ = "Fano Labs"
__version__ = "7.1.18"
__license__ = "Apache 2.0"
__copyright__ = "Copyright 2015, 2016, 2017, 2018, 2019, 2020 MinIO, Inc."

# pylint: disable=unused-import
from .api import Minio
from .error import InvalidResponseError, S3Error, ServerError
from .minioadmin import MinioAdmin
