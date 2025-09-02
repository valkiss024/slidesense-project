import factory
from django.utils import timezone

from ..models import Presentation


class PresentationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Presentation

    title = factory.Sequence(lambda n: f'Presentation {n}')
    domain = factory.Faker('word')
    target_audience = factory.Faker("word")
    favourited = False
    uploaded_at = factory.LazyFunction(timezone.now)
    last_analyzed_at = None

    class Params:
        with_analysis = factory.Trait(
            last_analyzed_at=factory.LazyFunction(timezone.now),
        )
        favourited_true = factory.Trait(
            favourited=True,
        )
