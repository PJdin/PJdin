# -*- coding: utf-8 -*-


import pandas as pd

"""另外可以導入Series和DataFrame，因為這兩個經常被用到："""

from pandas import Series, DataFrame

"""# 5.1 Introduction to pandas Data Structures

資料結構其實就是Series和DataFrame。

# 1 Series

這裡series我就不翻譯成序列了，因為之前的所有筆記裡，我都是把sequence翻譯成序列的。

series是一個像陣列一樣的一維序列，並伴有一個陣列表示label，叫做index。創建一個series的方法也很簡單：
"""

obj = pd.Series([4, 7, -5, 3])
obj

"""可以看到，左邊表示index，右邊表示對應的value。可以通過value和index屬性查看："""

obj.values

obj.index # like range(4)

"""當然我們也可以自己指定index的label："""

obj2 = pd.Series([4, 7, -5, 3], index=['d', 'b', 'a', 'c'])

obj2

obj2.index

"""可以用index的label來選擇："""

obj2['a']

obj2['d'] = 6

obj2[['c', 'a', 'd']]

"""這裡['c', 'a', 'd']其實被當做了索引，儘管這個索引是用string構成的。

使用numpy函數或類似的操作，會保留index-value的關係：
"""

obj2[obj2 > 0]

obj2 * 2

import numpy as np
np.exp(obj2)

"""另一種看待series的方法，它是一個長度固定，有順序的dict，從index映射到value。在很多場景下，可以當做dict來用："""

'b' in obj2

'e' in obj2

"""還可以直接用現有的dict來創建series："""

sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon':16000, 'Utah': 5000}

obj3 = pd.Series(sdata)
obj3

"""series中的index其實就是dict中排好序的keys。我們也可以傳入一個自己想要的順序："""

states = ['California', 'Ohio', 'Oregon', 'Texas']

obj4 = pd.Series(sdata, index=states)
obj4

"""順序是按states裡來的，但因為沒有找到california,所以是NaN。NaN表示缺失資料，用之後我們提到的話就用missing或NA來指代。pandas中的isnull和notnull函數可以用來檢測缺失資料："""

pd.isnull(obj4)

pd.notnull(obj4)

"""series也有對應的方法："""

obj4.isnull()

"""關於缺失資料，在第七章還會講得更詳細一些。

series中一個有用的特色自動按index label來排序（Data alignment features）：
"""

obj3

obj4

obj3 + obj4

"""這個Data alignment features（資料對齊特色）和資料庫中的join相似。

serice自身和它的index都有一個叫name的屬性，這個能和其他pandas的函數進行整合：
"""

obj4.name = 'population'

obj4.index.name = 'state'

obj4

"""series的index能被直接更改："""

obj

obj.index = ['Bob', 'Steve', 'Jeff', 'Ryan']
obj

"""# 2 DataFrame

DataFrame表示一個長方形表格，並包含排好序的列，每一列都可以是不同的數數值型別（數位，字串，布林值）。DataFrame有行索引和列索引（row index, column index）；可以看做是分享所有索引的由series組成的字典。資料是保存在一維以上的區塊裡的。

（其實我是把dataframe當做excel裡的那種表格來用的，這樣感覺更直觀一些）

構建一個dataframe的方法，用一個dcit，dict裡的值是list：


"""

data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'], 
        'year': [2000, 2001, 2002, 2001, 2002, 2003], 
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}

frame = pd.DataFrame(data)

frame

"""dataframe也會像series一樣，自動給資料賦index, 而列則會按順序排好。

對於一個較大的DataFrame，用head方法會返回前5行（注：這個函數在資料分析中經常使用，用來查看表格裡有什麼東西）：
"""

frame.head()

"""如果指定一列的話，會自動按列排序："""

pd.DataFrame(data, columns=['year', 'state', 'pop'])

"""如果你導入一個不存在的列名，那麼會顯示為缺失資料："""

