import django_filters
from datetime import timedelta, time, datetime
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

def _truncate(dt):
    return dt.date()

class CustomChoiceFilter(django_filters.ChoiceFilter):
    def __init__(self, choices=None, filters=None, *args, **kwargs):
        if choices is not None:
            self.choices = choices
        if filters is not None:
            self.filters = filters
        unique = set([x[0] for x in self.choices]) ^ set(self.filters)
        assert not unique, \
            "Keys must be present in both 'choices' and 'filters'. Missing keys: " \
            "'%s'" % ', '.join(sorted(unique))

        # TODO: remove assertion in 2.1
        assert not hasattr(self, 'options'), \
            "The 'options' attribute has been replaced by 'choices' and 'filters'. " \
            "See: https://django-filter.readthedocs.io/en/main/guide/migration.html"

        # null choice not relevant
        kwargs.setdefault('null_label', None)
        super().__init__(choices=self.choices, *args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs

        assert value in self.filters

        qs = self.filters[value](qs, self.field_name)
        return qs.distinct() if self.distinct else qs

class DateRangeFilter(CustomChoiceFilter):
    choices = [
        ('today', _('Today')),
        ('tomorrow', _('Amanhã')),
        ('yesterday', _('Yesterday')),
        ('currweek', _('Semana atual')),
        ('week', _('Past 7 days')),
        ('month', _('This month')),
        ('year', _('This year')),
    ]
    filters = {
        'today': lambda qs, name: qs.filter(**{
            '%s__year' % name: now().year,
            '%s__month' % name: now().month,
            '%s__day' % name: now().day
        }),
        'tomorrow': lambda qs, name: qs.filter(**{
            '%s__year' % name: (now() + timedelta(days=1)).year,
            '%s__month' % name: (now() + timedelta(days=1)).month,
            '%s__day' % name: (now() + timedelta(days=1)).day,
        }),
        'yesterday': lambda qs, name: qs.filter(**{
            '%s__year' % name: (now() - timedelta(days=1)).year,
            '%s__month' % name: (now() - timedelta(days=1)).month,
            '%s__day' % name: (now() - timedelta(days=1)).day,
        }),
        'week': lambda qs, name: qs.filter(**{
            '%s__gte' % name: _truncate(now() - timedelta(days=7)),
            '%s__lt' % name: _truncate(now() + timedelta(days=1)),
        }),
        'currweek': lambda qs, name: qs.filter(**{
            '%s__week' % name: now().strftime("%V"),
        }),
        'month': lambda qs, name: qs.filter(**{
            '%s__year' % name: now().year,
            '%s__month' % name: now().month
        }),
        'year': lambda qs, name: qs.filter(**{
            '%s__year' % name: now().year,
        }),
    }