from rest_framework import filters


class IsAuthorFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows authors to see their own books.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(authors__isnull=False)
