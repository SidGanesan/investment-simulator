from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, JSONAttribute


class Portfolio(Model):
    class Meta:
        table_name = "portfolios.uat.jarden.io"
        region = "ap-southeast-2"
        host = "http://localhost:8000"
        write_capacity_units = 10
        read_capacity_units = 10

    def __iter__(self):
        for name, attr in self.get_attributes().items():
            yield name, attr.serialize(getattr(self, name))

    def as_dict(self):
        return dict(self)

    model = UnicodeAttribute(hash_key=True)
    portfolio_name = UnicodeAttribute(range_key=True)
    risk_score = NumberAttribute()
    holdings = JSONAttribute(null=False)
    constants = JSONAttribute()


if __name__ == "__main__":
    Portfolio.create_table()
