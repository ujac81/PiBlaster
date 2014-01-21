
#ifndef HELPERS_H
#define HELPERS_H


#include <QGuiApplication>
#include <QDebug>


class Helpers : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int wait READ wait WRITE setWait)


public:
    explicit Helpers(QObject *parent = 0, QGuiApplication* app = 0);


    /// @brief set to 0 to stop wait loop
    void setWait(const int& w) { _waitLoop = w; }

    /// @brief unrequired read accessor for wait loop flag
    int wait() const { return _waitLoop; }


    /// @brief Wait until wait is set to 0, process events while waiting
    Q_INVOKABLE void waitLoop();


private:

    QGuiApplication* _app;


    int _waitLoop;



};

#endif // HELPERS_H
