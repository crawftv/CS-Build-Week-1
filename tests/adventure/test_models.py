import pytest

from adventure.models import Item
from hypothesis import given
from hypothesis.strategies import text,characters, integers,none,one_of,composite

pytestmark = pytest.mark.django_db

class TestItemModel:
    @composite
    def generate_item_data(draw):
        a = one_of(text())
        b = one_of(text(),none())
        #important to know your database limits, max_value will break tests if too big
        c = integers(min_value=0,max_value=10000)
        return draw(a),draw(b),draw(c)
    @given(generate_item_data())
    def test_item_create(self,g):
        a,b,c = g
        item = Item.objects.create(name=a,description=b,level=c)
        item.save()
        assert Item.objects.get(id=item.id)
