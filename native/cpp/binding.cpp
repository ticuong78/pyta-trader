#include <pybind11/pybind11.h> //Dùng thư viện này để tạo modules Py từ C++
#include <pybind11/stl.h> //Cái này giúp tự động chuyển đổi hàm và dữ liệu từ C++ sang Python
#include <vector> //Thư viện C++ dùng để tạo dynamic array (Chuẩn C++, còn nhiều thứ nữa) 

using namespace std;

double calculate_sma (const vector<double> & prices, int period); //hàm SMA
vector<double> calculate_ema (const vector<double> & prices, int period); //hàm EMA

//Tạo module có tên như bên dưới
PYBIND11_MODULE(smoothing_cpp, m) 
{
    m.def("calculate_sma", &calculate_sma, "Calculate SMA"); //Đăng ký sản phẩm với nhà Py
    m.def("calculate_ema", &calculate_ema, "Calculate EMA"); //Đăng ký sản phẩm với nhà Py
}