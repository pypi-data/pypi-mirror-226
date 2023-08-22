from enum import Enum

from px_access_scopes import ScopeRegistry, ScopeDomain, auto, raw
from px_access_scopes.export import export_nested_tree, export_nested_tree_leaves


def test_nested_export():
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

    tree = export_nested_tree(root)

    assert tree['TOKENS']['v'] == root._domain
    assert tree['TOKENS']['c']['SOME']['c']['AUTO3']['v'] == 'AUTO3'
    assert tree['TOKENS']['c']['SOME']['c']['NESTED']['c']['SOME']['v'] == Nested.SOME


def test_nested_leaves_export():
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

    tree = export_nested_tree_leaves(root)

    assert tree['TOKENS']['SOME']['AUTO3'] == 'AUTO3'
    assert tree['TOKENS']['SOME']['NESTED']['SOME'] == Nested.SOME
