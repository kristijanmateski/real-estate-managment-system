from django.contrib import admin
from django.utils import timezone

from app.models import *


# Register your models here.

class AgentAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def has_add_permission(self, request):
        return request.user.is_superuser


class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True


class CharacteristicRealStateInline(admin.StackedInline):
    model = CharacteristicRealEstate
    extra = 0


class AgentRealEstateInline(admin.StackedInline):
    model = AgentRealEstate
    extra = 0


class RealEstateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'area',)
    exclude = ('characteristic',)

    inlines = [CharacteristicRealStateInline, AgentRealEstateInline]

    # dali postoi takov agent? valjda e toa
    def has_add_permission(self, request):
        return Agent.objects.filter(user=request.user).exists()

    def has_delete_permission(self, request, obj=None):
        if not CharacteristicRealEstate.objects.filter(real_state=obj).exists():
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if obj and AgentRealEstate.objects.filter(real_state=obj, agent__user=request.user).exists():
            return True

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            agent = Agent.objects.filter(user=request.user).first()
            if agent:
                AgentRealEstate.objects.create(real_state=obj, agent=agent)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            today = timezone.now().date()
            return qs.filter(date=today)
        return qs


admin.site.register(RealState, RealEstateAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(Agent, AgentAdmin)
