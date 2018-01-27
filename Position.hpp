#ifndef PORTFOLIO_SRC_POSITION_HPP
#define PORTFOLIO_SRC_POSITION_HPP

#include <string>

using namespace std;

class Position 
{
  private:

    string ticker;

    int shares;

    float price;

  public:

    Position(string _ticker, int _shares)
    {
        ticker = _ticker;
        shares = _shares;
        price = -1;
    }

    string get_ticker()
    {
        return ticker;
    }

    int get_shares()
    {
        return shares;
    }

    float get_price()
    {
        return price;
    }

    void update_price()
    {
        price = -2;
    }
};

#endif
