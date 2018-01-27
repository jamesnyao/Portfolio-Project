#include <iostream>

#include "Profile.hpp"

using namespace std;

int main(int argc, char **argv)
{
    Profile p(1);
    p.add_position("ABC", 10);

    cout << p.get_id() << p[1].get_price() << endl;

    return 0;
}
