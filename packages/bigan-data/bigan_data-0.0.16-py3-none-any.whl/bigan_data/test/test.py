from datetime import datetime

import akshare as ak
import numpy
import numpy as np

from bigan_data.db.PostgresqlAdapter import PostgresqlAdapter
from bigan_data.math.GreyRelationAnalyzer import GreyRelationAnalyzer
from bigan_data.model.AKShareSyncModel import get_akshare_stock_info_a_code_name, get_akshare_stock_zh_a_hist
from bigan_data.model.AKShareSyncModelClean import clean_akshare_stock_info_a_code_name


def cal_relation(calculate_range: int):
    array = stock_zh_index_daily_em_df["close"].to_numpy()
    time_arr = stock_zh_index_daily_em_df["date"].to_numpy()
    # array = array[:-5]
    # time_arr = time_arr[:-5]
    arr_len = len(array)
    cal = list()
    for i in range(arr_len - 1):
        cal.append(array[i])
    # calculate range 20
    arr_len = arr_len - 1
    reference_seq = list()
    for i in range(arr_len - calculate_range, arr_len):
        reference_seq.append(cal[i])
    gra = GreyRelationAnalyzer(resolution_factor=0.5, reference_seq=reference_seq)
    for i in range(arr_len - calculate_range):
        sub_seq = cal[i:i + calculate_range]
        gra.add_analysis_seq(sub_seq)
    res = gra.analysis_res()
    # print(res)
    max_index = np.argmax(res)
    max_val = np.max(res)
    print("--------------------------")
    print("calculate_range:", calculate_range)
    print("max_index:", max_index, ",max_val:", max_val)
    print(time_arr[max_index + calculate_range - 1])


if __name__ == '__main__':
    # print("test")
    # start_date = "20230101"
    # today = datetime.today().strftime('%Y%m%d')
    # print(today)
    # pg = PostgresqlAdapter()
    # clean_akshare_stock_info_a_code_name(pg, today)
    # stocks = get_akshare_stock_info_a_code_name()
    # #pg.add_entities(stocks)
    # for stock in stocks:
    #     stock_zh_a_hist = get_akshare_stock_zh_a_hist(stock.code, start_date, today)
    #     print(stock_zh_a_hist)
    #     pg.add_entities(stock_zh_a_hist)
    # stock_zh_index_daily_tx_df = ak.stock_zh_index_daily_tx(symbol="sh000001")
    # print(stock_zh_index_daily_tx_df)

    # gra = GreyRelationAnalyzer(reference_seq=[1988, 2062, 2335, 2750, 3356, 3806])
    # gra.add_analysis_seq([386, 408, 422, 482, 511, 561])
    # gra.add_analysis_seq([839, 846, 960, 1258, 1577, 1893])
    # gra.add_analysis_seq([763, 808, 953, 1010, 1268, 1352])
    # print( gra.analysis_res())

    # stock_zh_index_daily_em_df = ak.stock_zh_index_daily_em(symbol="sz399300")
    stock_zh_index_daily_em_df = ak.stock_zh_index_daily_em(symbol="sh000001")
    for range_val in range(5, 41):
        cal_relation(range_val)
