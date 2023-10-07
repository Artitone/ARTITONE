from django.db import models

from profiles.models.artist import Artist
from profiles.models.customer import Customer


class UserFollowing(models.Model):
    user_id = models.ForeignKey(
        Customer, related_name="following", null=True, default=None, on_delete=models.CASCADE
    )
    following_user_id = models.ForeignKey(
        Artist, related_name="followers", null=True, default=None, on_delete=models.CASCADE
    )

    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "following_user_id"], name="unique_followers"
            )
        ]

        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"


def follow(customer, artist):
    following = UserFollowing.objects.create(user_id=customer, following_user_id=artist)
    return following


def unfollow(customer, artist):
    UserFollowing.objects.filter(user_id=customer, following_user_id=artist).delete()
