import pandas as pd
import dataframe_pointer


def test_df_pointer_differs_by_df():
    df1 = pd.DataFrame({'a': range(1000)})
    df2 = pd.DataFrame({'a': range(200)})
    df3 = pd.DataFrame({'1234': range(4000)})
    point1 = df1.pointer()
    point2 = df2.pointer()
    point3 = df3.pointer()
    pd.testing.assert_frame_equal(point1.df, df1)
    assert point1 != point2
    assert point2 != point3
    assert point1 != point3
    assert point1 == df1.pointer()
    assert point1 == df1.copy().pointer()