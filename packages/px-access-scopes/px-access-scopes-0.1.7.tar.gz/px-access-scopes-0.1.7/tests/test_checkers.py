from enum import Enum
from dataclasses import dataclass
from typing import Sequence
import pytest
from px_access_scopes import (
    ScopesCheckRunner, scopes_checker, aggregates_checker, HierarchyChecker,
    domain_path_hierarchy_lookup, CheckExit,
    MultiregistryHierarchyLookup
)
from px_access_scopes.contrib.django import (
    Aggregate, Aggregates, ScopeDomain, ScopeRegistry, auto
)
from px_access_scopes.contrib.django.checkers import user_checker


@dataclass
class User:
    permissions: Sequence[str]

    def has_perm(self, permission: str, obj=None):
        return permission in self.permissions


@pytest.fixture
def rules():
    root = ScopeRegistry.create_root(ScopeDomain('TOKENS'))

    @root.nest('FIRST')
    class Tokens(Enum):
        ONE = auto
        TWO = auto

    @Tokens.nest('NESTED')
    class Nested:
        AUTO = auto
        SOME = 'OTHER'
        THIRD = 'THIRD'

    class Roles(Aggregates):
        Simple = Aggregate(5000)
        First = Aggregate(4900)

    Roles.Simple.add(Nested._domain)
    Roles.First.add(Tokens.ONE)
    Roles.First.add(Nested.SOME)

    return root, Tokens, Nested, Roles


def test_simple_lookups(rules):
    root, Tokens, Nested, Roles = rules

    checker = ScopesCheckRunner((
        scopes_checker,
    ), registry=root)

    USER1 = {'scopes': [Nested.AUTO]}
    USER2 = {'scopes': [Nested.AUTO], 'aggregates': [Roles.Simple]}

    assert checker((Nested.AUTO,), **USER1) is True
    assert checker((Nested.SOME,), **USER1) is False

    assert checker((Nested.AUTO,), **USER2) is True
    assert checker((Nested.SOME,), **USER2) is False


def test_aggregates_lookups(rules):
    root, Tokens, Nested, Roles = rules

    checker = ScopesCheckRunner((
        scopes_checker, aggregates_checker
    ), registry=root)

    USER1 = {'scopes': [Nested.AUTO]}
    USER2 = {'scopes': [Nested.AUTO], 'aggregates': [Roles.Simple]}
    USER3 = {'scopes': [Nested.AUTO], 'aggregates': [Roles.First]}

    assert checker((Nested.AUTO,), **USER1) is True
    assert checker((Nested.SOME,), **USER1) is False

    assert checker((Nested.AUTO,), **USER2) is True
    assert checker((Nested.SOME,), **USER2) is False

    assert checker((Nested.AUTO,), **USER3) is True
    assert checker((Nested.SOME,), **USER3) is True


def test_multiscope_check_lookups(rules):
    root, Tokens, Nested, Roles = rules

    checker = ScopesCheckRunner((
        scopes_checker, aggregates_checker
    ), registry=root)

    USER1 = {'scopes': [Nested.AUTO]}
    USER2 = {'scopes': [Nested.AUTO], 'aggregates': [Roles.Simple]}
    USER3 = {'scopes': [Nested.AUTO], 'aggregates': [Roles.First]}

    assert checker((Nested.AUTO, Nested.SOME), **USER1) is True

    assert checker((Nested.AUTO, Tokens.ONE), **USER2) is True
    assert checker((str(Nested), Tokens.ONE), **USER2) is True

    assert checker((Nested.AUTO, Nested.SOME), **USER3) is True
    assert checker((Nested.AUTO, Tokens.ONE), **USER3) is True
    assert checker((Nested.AUTO, Tokens.TWO), **USER3) is True
    assert checker((str(Nested), Tokens.TWO), **USER3) is False

    assert checker((), **USER3) is True
    assert checker(()) is True
    assert checker(('',)) is False


def test_hierarchy_lookups(rules):
    root, Tokens, Nested, Roles = rules

    checker = ScopesCheckRunner((HierarchyChecker((
        scopes_checker, aggregates_checker
    )),), registry=root)

    USER1 = {'scopes': [Nested.AUTO]}
    USER2 = {'scopes': [Nested.AUTO], 'aggregates': [Roles.Simple]}
    USER3 = {'scopes': [Nested.AUTO], 'aggregates': [Roles.First]}

    assert checker((Nested.AUTO,), **USER1) is True
    assert checker((Nested.SOME,), **USER1) is False

    assert checker((Nested.AUTO,), **USER2) is True
    assert checker((Nested.SOME,), **USER2) is True

    assert checker((Nested.AUTO,), **USER3) is True
    assert checker((Nested.SOME,), **USER3) is True


def test_no_registry_lookups(rules):
    root, Tokens, Nested, Roles = rules

    checker = ScopesCheckRunner((HierarchyChecker((
        scopes_checker, aggregates_checker
    ), hierarchy_lookup=domain_path_hierarchy_lookup),))

    USER1 = {'scopes': [Nested.AUTO]}
    USER2 = {'scopes': [Nested.AUTO], 'aggregates': [Roles.Simple]}
    USER3 = {'scopes': [Nested.AUTO], 'aggregates': [Roles.First]}

    assert checker((Nested.AUTO,), **USER1) is True
    assert checker((Nested.SOME,), **USER1) is False

    assert checker((Nested.AUTO,), **USER2) is True
    assert checker((Nested.SOME,), **USER2) is True

    assert checker((Nested.AUTO,), **USER3) is True
    assert checker((Nested.SOME,), **USER3) is True
    assert checker((Tokens.ONE,), **USER3) is True
    assert checker((Tokens.TWO,), **USER3) is False


def test_stopper_lookups(rules):
    root, Tokens, Nested, Roles = rules

    def stop_checker(*a, **kw):
        raise CheckExit('Just stop')

    checker = ScopesCheckRunner((HierarchyChecker((
        scopes_checker, stop_checker, aggregates_checker
    ), hierarchy_lookup=domain_path_hierarchy_lookup),))

    USER1 = {'scopes': [Nested.AUTO]}
    USER2 = {'scopes': [Nested.AUTO], 'aggregates': [Roles.Simple]}
    USER3 = {'scopes': [Nested.AUTO], 'aggregates': [Roles.First]}

    assert checker((Nested.AUTO,), **USER1) is True
    assert checker((Nested.SOME,), **USER1) is False

    assert checker((Nested.AUTO,), **USER2) is True
    assert checker((Nested.SOME,), **USER2) is False

    assert checker((Nested.AUTO,), **USER3) is True
    assert checker((Nested.SOME,), **USER3) is False
    assert checker((Tokens.ONE,), **USER3) is False
    assert checker((Tokens.TWO,), **USER3) is False


def test_django_user_checker_lookups(rules):
    root, Tokens, Nested, Roles = rules

    checker = ScopesCheckRunner((
        HierarchyChecker(
            (user_checker,),
            hierarchy_lookup=MultiregistryHierarchyLookup(
                registries=[root]
            )
        ),
    ))

    USER1 = User((Nested.AUTO, Tokens.ONE))
    USER2 = User((str(Nested),))

    assert checker((Nested.AUTO,), user=USER1) is True
    assert checker((Nested.SOME,), user=USER1) is False
    assert checker((Nested.SOME, Tokens.ONE), user=USER1) is True
    assert checker((Nested.SOME, ), user=USER2) is True
    assert checker((Nested.AUTO, ), user=USER2) is True
    assert checker((Nested.THIRD, ), user=USER2) is True
