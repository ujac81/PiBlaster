
#include "RFCommClient.h"
#include "RFCommThread.h"

#ifndef DUMMY_MODE
    #include <QtAndroidExtras/QAndroidJniObject>
#endif

#include <QThread>
#include <QtDebug>



RFCommClient::RFCommClient(QObject *parent, QGuiApplication* app)
    : QObject(parent),
    _app(app)
{
    connect(this, SIGNAL(notificationChanged()), this, SLOT(updateAndroidNotification()));

#ifndef DUMMY_MODE
    QAndroidJniObject::callStaticMethod<void>( "org/piblaster/piblaster/rfcomm/RfcommClient", "onInit" );
#endif
}


void RFCommClient::setNotification(const QString &notification)
{
    if ( _notification == notification ) return;
    _notification = notification;
    emit notificationChanged();
}


void RFCommClient::updateAndroidNotification()
{
#ifndef DUMMY_MODE
    QAndroidJniObject javaNotification = QAndroidJniObject::fromString(_notification);
    QAndroidJniObject::callStaticMethod<void>("org/piblaster/piblaster/rfcomm/RfcommClient",
                                              "notify", "(Ljava/lang/String;)V",
                                              javaNotification.object<jstring>());
#endif
}


int RFCommClient::tryConnect()
{
#ifndef DUMMY_MODE
    jint res = QAndroidJniObject::callStaticMethod<jint>("org/piblaster/piblaster/rfcomm/RfcommClient",
                                                         "tryConnect");
    return res;
#else
    return 3;
#endif
}

int RFCommClient::disconnect()
{
#ifndef DUMMY_MODE
    jint res = QAndroidJniObject::callStaticMethod<jint>( "org/piblaster/piblaster/rfcomm/RfcommClient",
                                                          "disconnect" );
    return res;
#else
    return 0;
#endif
}

int RFCommClient::disableBT()
{
#ifndef DUMMY_MODE
    jint res = QAndroidJniObject::callStaticMethod<jint>( "org/piblaster/piblaster/rfcomm/RfcommClient",
                                                          "disableBT" );
    return res;
#else
    return 0;
#endif
}

int RFCommClient::connectionStatus()
{
#ifndef DUMMY_MODE
    jint res = QAndroidJniObject::callStaticMethod<jint>( "org/piblaster/piblaster/rfcomm/RfcommClient",
                                                          "bluetoothConnectionStatus" );
    return res;
#else
    return 3;
#endif
}


int RFCommClient::initAndCountBluetoothMessages()
{
    _logentries.clear();
#ifndef DUMMY_MODE
    int count = QAndroidJniObject::callStaticMethod<jint>("org/piblaster/piblaster/rfcomm/RfcommClient",
                                                          "bluetoothMessagesCount");
    for ( int i = 0; i < count; i++ )
    {
        QAndroidJniObject string = QAndroidJniObject::callStaticObjectMethod(
                    "org/piblaster/piblaster/rfcomm/RfcommClient",
                    "bluetoothMessage", "(I)Ljava/lang/String;", i );
        _logentries.append( string.toString() );
    }
#else
    _logentries.append( "Some funny" );
    _logentries.append( "bluetooth messages" );
    _logentries.append( "in here" );
#endif
    _curlogentry = 0;
    return _logentries.size();
}


