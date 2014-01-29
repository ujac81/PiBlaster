#ifndef RFCOMMMESSAGEOBJECT_H
#define RFCOMMMESSAGEOBJECT_H


#include <QList>
#include <QObject>
#include <QString>

class RFCommMessageObject : public QObject
{
    Q_OBJECT

public:

    Q_INVOKABLE RFCommMessageObject( QObject* parent = 0 ) : QObject( parent ),
        _id(-1),
        _status(-1),
        _code(-1),
        _plSize(0)
    {}

    Q_INVOKABLE RFCommMessageObject( const RFCommMessageObject& copy ) :
        QObject(),
        _id( copy._id ),
        _status( copy._status ),
        _code( copy._code ),
        _plSize( copy._plSize ),
        _cmd( copy._cmd ),
        _payload( copy._payload )
    {}

    RFCommMessageObject( int id, int status, int code, int plSize, const QString& cmd ) :
        QObject(),
        _id( id ),
        _status( status ),
        _code( code ),
        _plSize( plSize ),
        _cmd( cmd )
    {}

    Q_INVOKABLE virtual ~RFCommMessageObject() {}

    Q_INVOKABLE int id() const { return _id; }
    Q_INVOKABLE int status() const { return _status; }
    Q_INVOKABLE int code() const { return _code; }
    Q_INVOKABLE QString message() const { return _cmd; }

    bool payloadComplete() const { return _plSize == _payload.size(); }

    Q_INVOKABLE int payloadSize() const { return _payload.size(); }
    Q_INVOKABLE QString payload( int i ) const { return _payload[i]; }

    bool addPayload( const QString& line )
    {
        _payload.push_back( line );
        return payloadComplete();
    }



private:
    int                 _id;
    int                 _status;
    int                 _code;
    int                 _plSize;
    QString             _cmd;

    QList<QString>      _payload;


};


Q_DECLARE_METATYPE(RFCommMessageObject)


#endif // RFCOMMMESSAGEOBJECT_H
