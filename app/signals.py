from django.db.models.signals import pre_save

from django.dispatch import receiver

from app.models import RealState, AgentRealEstate


@receiver(pre_save, sender=RealState)
def handle_saving_house(sender, instance, **kwargs):
    old_instance = sender.objects.filter(id=instance.id).first()
    if old_instance:
        if old_instance.sold != instance.sold:
            agents_real_state = AgentRealEstate.objects.filter(real_state=old_instance).all()
            for agent_real_estate in agents_real_state:
                agent = agent_real_estate.agent
                agent.total_sales += 1
                agent.save()
