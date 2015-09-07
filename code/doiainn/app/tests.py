from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.db.models import Q


class AppTestCase(TestCase):
    def setUp(self):
        self.surgeon = Group.objects.create(name='Surgeon')
        self.flagged = Group.objects.create(name='Flagged')

    def test_m2m_count(self):
        house = User.objects.create_user(username='house',
                                         email='house@vumedi.com',
                                         password='house123')
        # only one user, Dr. House
        self.assertEqual(User.objects.count(), 1)

        # House is a surgeon and flagged
        house.groups.add(self.surgeon, self.flagged)
        self.assertEqual(User.objects.filter(groups=self.surgeon).count(), 1)
        self.assertEqual(User.objects.filter(groups=self.flagged).count(), 1)

        # how many users that are surgeon or flagged?
        # only one user in db
        # it must be one
        surgeons = User.objects.filter(groups__in=[self.surgeon, self.flagged])
        self.assertEqual(surgeons.count(), 2)

        # same thing with Qs
        surgeons = User.objects.filter(Q(groups=self.surgeon) |
                                       Q(groups=self.flagged))
        self.assertEqual(surgeons.count(), 2)

        # use distinct
        self.assertEqual(surgeons.distinct().count(), 1)
