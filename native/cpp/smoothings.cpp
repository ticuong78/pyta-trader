#include <vector> //Thư viện C++ dùng để tạo dynamic array (Chuẩn C++, còn nhiều thứ nữa) 

double calculate_sma (const std::vector<double> & prices, int period) //hàm SMA
{
    if (prices.size() < period || period <= 0) //dữ liệu không đủ hoặc không hợp lệ sẽ return
    return 0.0;

    double sum = 0.0;

    for (int i = 0; i < period; i++) //Tính tổng các phần tử đầu tiên theo từng chu kỳ 
        sum += prices[i];
    return sum / period; //giá trị Avg của sma 
}

std::vector<double> calculate_ema (const std::vector<double> & prices, int period) //hàm EMA
{
    std::vector<double> ema;

    if (prices.size() < period || period <= 0)
    return ema;

    double alpha = 2.0 / (period + 1); //Tính alpha
    double sma = calculate_sma(prices, period); //Dùng SMA làm bờ vai cho EMA tựa đầu vào
    ema.insert(ema.end(), period - 1, NAN); //padding
    ema.push_back(sma); //EMA với anh SMA là giá trị ban đầu

    //tính EMA cho các phần tử còn lại
    for (size_t i = period; i < prices.size(); i++ )
    {
        double next = alpha * prices[i] + (1 - alpha) * ema.back(); //Công thức ema
        ema.push_back(next);
    }
    return ema;
}