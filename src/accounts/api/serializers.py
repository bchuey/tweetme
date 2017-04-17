from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from rest_framework import serializers

User = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):

    # serializer method field
    follower_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            # 'email',
            'follower_count',
            'url',
        ]

    # get_<name of field>
    def get_follower_count(self, obj):
        # print(obj.username)
        return 0

    def get_url(self,obj):

        return reverse_lazy('profiles:detail', kwargs={'username':obj.username})
