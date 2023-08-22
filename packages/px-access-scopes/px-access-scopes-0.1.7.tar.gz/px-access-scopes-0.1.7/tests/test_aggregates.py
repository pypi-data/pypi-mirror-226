from px_access_scopes import Aggregate, Aggregates, auto_aggregate as auto


def test_aggregates():
    class Roles(Aggregates):
        Manager = auto
        Other = Aggregate('different')

    Roles.Manager.add('some')

    assert Roles.Manager.name == 'Manager'
    assert Roles._item_names == ['Manager', 'Other']
    assert 'some' in Roles.Manager
