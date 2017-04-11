import praelatus.lib.labels as labels
import pytest
from praelatus.lib import session


@pytest.fixture
def db():
    return session()


def test_get(db):
    lbl = labels.get(db, name='duplicate')
    assert lbl is not None
    assert lbl.name == 'duplicate'
    assert lbl.id is not None


def test_get_with_filter(db):
    lbls = labels.get(db, filter='*t*')
    assert lbls is not None
    assert len(lbls) > 0
    assert lbls[0].id is not None

