import enum
import unittest
import logging

from framework.config import BaseConfiguration
from framework.tags import MetaTag


class FilterReason(enum.Enum):
    """Format strings for all messages to publish in report for skipped tests
    """
    product_excluded = '[Filter] Product-specific test (Found:{found})'
    shared_excluded = '[Filter] General product test'
    priority_undefined = '[Filter] No priority defined'
    priority_mismatch = '[Filter] Priority lower than filter (Found:{found})'
    category_blacklist = '[Filter] Category in exclusion list (Matched:{matches})'
    category_whitelist = '[Filter] Category not in inclusion list'


class FilterSystem:

    def __init__(self, config: BaseConfiguration):
        self._logger = logging.getLogger(__name__)
        self._config = config
        pass

    def filter_by_product(self, test, method, tags: MetaTag):
        is_filtered = False

        filter_product = self._config.get_product()
        skip_shared = self._config.is_shared_skipped()

        if filter_product:
            if not tags and skip_shared:
                is_filtered = self._skip_all_shared(test, method)
            elif tags:
                if not tags.product and skip_shared:
                    is_filtered = self._skip_all_shared(test, method)
                elif tags.product and tags.product != filter_product:
                    is_filtered = self._skip_by_product(test, method)
        else:
            if tags and tags.product:
                is_filtered = self._skip_by_product(test, method)

        return is_filtered

    def filter_by_priority(self, test, method, tags: MetaTag):
        is_filtered = False

        filter_priority = self._config.get_priority()

        if filter_priority > 0:
            if not tags:
                is_filtered = self._skip_nonpriority(test, method)
            else:
                if tags.priority < 0:
                    is_filtered = self._skip_nonpriority(test, method)
                elif tags.priority > filter_priority:
                    is_filtered = self._skip_lower_priority(test, method)

        return is_filtered

    def filter_by_blacklist(self, test, method, tags: MetaTag):
        is_filtered = False

        if not self._config.is_excluded:
            return is_filtered

        filter_categories = self._config.get_categories()

        if len(filter_categories) == 0:
            return is_filtered

        if tags:
            matched = tags.categories.intersection(filter_categories)
            if len(matched) > 0:
                is_filtered = self._skip_blacklisted_category(test, method, matched)

        return is_filtered

    def filter_by_whitelist(self, test, method, tags: MetaTag):
        is_filtered = False

        if self._config.is_excluded:
            return is_filtered

        filter_categories = self._config.get_categories()

        if len(filter_categories) == 0:
            return is_filtered

        if not tags:
            is_filtered = self._skip_non_whitelisted_category(test, method)
        else:
            matched = tags.categories.intersection(filter_categories)
            if len(matched) == 0:
                is_filtered = self._skip_non_whitelisted_category(test, method)

        return is_filtered

    @staticmethod
    def _skip_by_product(test, method):
        tags = getattr(method, 'tags', None)
        _mark_for_skip(test, method, FilterReason.product_excluded, found=tags.product)
        return True

    @staticmethod
    def _skip_all_shared(test, method):
        _mark_for_skip(test, method, FilterReason.shared_excluded)
        return True

    @staticmethod
    def _skip_nonpriority(test, method):
        _mark_for_skip(test, method, FilterReason.priority_undefined)
        return True

    @staticmethod
    def _skip_lower_priority(test, method):
        tags = getattr(method, 'tags', None)
        _mark_for_skip(test, method, FilterReason.priority_mismatch, found=tags.priority)
        return True

    @staticmethod
    def _skip_blacklisted_category(test, method, matches):
        _mark_for_skip(test, method, FilterReason.category_blacklist, matches=matches)
        return True

    @staticmethod
    def _skip_non_whitelisted_category(test, method):
        _mark_for_skip(test, method, FilterReason.category_whitelist)
        return True


def _mark_for_skip(test, method, reason_code: FilterReason, *args, **kwargs):
    reason = reason_code.value.format(*args, **kwargs)
    setattr(test, method.__name__, _decorate_skip(method, reason))


def _decorate_skip(method, reason):
    """unittest provides a built-in skip decorator that can be reused for
        disabled test cases that do not match the filter criteria. It is a
        parameterized decorator, so dynamic decoration syntax is convoluted
    """
    return unittest.skip(reason)(method)
