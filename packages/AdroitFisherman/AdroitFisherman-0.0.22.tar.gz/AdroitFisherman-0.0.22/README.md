example!
```python
from AdroitFisherman.DoubleLinkedListWithoutHeadNode.Double import DoubleLinkedListWithoutHeadNode_double
if __name__ == '__main__':
    operate=0
    test=DoubleLinkedListWithoutHeadNode_double()
    while operate<16:
        print("1:Init linear list	2:Destroy linear list	3:Clear Linear list", end='\n')
        print("4:Is list empty	5:Get list length	6:Get elem's value", end='\n')
        print("7:Get elem's index	8:Get elem's prior elem	9:Get elem's next elem", end='\n')
        print("10:Add elem to the first position	11:Add elem to the last position	12:Insert elem into list", end='\n')
        print("13:Delete elem	14:View list	15:View list by reverse order", end='\n')
        operate = int(input("please choose operation options:"))
        if operate==1:
            test.init_list()
        elif operate==2:
            test.destroy_list()
        elif operate==3:
            test.clear_list()
        elif operate==4:
            if test.list_empty()==True:
                print("empty",end='\n')
            else:
                print("not empty",end='\n')
        elif operate==5:
            print(f"length:{test.list_length()}",end='\n')
        elif operate==6:
            index=int(input("please input elem's position:"))
            print(f"elem value:{test.get_elem(index)}")
        elif operate==7:
            elem=float(input("please input elem's value:"))
            print("elem position:%d"%test.locate_elem(elem))
        elif operate==8:
            elem = float(input("please input elem's value:"))
            print("prior elem's value:%f" % test.prior_elem(elem))
        elif operate==9:
            elem = float(input("please input elem's value:"))
            print("next elem's value:%f" % test.next_elem(elem))
        elif operate==10:
            elem = float(input("please input elem's value:"))
            test.add_first(elem)
            for i in range(0,test.list_length(),1):
                print(test.get_elem(i),end='\t')
            print(end='\n')
        elif operate==11:
            elem = float(input("please input elem's value:"))
            test.add_after(elem)
            for i in range(0,test.list_length(),1):
                print(test.get_elem(i),end='\t')
            print(end='\n')
        elif operate==12:
            index = int(input("please input elem's position:"))
            elem = float(input("please input elem's value:"))
            test.list_insert(index, elem)
            for i in range(0,test.list_length(),1):
                print(test.get_elem(i),end='\t')
            print(end='\n')
        elif operate==13:
            index = int(input("please input elem's position:"))
            test.list_delete(index)
            for i in range(0,test.list_length(),1):
                print(test.get_elem(i),end='\t')
            print(end='\n')
        elif operate==14:
            for i in range(0,test.list_length(),1):
                print(test.get_elem(i),end='\t')
            print(end='\n')
        elif operate==15:
            test.traverse_list_by_reverse_order()
```