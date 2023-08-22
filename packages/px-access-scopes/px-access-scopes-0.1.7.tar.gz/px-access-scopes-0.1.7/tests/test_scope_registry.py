from enum import Enum
import pytest
from django.db import models
from px_domains import Domain
from px_access_scopes import ScopeRegistry, ScopeDomain, auto, raw


def test_simple_creation():
    root = ScopeRegistry.create_root('TOKENS')

    @root.nest('SOME')
    class Tokens(Enum):
        AUTO1 = auto
        AUTO2 = auto
        AUTO3 = raw('AUTO3')
        FIXED = 'some'

    assert Tokens.AUTO1 == 'TOKENS::SOME::AUTO1'
    assert Tokens.FIXED == 'TOKENS::SOME::some'
    assert Tokens.AUTO3 == 'AUTO3'
    assert Tokens.AUTO3.value == 'AUTO3'
    assert isinstance(Tokens.AUTO1.value, ScopeDomain)


def test_nested_creation():
    root = ScopeRegistry.create_root(ScopeDomain('TOKENS'))

    @root.nest('SOME')
    class Tokens(Enum):
        AUTO1 = auto
        AUTO2 = auto
        AUTO3 = raw('AUTO3')
        FIXED = 'some'

    @Tokens.nest('NESTED')
    class Nested:
        AUTO = auto
        SOME = 'OTHER'

    assert Nested.AUTO == 'TOKENS::SOME::NESTED::AUTO'
    assert Nested.SOME == 'TOKENS::SOME::NESTED::OTHER'


def test_same_named_token_nest():
    root = ScopeRegistry.create_root('TOKENS')

    @root.nest('SOME')
    class Tokens(Enum):
        AUTO1 = auto
        AUTO2 = auto
        AUTO3 = raw('AUTO3')
        FIXED = 'some'

    with pytest.raises(AssertionError):
        @Tokens.nest('some')
        class Nested:
            AUTO = auto
            SOME = 'OTHER'


def test_wrong_domain_root():
    root = ScopeRegistry.create_root(Domain('TOKENS'))

    assert isinstance(root._domain, ScopeDomain)


@pytest.mark.django_db
def test_django_choices_nesting():
    from px_access_scopes.contrib.django.scopes import ScopeRegistry, auto
    from px_access_scopes.contrib.django.generator import generate_all
    from px_access_scopes.contrib.django.globals import registries, aggregates
    root = ScopeRegistry.create_root('TOKENS', 'Some')

    @root.nest('SOME', 'Label')
    class Tokens(models.TextChoices):
        baba = 'baba', 'Baba'
        gaga = 'gaga', 'Gaga'

    @Tokens.nest('OTHER', 'Label2')
    class Nested(models.TextChoices):
        AUTO = auto
        SOME = 'OTHER'

    @Tokens.nest('THIRD', 'Label3')
    class Nested2:
        AUTO = auto
        SOME = 'OTHER'

    generate_all([root], aggregates)