frame2 = pd.DataFrame(data, columns=['year', 'state', 'pop', 'debt'], 
                      index=['one', 'two', 'three', 'four', 'five', 'six'])

frame2

frame2.columns

"""從DataFrame裡提取一列的話會返回series格式，可以以屬性或是dict一樣的形式來提取："""

frame2['state']

frame2.year

"""注意：frame2[column]能應對任何列名，但frame2.column的情況下，列名必須是有效的python變數名才行。

返回的series有DataFrame種同樣的index，而且name屬性也是對應的。

對於行，要用在loc屬性裡用 位置或名字：
"""

frame2.loc['three']

"""列值也能通過賦值改變。比如給debt賦值："""

frame2['debt'] = 16.5
frame2

frame2['debt'] = np.arange(6.)
frame2

"""如果把list或array賦給column的話，長度必須符合DataFrame的長度。如果把一二series賦給DataFrame，會按DataFrame的index來賦值，不夠的地方用缺失資料來表示："""

val = pd.Series([-1.2, -1.5, -1.7], index=['two', 'four', 'five'])
frame2['debt'] = val
frame2

"""如果列不存在，賦值會創建一個新列。而del也能像刪除字典關鍵字一樣，刪除列："""

frame2['eastern'] = frame2.state == 'Ohio'
frame2

"""然後用del刪除這一列："""

del frame2['eastern']

frame2.columns

"""注意：columns返回的是一個view，而不是新建了一個copy。因此，任何對series的改變，會反映在DataFrame上。除非我們用copy方法來新建一個。

另一種常見的格式是dict中的dict：
"""

pop = {'Nevada': {2001: 2.4, 2002: 2.9},
       'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}

"""把上面這種嵌套dcit傳給DataFrame，pandas會把外層dcit的key當做列，內層key當做行索引："""

frame3 = pd.DataFrame(pop)
frame3

"""另外DataFrame也可以向numpy陣列一樣做轉置："""

frame3.T

"""指定index："""

pd.DataFrame(pop, index=[2001, 2002, 2003])

"""series組成的dict："""

pdata = {'Ohio': frame3['Ohio'][:-1],
         'Nevada': frame3['Nevada'][:2]}

pd.DataFrame(pdata)

"""其他一些可以傳遞給DataFrame的構造器：

![](http://oydgk2hgw.bkt.clouddn.com/pydata-book/yv7rc.png)

如果DataFrame的index和column有自己的name屬性，也會被顯示：


"""

frame3.index.name = 'year'; frame3.columns.name = 'state'

frame3

"""values屬性會返回二維陣列："""

frame3.values

"""如果column有不同的類型，dtype會適應所有的列："""

frame2.values

"""# 3 Index Objects (索引物件)

pandas的Index Objects (索引物件)負責保存axis labels和其他一些資料（比如axis name或names）。一個陣列或其他一個序列標籤，只要被用來做構建series或DataFrame，就會被自動轉變為index：
"""

obj = pd.Series(range(3), index=['a', 'b', 'c'])

index = obj.index
index

index[1:]

"""index object是不可更改的："""

index[1] = 'd'

"""正因為不可修改，所以data structure中分享index object是很安全的："""

labels = pd.Index(np.arange(3))
labels

obj2 = pd.Series([1.5, -2.5, 0], index=labels)
obj2

obj2.index is labels

"""index除了想陣列，還能像大小一定的set："""

frame3

frame3.columns

'Ohio' in frame3.columns

2003 in frame3.columns

"""與python裡的set不同，pandas的index可以有重複的labels："""

dup_labels = pd.Index(['foo', 'foo', 'bar', 'bar'])
dup_labels

"""在這種重複的標籤中選擇的話，會選中所有相同的標籤。

Index還有一些方法和屬性：

![](http://oydgk2hgw.bkt.clouddn.com/pydata-book/14j6g.png)

"""

