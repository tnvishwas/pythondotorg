import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from ..factories import UserFactory, MembershipFactory
from ..models import Membership

User = get_user_model()


class UsersModelsTestCase(TestCase):
    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username='username',
            password='password',
            email='user@domain.com'
        )
        self.assertNotEqual(user, None)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

        kwargs = {
            'username': '',
            'password': 'password',
        }
        self.assertRaises(ValueError, User.objects.create_user, **kwargs)

    def test_membership(self):
        plain_user = UserFactory()
        self.assertFalse(plain_user.has_membership)

        member = MembershipFactory()
        self.assertTrue(member.creator.has_membership)

    def test_higher_level_member(self):
        member1 = MembershipFactory()
        member2 = MembershipFactory(membership_type=Membership.SPONSOR)

        self.assertFalse(member1.higher_level_member)
        self.assertTrue(member2.higher_level_member)

    def test_needs_vote_affirmation(self):
        member1 = MembershipFactory()
        self.assertFalse(member1.needs_vote_affirmation)

        member2 = MembershipFactory(votes=True)
        self.assertFalse(member2.needs_vote_affirmation)

        last_year = timezone.now() - datetime.timedelta(days=366)
        member3 = MembershipFactory(
            votes=True,
            last_vote_affirmation=last_year,
        )

        self.assertTrue(member3.needs_vote_affirmation)
