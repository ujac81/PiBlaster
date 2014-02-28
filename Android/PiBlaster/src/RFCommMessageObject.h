#ifndef RFCOMMMESSAGEOBJECT_H
#define RFCOMMMESSAGEOBJECT_H


#include <QList>
#include <QObject>
#include <QString>
#include <QStringList>

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
        _payload( copy._payload ),
        _payloadElements( copy._payloadElements )
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

    Q_INVOKABLE QList<QString> payloadElements( int i ) const { return _payloadElements[i]; }

    bool addPayload( const QString& line )
    {
        _payload.push_back( line );
        return payloadComplete();
    }

    /**
     * @brief Split each payload line and store results in payloadElements(i)
     * Called in RFCommMaster before sendig to QML app
     */
    void preparePayloadElements()
    {
        _payloadElements.clear();
        for ( int i = 0; i < _payload.size(); ++i )
        {
            QString line = _payload[i];
            int toks = line.left(2).toInt();
            int pos = 2;
            QList<QString> plLine;
            for ( int j = 0; j < toks; ++j )
            {
                int plSubSize = line.mid(pos, 3).toInt();
                pos += 3;
                plLine.append( line.mid(pos, plSubSize) );
                pos += plSubSize;
            }
            _payloadElements.append( plLine );
        }
    }


private:


    int                 _id;
    int                 _status;
    int                 _code;
    int                 _plSize;
    QString             _cmd;

    QList<QString>          _payload;
    QList<QList<QString> >  _payloadElements;


};


Q_DECLARE_METATYPE(RFCommMessageObject)


#endif // RFCOMMMESSAGEOBJECT_H
