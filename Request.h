#ifndef PORTFOLIO_SRC_REQUEST_H
#define PORTFOLIO_SRC_REQUEST_H

#include <string>
#include <sstream>

class Request
{
  private:

    std::string text;
    
  public:

    Request(std::string _url);

};

#endif
