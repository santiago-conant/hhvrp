from django.contrib import admin

from .models import Solution, Route, RouteSequence, Result

admin.site.register(Solution)
admin.site.register(Route)
admin.site.register(RouteSequence)
admin.site.register(Result)
