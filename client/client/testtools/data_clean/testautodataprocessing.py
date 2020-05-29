'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-17 21:31:43
@LastEditors: feliciaren
@LastEditTime: 2020-05-17 22:38:27
'''
from client.data_clean.autodataprocessing import AutoDataProcess


class TestAutoDataProcessing:
    def setup(self):
        self.data = [[1,2,3,'a'],[2,3,4,'b']]
        self.testdata = [[1,3,4,'b']]

    def test_init(self):
        autodataprocess = AutoDataProcess()
        assert(autodataprocess.__class__==AutoDataProcess)
    
    def test_fit(self):
        autodataprocess = AutoDataProcess(label_col=0)
        feature,label = autodataprocess._fit_(self.data)
        print(feature,label)
        assert(feature == [[2,3,0],[3,4,1]] or feature ==  [[2,3,1],[3,4,0]])
        assert(label == [1,0] or label == [0,1])
    
    def test_transform(self):
        autodataprocess = AutoDataProcess(label_col=0)
        feature,label = autodataprocess._fit_(self.data)
        feature,label = autodataprocess._transform_(self.testdata)
        print(feature,label)
        assert(feature == [[3,4,1]] or feature == [[3,4,0]])
        assert(label == [1] or label == [0])


if __name__ == "__main__":
    test = TestAutoDataProcessing()
    test.setup()
    test.test_init()
    test.test_fit()
    test.test_transform()
        
