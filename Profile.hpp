#ifndef PORTFOLIO_SRC_PROFILE_HPP
#define PORTFOLIO_SRC_PROFILE_HPP

#include <vector>

#include "Position.hpp"

using namespace std;

class Profile
{
  private:

    int id;

    vector<Position> positions;

  public:

    Profile(int _id)
    {
        id = _id;
    }

    int get_id()
    {
        return id;
    }

    Position operator[](int i)
    {
        if (i < 0 || i >= positions.size())
        {
            cerr << "Out of vector bounds" << endl;
            throw exception();
        }
        return positions[i];
    }

    void add_position(string ticker, int shares)
    {
        positions.push_back(Position(ticker, shares));
    }
};

#endif
