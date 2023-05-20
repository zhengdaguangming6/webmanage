#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django_filters import FilterSet, filters
from apps.bug.models import BugList


class BugFilterset(FilterSet):
    submitter = filters.CharFilter(field_name="submitter", lookup_expr="contains")
    content = filters.CharFilter(field_name="content", lookup_expr="contains")
    follow_up_person = filters.CharFilter(field_name="follow_up_person", lookup_expr="contains")
    solver = filters.CharFilter(field_name="solver", lookup_expr="contains")
    cause_detail = filters.CharFilter(field_name="cause_detail",  lookup_expr="contains")
    priority = filters.CharFilter(field_name="priority", lookup_expr="contains")
    level = filters.CharFilter(field_name="level", lookup_expr="contains")
    classification = filters.NumberFilter(field_name="classification", lookup_expr="exact")
    cause = filters.NumberFilter(field_name="cause", lookup_expr="exact")
    department = filters.NumberFilter(field_name="department", lookup_expr="exact")
    result = filters.NumberFilter(field_name="result", lookup_expr="exact")
    is_push = filters.NumberFilter(field_name="is_push", lookup_expr="exact")

    class Meta:
        model = BugList
        fields = ["submitter", "content", "follow_up_person", "solver", "cause_detail"]