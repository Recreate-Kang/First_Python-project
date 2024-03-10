class CompanyModel:
 
    def __init__(self, _name, _cate, _country, _score, _rank20, _rank19):
        self.name = _name
        self.category = _cate
        self.country = _country
        self.score = _score
        self.rank2020 = _rank20
        self.rank2019 = _rank19
 
    def SaveFormat(self):
        data = '{0};{1};{2};{3};{4};{5}'.format(self.name, self.category, self.country, self.score, self.rank2020, self.rank2019)
 
        return data
