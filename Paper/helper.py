import hashlib
import pathlib
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from enum import Enum
from os.path import basename

from rest_framework.response import Response


def filter_params(params, items):
    result = {}
    for item in items:
        if params.get(item):
            result[item] = params.get(item)
    return result


def publisher_logo_path(instance, filename):
    return f"upload/publisher/{hashlib.md5(str(filename).encode('utf-8')).hexdigest()}{pathlib.Path(filename).suffix}"


def journal_resource_path(instance, filename):
    return f"upload/journals/{instance.name}/{hashlib.md5(str(filename).encode('utf-8')).hexdigest()}{pathlib.Path(filename).suffix}"


def submit_upload_path(instance, filename):
    return f"upload/submit-papers/{instance.submit.id}/{hashlib.md5(str(filename).encode('utf-8')).hexdigest()}{pathlib.Path(filename).suffix}"


def resource_upload_path(instance, filename):
    return f"upload/resource/{instance.resource.id}/{filename}"


def censor_file_path(instance, filename):
    return f"censorship/{basename(filename)}"


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('current_page', self.request.query_params.get('page', 1)),
            ('results', data),
        ]))


class SubmissionStatus:
    NEW_SUBMISSION = 'New Submission'
    START_SUBMISSION = 'Start Submission'
