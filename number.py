class To_Number:
    def __init__(self, start_of_index = 0, ):
        self.end_of_index = start_of_index 
        self.start_of_index = start_of_index 
        self.dict={}
        self.decode_dict={}
    def add(self, ele):
        if ele not in self.dict:
            self.dict[ele] = self.end_of_index
            self.decode_dict[self.end_of_index] = ele
            self.end_of_index= self.end_of_index+ 1
    def encode(self, ele):
        self.add(ele)
        return self.dict[ele]
    def encode_array(self, array):
        return list(map(self.encode, array))
    def decode(self, number):
        assert isinstance(number, int)
        assert number >= self.start_of_index
        assert number < self.end_of_index
        return self.decode_dict[number]
    def decode_array(self, number_array):
        return list(map(self.decode, number_array))
    
to_number = To_Number()
items_number = list(map(to_number.encode_array, items))
to_number.decode_array(items_number[3])