int RFCommClient::execCommand(const QString& command)
{
    _cmdResult.clear();

#ifndef DUMMY_MODE

    QAndroidJniObject javaCommand = QAndroidJniObject::fromString(command);
    int count = QAndroidJniObject::callStaticMethod<jint>(
                "org/piblaster/piblaster/rfcomm/RfcommClient",
                "sendReceive", "(Ljava/lang/String;)I", javaCommand.object<jstring>() );

    for ( int i = 0; i < count; i++ )
    {
        QAndroidJniObject string = QAndroidJniObject::callStaticObjectMethod(
                    "org/piblaster/piblaster/rfcomm/RfcommClient",
                    "rfcommMessage", "(I)Ljava/lang/String;", i );
        if ( i == 0 )
            _status = string.toString().toInt();
        if ( i == 1 )
            _statusMessage = string.toString();
        if ( i > 2 )
            _cmdResult.append( string.toString() );
    }

#else

    if ( command == "showdevices" )
    {
        _cmdResult.append("||0||DACE-470F||StormTrooper||1||11||90||2.95 GB||759.81 MB||");
        _cmdResult.append("||1||AA17-F608||Weisser32GB Ulli||1||344||1678||18.8 GB||10.13 GB||");
    }
    if ( command == "lsdirs 1 0" )
    {
        _cmdResult.append("||1||1||0||3||0||2013NOAF||");
        _cmdResult.append("||1||118||0||19||0||Alben||");
        _cmdResult.append("||1||252||0||31||0||Extreme_Metal3||");
        _cmdResult.append("||1||339||0||0||0||Music||");
        _cmdResult.append("||1||340||0||0||105||PartyMetal||");
        _cmdResult.append("||1||341||0||3||0||bilder||");
    }
    if ( command == "lsfiles 1 340" )
    {
        _cmdResult.append("||1||340||1||4:23||Amon Amarth||Twilight Of The Thunder God||Guardians Of Asgaard||");
        _cmdResult.append("||1||340||2||4:18||Amon Amarth||Twilight Of The Thunder God||Varyags Of Miklagaard||");
        _cmdResult.append("||1||340||3||||Amon Amarth||Versus The World||Death in Fire||");
        _cmdResult.append("||1||340||4||||Amon Amarth||With Oden On Our Side||Asator||");
        _cmdResult.append("||1||340||5||4:05||Amorphis||Elegy||Against Widows||");
        _cmdResult.append("||1||340||6||5:40||Anthrax||Return of the killer A's||Indians||");
        _cmdResult.append("||1||340||7||||Arch Enemy||Anthems Of Rebellion||We Will Rise||");
        _cmdResult.append("||1||340||8||||Arch Enemy||Anthems Of Rebellion||Dead Eyes See No Future||");
        _cmdResult.append("||1||340||9||||Arch Enemy||Doomsday Machine||My Apocalypse||");
        _cmdResult.append("||1||340||10||||At The Gates||Suicidal Final Art||Blinded By Fear||");
        _cmdResult.append("||1||340||11||||Black Sabbath||Black Sabbath||The Wizard||");
        _cmdResult.append("||1||340||12||2:52||Black Sabbath||Paranoid||Paranoid||");
        _cmdResult.append("||1||340||13||||Blind Guardian||Follow the blind||Valhalla||");
        _cmdResult.append("||1||340||14||||Blind Guardian||Imaginations from the other Side||Mordred's Song||");
        _cmdResult.append("||1||340||15||5:06||Blind Guardian||Nightfall In Middle-Earth||Mirror Mirror||");
        _cmdResult.append("||1||340||16||||Blind Guardian||Somewhere Far Beyond||Journey Through The Dark||");
        _cmdResult.append("||1||340||17||||Blind Guardian||Somewhere Far Beyond||Ashes To Ashes||");
        _cmdResult.append("||1||340||18||||Blind Guardian||Somewhere Far Beyond||Somewhere Far Beyond||");
        _cmdResult.append("||1||340||19||4:50||Blind Guardian||Tales from the Twilight World||Welcome To Dying||");
        _cmdResult.append("||1||340||20||||Bolt Thrower||Mercenary||No Guts, No Glory||");
        _cmdResult.append("||1||340||21||||Bolt Thrower||Those Once Loyal||At first Light||");
        _cmdResult.append("||1||340||22||||Bolt Thrower||Those Once Loyal||Entrenched||");
        _cmdResult.append("||1||340||23||||Bolt Thrower||Those Once Loyal||The Killchain||");
        _cmdResult.append("||1||340||24||||Children Of Bodom||Downfall||Downfall||");
        _cmdResult.append("||1||340||25||||Children Of Bodom||Follow The Reaper||Bodom After Midnight||");
        _cmdResult.append("||1||340||26||||Children Of Bodom||Follow The Reaper||Everytime I Die||");
        _cmdResult.append("||1||340||27||||Children Of Bodom||Skeletons In The Closet||Aces High||");
        _cmdResult.append("||1||340||28||||Children Of Bodom||Skeletons In The Closet||Rebel Yell||");
        _cmdResult.append("||1||340||29||||Dark Tranquillity||A Closer End||22 Acacia Avenue||");
        _cmdResult.append("||1||340||30||||Dark Tranquillity||Damage Done||Hours Passed in Exile||");
        _cmdResult.append("||1||340||31||||Dark Tranquillity||Damage Done||Cathode Ray Sunshine||");
        _cmdResult.append("||1||340||32||||Die Apokalyptischen Reiter||Riders on the Storm||Riders on the Storm||");
        _cmdResult.append("||1||340||33||||Ensiferum||Ensiferum||Guardians of Fate||");
        _cmdResult.append("||1||340||34||||Ensiferum||Iron||Iron||");
        _cmdResult.append("||1||340||35||||Ensiferum||Iron||Sword Chant||");
        _cmdResult.append("||1||340||36||||Equilibrium||Sagas||Blut im Auge||");
        _cmdResult.append("||1||340||37||||Equilibrium||Sagas||Unbesiegt||");
        _cmdResult.append("||1||340||38||||Equilibrium||Turis Fratyr||Wingthors Hammer||");
        _cmdResult.append("||1||340||39||4:41||Evil Hedgehog||Rising||Dressed in Black||");
        _cmdResult.append("||1||340||40||5:44||Evil Hedgehog||Rising||One Thousand Voices||");
        _cmdResult.append("||1||340||41||||Evocation||Tales from the Tomb||Feed the Fire||");
        _cmdResult.append("||1||340||42||2:32||Excrementory Grindfuckers||Bitte nicht vor den Gästen||Nein kein Grindcore||");
        _cmdResult.append("||1||340||43||1:44||Excrementory Grindfuckers||Bitte nicht vor den Gästen||Halb und Halb||");
        _cmdResult.append("||1||340||44||||Excrementory Grindfuckers||Excrementory Grindfuckers||Vater Morgana||");
        _cmdResult.append("||1||340||45||||Excrementory Grindfuckers||Headliner Der Herzen||Grindcore Vibes||");
        _cmdResult.append("||1||340||46||||Fear Factory||Demanufacture||Demanufacture||");
        _cmdResult.append("||1||340||47||||Fear Factory||Demanufacture||Replica||");
        _cmdResult.append("||1||340||48||||Grailknights||Return To Castle Grailskull||Moonlit Masquerade||");
        _cmdResult.append("||1||340||49||||Grailknights||Return To Castle Grailskull||Fight Until You Die||");
        _cmdResult.append("||1||340||50||4:45||Grave Digger||Excalibur||Excalibur||");
        _cmdResult.append("||1||340||51||||Grave Digger||Rheingold||Maidens Of War||");
        _cmdResult.append("||1||340||52||4:32||Grave Digger||Tunes Of War||The Dark Of The Sun||");
        _cmdResult.append("||1||340||53||4:05||Grave Digger||Tunes Of War||Rebellion (The Clans Are Marching)||");
        _cmdResult.append("||1||340||54||||Grave Digger||Witch Hunter||Witch Hunter||");
        _cmdResult.append("||1||340||55||4:34||Graveworm||Collateral Defect||I Need A Hero||");
        _cmdResult.append("||1||340||56||4:49||Hammerfall||Glory To The Brave||Hammerfall||");
        _cmdResult.append("||1||340||57||3:44||Hammerfall||Glory To The Brave||Child Of The Damned||");
        _cmdResult.append("||1||340||58||5:14||Hypocrisy||10 Years of Chaos and Confusion||Fractured Millennium||");
        _cmdResult.append("||1||340||59||||Hypocrisy||Abducted||Killing Art||");
        _cmdResult.append("||1||340||60||||Hypocrisy||The Arrival||War within||");
        _cmdResult.append("||1||340||61||||Hypocrisy||Virus||Compulsive Psychosis||");
        _cmdResult.append("||1||340||62||||Iced Earth||Burnt Offerings||Last December||");
        _cmdResult.append("||1||340||63||3:43||Iced Earth||Something Wicked This Way Comes||Burning Times||");
        _cmdResult.append("||1||340||64||||Iced Earth||The Dark Saga||The Hunter||");
        _cmdResult.append("||1||340||65||4:42||In Flames||Clayman||Bullet Ride||");
        _cmdResult.append("||1||340||66||||In Flames||Colony||Colony||");
        _cmdResult.append("||1||340||67||||In Flames||Reroute to Remain||Cloud Connected||");
        _cmdResult.append("||1||340||68||3:17||Iron Maiden||Iron Maiden||Running Free||");
        _cmdResult.append("||1||340||69||5:00||Iron Maiden||Killers||Killers||");
        _cmdResult.append("||1||340||70||6:36||Iron Maiden||The Number Of The Beast||22 Acacia Avenue||");
        _cmdResult.append("||1||340||71||7:11||Iron Maiden||The Number Of The Beast||Hallowed Be Thy Name||");
        _cmdResult.append("||1||340||72||||Judas Priest||British Steel||Breaking the Law||");
        _cmdResult.append("||1||340||73||||Judas Priest||Defenders of the Faith||The Sentinel||");
        _cmdResult.append("||1||340||74||||Judas Priest||Defenders of the Faith||Love Bites||");
        _cmdResult.append("||1||340||75||||Judas Priest||Painkiller||Painkiller||");
        _cmdResult.append("||1||340||76||||Korpiklaani||Spirit of the Forest||Wooden Pints||");
        _cmdResult.append("||1||340||77||||Korpiklaani||Voice of Wilderness||Beer Beer||");
        _cmdResult.append("||1||340||78||||Kreator||Enemy Of God||Enemy Of God||");
        _cmdResult.append("||1||340||79||||Kreator||Hordes Of Chaos||hordes of chaos (a necrologue for the elite)||");
        _cmdResult.append("||1||340||80||||Kreator||Hordes Of Chaos||warcurse||");
        _cmdResult.append("||1||340||81||||Kreator||Phantom Antichrist||Civilisation Collapse||");
        _cmdResult.append("||1||340||82||||Kreator||Phantom Antichrist||United In Hate||");
        _cmdResult.append("||1||340||83||||Manowar||Hail To England||Each Dawn I Die||");
        _cmdResult.append("||1||340||84||||Manowar||Hail To England||Kill with Power||");
        _cmdResult.append("||1||340||85||||Manowar||Into Glory Ride||Gloves of Metal||");
        _cmdResult.append("||1||340||86||||Manowar||Kings Of Metal||Hail And Kill||");
        _cmdResult.append("||1||340||87||||Manowar||Kings Of Metal||Blood Of The Kings||");
        _cmdResult.append("||1||340||88||||Manowar||Louder Than Hell||The Power||");
        _cmdResult.append("||1||340||89||||Pantera||Cowboys From Hell||Cowboys From Hell||");
        _cmdResult.append("||1||340||90||||Pantera||Vulgar Display of Power||Fucking Hostile||");
        _cmdResult.append("||1||340||91||||Pantera||Vulgar Display of Power||This Love||");
        _cmdResult.append("||1||340||92||||Powerwolf||Blood of the Saints||We Drink Your Blood||");
        _cmdResult.append("||1||340||93||||Powerwolf||Blood of the Saints||Die, Die, Crucified||");
        _cmdResult.append("||1||340||94||||Rammstein||Herzeleid||Wollt Ihr Das Bett In Flammen||");
        _cmdResult.append("||1||340||95||||Rammstein||Herzleid||Rammstein||");
        _cmdResult.append("||1||340||96||||Savatage||Dead Winter Dead||Doesn't Matter Anyway||");
        _cmdResult.append("||1||340||97||||Savatage||Hall Of The Mountain King||Hall Of The Mountain King||");
        _cmdResult.append("||1||340||98||||Slayer||Soundtrack To The Apocalypse||Angel Of Death||");
        _cmdResult.append("||1||340||99||||Slayer||Soundtrack To The Apocalypse||Raining Blood||");
        _cmdResult.append("||1||340||100||||Slayer||World Painted Blood||World Painted Blood||");
        _cmdResult.append("||1||340||101||||Sodom||In War And Pieces||In War And Pieces||");
        _cmdResult.append("||1||340||102||||Sodom||In War And Pieces||Hellfire||");
        _cmdResult.append("||1||340||103||||Testament||First Strike Still Deadly||The Preacher||");
        _cmdResult.append("||1||340||104||||Testament||First Strike Still Deadly||Alone In The Dark||");
        _cmdResult.append("||1||340||105||||Turbonegro||Sexual Harassment||Dude Without a Face||");
    }

    _statusMessage = "OK.";
    _status = 0;
#endif

    // postprocess results
    _cmdResultFields.clear();
    for ( int i = 0; i < _cmdResult.size(); ++i )
    {
        _cmdResultFields.append( _cmdResult.at( i ).split("||") );
    }

    return _status;
}


void RFCommClient::preparePlaylistAdd( int mode )
{
    _plAddList.clear();
    _plAddMode = mode;
}


void RFCommClient::addPlaylistItem( const QString&row )
{
    _plAddList.append( row );
}


int RFCommClient::sendPlaylistAdd()
{
    RFCommThread* send = new RFCommThread( this );
    connect( send, &RFCommThread::gotReply, this, &RFCommClient::addToPlaylistFinished );
    connect( send, &RFCommThread::finished, send, &QObject::deleteLater );
    send->start();
    return 0;
}



