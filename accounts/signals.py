from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import UserProfile, MyUser

@receiver(post_save, sender=MyUser) 
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    # print(created)
    if created:
        UserProfile.objects.create(user=instance)  
        # print('User profile has ben created successfully') 
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()       
        except:
            #Create profile if it didnt exist
            UserProfile.objects.create(user=instance)
            # print('Profile didnt exist, but I have created one') 
        # print('user is updated')    
# post.save.connect(post_save_create_profile_receiver, sender=MyUser) >> instead use @receiver(post_save, sender=MyUser) above for simplicity

@receiver(pre_save, sender=MyUser)
def pre_save_profile_receiver(sender, instance, **kwargs):
    # print(instance.username, 'This user is being saved')
    pass