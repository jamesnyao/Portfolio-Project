#include "Request.h"

using namespace std;

Request::Request(string url)
{
    text = cpr::Get(cpr::Url{"http://httpbin.org/get"}).text;
}


