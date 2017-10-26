# -*- coding: utf-8 -*-

import json

from constants import DEFAULT_COVERAGE, ESTADOS_BRASIL


class SpiderCoverageMixin(object):
    default_coverage = DEFAULT_COVERAGE

    @classmethod
    def check_multiple_coverage(cls, coverage_fields):
        inter = len(set(ESTADOS_BRASIL).intersection(set(coverage_fields)))
        if inter > 0 or 'default' in coverage_fields:
            return True
        return False

    @classmethod
    def check_default_coverage(cls):
        coverage = getattr(cls, 'coverage', {})
        return cls.default_coverage != coverage

    @classmethod
    def check_required_args(cls):
        for arg in ['name', 'fonte', 'coverage']:
            if not hasattr(cls, arg):
                return False
        if not (hasattr(cls, 'estado') or
                hasattr(cls, 'estados_config') or
                hasattr(cls, 'estados')):
            return False
        return True

    @classmethod
    def check_coverage(cls):
        default_fields = DEFAULT_COVERAGE.keys()
        coverage = getattr(cls, 'coverage', {})

        coverage_fields = coverage.keys()
        if cls.check_multiple_coverage(coverage_fields):
            for value in coverage.values():
                if not set(default_fields).issubset(value.keys()):
                    return False
            return True

        elif set(default_fields).issubset(coverage_fields):
            return True
        return False

    @classmethod
    def test_spider(cls):
        if 'extrair' not in getattr(cls, 'name', ''):
            if not cls.check_default_coverage():
                raise Exception(
                    u'Spider coverage arguments are equal to default')
            if not cls.check_required_args():
                raise Exception(
                    u'This spider does not have all required arguments')
            if not cls.check_coverage():
                raise Exception(u'Error on spider coverage arguments')

    @classmethod
    def output_json(cls):
        output = {}
        # Required Fields
        for arg in ['name', 'fonte']:
            arg_dict = {arg: getattr(cls, arg, '')}
            output.update(arg_dict)

        # Estados
        if hasattr(cls, 'estados_config'):
            estados = [estado_dict['meta']['estado']
                       for estado_dict in getattr(cls, 'estados_config', '')]
            output.update({'estados': estados})
        elif hasattr(cls, 'estados'):
            output.update({'estados': getattr(cls, 'estados', '')})
        else:
            output.update({'estado': getattr(cls, 'estado', '')})

        # Coverage
        coverage = getattr(cls, 'coverage', {})
        if cls.check_multiple_coverage(coverage.keys()):
            output.update({'coverage': coverage})
        else:
            output.update(getattr(cls, 'coverage', {}))

        return json.dumps(output, ensure_ascii=False)
