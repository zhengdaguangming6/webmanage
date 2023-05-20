#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django_filters import FilterSet, filters
from apps.interface_test.models import InterfaceTest


class InterfaceFilterset(FilterSet):
    yapi = filters.CharFilter(field_name="domain", lookup_expr="contains")
    tapi = filters.CharFilter(field_name="domain", lookup_expr="contains")
    m = filters.CharFilter(field_name="domain", lookup_expr="contains")
    interface_title = filters.CharFilter(field_name="interface_title", lookup_expr="contains")
    create_user = filters.CharFilter(field_name="create_user__username",  lookup_expr="contains")
    update_user = filters.CharFilter(field_name="update_user__username",  lookup_expr="contains")
    run = filters.NumberFilter(field_name="run", lookup_expr="exact")

    class Meta:
        model = InterfaceTest
        fields = ["yapi", "tapi", "m"]