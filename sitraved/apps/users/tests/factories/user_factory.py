import factory

from sitraved.apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    email = factory.Sequence(lambda n: f'user{n}@test.com')
    username = factory.Sequence(lambda n: f'user{n}')

    @factory.post_generation
    def password(self, create, extracted, **unused_kwargs):
        if not create:
            return
        password = extracted or '12345678'
        self.set_password(password)
        self.save()
