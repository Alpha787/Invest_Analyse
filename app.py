import pandas as pd

# use - arch -x86_64 python app.py to start program
df1 = pd.DataFrame([['a', 'b'], ['c', 'd']],
                    index=['row 1', 'row 2'],
                    columns=['col 1', 'col 2'])
df1.to_excel("output2.xlsx")  



