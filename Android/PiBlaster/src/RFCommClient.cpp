

#include "RFCommClient.h"

#ifndef DUMMY_MODE
    #include <QtAndroidExtras/QAndroidJniObject>
#endif
#include <QtDebug>

RFCOMMClient::RFCOMMClient(QObject *parent)
    : QObject(parent)
{
    connect(this, SIGNAL(notificationChanged()), this, SLOT(updateAndroidNotification()));

#ifndef DUMMY_MODE
    QAndroidJniObject::callStaticMethod<void>( "org/piblaster/piblaster/rfcomm/RfcommClient", "onInit" );
#endif
}

void RFCOMMClient::setNotification(const QString &notification)
{
    if (m_notification == notification) return;
    m_notification = notification;
    emit notificationChanged();
}

void RFCOMMClient::updateAndroidNotification()
{
    qDebug() << "updateNotification: " << m_notification;

#ifndef DUMMY_MODE
    QAndroidJniObject javaNotification = QAndroidJniObject::fromString(m_notification);
    QAndroidJniObject::callStaticMethod<void>("org/piblaster/piblaster/rfcomm/RfcommClient",
                                              "notify", "(Ljava/lang/String;)V",
                                              javaNotification.object<jstring>());
#endif
}


int RFCOMMClient::tryConnect()
{
#ifndef DUMMY_MODE
    jint res = QAndroidJniObject::callStaticMethod<jint>("org/piblaster/piblaster/rfcomm/RfcommClient",
                                                         "tryConnect");

    qDebug() << "RFCOMMClient::tryConnect(): " << res;
    return res;
#else
    return 3;
#endif
}

int RFCOMMClient::disconnect()
{
#ifndef DUMMY_MODE
    jint res = QAndroidJniObject::callStaticMethod<jint>( "org/piblaster/piblaster/rfcomm/RfcommClient",
                                                          "disconnect" );
    qDebug() << "RFCOMMClient::disconnect(): " << res;
    return res;
#else
    return 0;
#endif
}

int RFCOMMClient::disableBT()
{
#ifndef DUMMY_MODE
    jint res = QAndroidJniObject::callStaticMethod<jint>( "org/piblaster/piblaster/rfcomm/RfcommClient",
                                                          "disableBT" );
    qDebug() << "RFCOMMClient::disableBT(): " << res;
    return res;
#else
    return 0;
#endif
}

int RFCOMMClient::connectionStatus()
{
#ifndef DUMMY_MODE
    jint res = QAndroidJniObject::callStaticMethod<jint>( "org/piblaster/piblaster/rfcomm/RfcommClient",
                                                          "bluetoothConnectionStatus" );
    qDebug() << "RFCOMMClient::connectionStatus(): " << res;
    return res;
#else
    return 3;
#endif
}


int RFCOMMClient::initAndCountBluetoothMessages()
{
    m_logentries.clear();
#ifndef DUMMY_MODE
    int count = QAndroidJniObject::callStaticMethod<jint>("org/piblaster/piblaster/rfcomm/RfcommClient",
                                                          "bluetoothMessagesCount");
    for ( int i = 0; i < count; i++ )
    {
        QAndroidJniObject string = QAndroidJniObject::callStaticObjectMethod(
                    "org/piblaster/piblaster/rfcomm/RfcommClient",
                    "bluetoothMessage", "(I)Ljava/lang/String;", i );
        m_logentries.append( string.toString() );
    }
#else
    m_logentries.append( "Some funny" );
    m_logentries.append( "bluetooth messages" );
    m_logentries.append( "in here" );
#endif
    m_curlogentry = 0;
    return m_logentries.size();
}


int RFCOMMClient::execCommand(const QString& command)
{
    qDebug() << "Invoking: " << command;

    m_cmdResult.clear();

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
            m_status = string.toString().toInt();
        if ( i == 1 )
            m_statusMessage = string.toString();
        if ( i > 2 )
            m_cmdResult.append( string.toString() );
    }

#else

    if ( command == "showdevices" )
    {
        m_cmdResult.append("||0||DACE-470F||StormTrooper||1||11||90||2.95 GB||759.81 MB||");
        m_cmdResult.append("||1||AA17-F608||Weisser32GB Ulli||1||344||1678||18.8 GB||10.13 GB||");
    }
    if ( command == "lsdirs 1 0" )
    {
        m_cmdResult.append("||1||1||0||3||0||2013NOAF||");
        m_cmdResult.append("||1||118||0||19||0||Alben||");
        m_cmdResult.append("||1||252||0||31||0||Extreme_Metal3||");
        m_cmdResult.append("||1||339||0||0||0||Music||");
        m_cmdResult.append("||1||340||0||0||105||PartyMetal||");
        m_cmdResult.append("||1||341||0||3||0||bilder||");
    }
    if ( command == "lsfiles 1 340" )
    {
        m_cmdResult.append("||1||340||1||4:23||Amon Amarth||Twilight Of The Thunder God||Guardians Of Asgaard||");
        m_cmdResult.append("||1||340||2||4:18||Amon Amarth||Twilight Of The Thunder God||Varyags Of Miklagaard||");
        m_cmdResult.append("||1||340||3||||Amon Amarth||Versus The World||Death in Fire||");
        m_cmdResult.append("||1||340||4||||Amon Amarth||With Oden On Our Side||Asator||");
        m_cmdResult.append("||1||340||5||4:05||Amorphis||Elegy||Against Widows||");
        m_cmdResult.append("||1||340||6||5:40||Anthrax||Return of the killer A's||Indians||");
        m_cmdResult.append("||1||340||7||||Arch Enemy||Anthems Of Rebellion||We Will Rise||");
        m_cmdResult.append("||1||340||8||||Arch Enemy||Anthems Of Rebellion||Dead Eyes See No Future||");
        m_cmdResult.append("||1||340||9||||Arch Enemy||Doomsday Machine||My Apocalypse||");
        m_cmdResult.append("||1||340||10||||At The Gates||Suicidal Final Art||Blinded By Fear||");
        m_cmdResult.append("||1||340||11||||Black Sabbath||Black Sabbath||The Wizard||");
        m_cmdResult.append("||1||340||12||2:52||Black Sabbath||Paranoid||Paranoid||");
        m_cmdResult.append("||1||340||13||||Blind Guardian||Follow the blind||Valhalla||");
        m_cmdResult.append("||1||340||14||||Blind Guardian||Imaginations from the other Side||Mordred's Song||");
        m_cmdResult.append("||1||340||15||5:06||Blind Guardian||Nightfall In Middle-Earth||Mirror Mirror||");
        m_cmdResult.append("||1||340||16||||Blind Guardian||Somewhere Far Beyond||Journey Through The Dark||");
        m_cmdResult.append("||1||340||17||||Blind Guardian||Somewhere Far Beyond||Ashes To Ashes||");
        m_cmdResult.append("||1||340||18||||Blind Guardian||Somewhere Far Beyond||Somewhere Far Beyond||");
        m_cmdResult.append("||1||340||19||4:50||Blind Guardian||Tales from the Twilight World||Welcome To Dying||");
        m_cmdResult.append("||1||340||20||||Bolt Thrower||Mercenary||No Guts, No Glory||");
        m_cmdResult.append("||1||340||21||||Bolt Thrower||Those Once Loyal||At first Light||");
        m_cmdResult.append("||1||340||22||||Bolt Thrower||Those Once Loyal||Entrenched||");
        m_cmdResult.append("||1||340||23||||Bolt Thrower||Those Once Loyal||The Killchain||");
        m_cmdResult.append("||1||340||24||||Children Of Bodom||Downfall||Downfall||");
        m_cmdResult.append("||1||340||25||||Children Of Bodom||Follow The Reaper||Bodom After Midnight||");
        m_cmdResult.append("||1||340||26||||Children Of Bodom||Follow The Reaper||Everytime I Die||");
        m_cmdResult.append("||1||340||27||||Children Of Bodom||Skeletons In The Closet||Aces High||");
        m_cmdResult.append("||1||340||28||||Children Of Bodom||Skeletons In The Closet||Rebel Yell||");
        m_cmdResult.append("||1||340||29||||Dark Tranquillity||A Closer End||22 Acacia Avenue||");
        m_cmdResult.append("||1||340||30||||Dark Tranquillity||Damage Done||Hours Passed in Exile||");
        m_cmdResult.append("||1||340||31||||Dark Tranquillity||Damage Done||Cathode Ray Sunshine||");
        m_cmdResult.append("||1||340||32||||Die Apokalyptischen Reiter||Riders on the Storm||Riders on the Storm||");
        m_cmdResult.append("||1||340||33||||Ensiferum||Ensiferum||Guardians of Fate||");
        m_cmdResult.append("||1||340||34||||Ensiferum||Iron||Iron||");
        m_cmdResult.append("||1||340||35||||Ensiferum||Iron||Sword Chant||");
        m_cmdResult.append("||1||340||36||||Equilibrium||Sagas||Blut im Auge||");
        m_cmdResult.append("||1||340||37||||Equilibrium||Sagas||Unbesiegt||");
        m_cmdResult.append("||1||340||38||||Equilibrium||Turis Fratyr||Wingthors Hammer||");
        m_cmdResult.append("||1||340||39||4:41||Evil Hedgehog||Rising||Dressed in Black||");
        m_cmdResult.append("||1||340||40||5:44||Evil Hedgehog||Rising||One Thousand Voices||");
        m_cmdResult.append("||1||340||41||||Evocation||Tales from the Tomb||Feed the Fire||");
        m_cmdResult.append("||1||340||42||2:32||Excrementory Grindfuckers||Bitte nicht vor den Gästen||Nein kein Grindcore||");
        m_cmdResult.append("||1||340||43||1:44||Excrementory Grindfuckers||Bitte nicht vor den Gästen||Halb und Halb||");
        m_cmdResult.append("||1||340||44||||Excrementory Grindfuckers||Excrementory Grindfuckers||Vater Morgana||");
        m_cmdResult.append("||1||340||45||||Excrementory Grindfuckers||Headliner Der Herzen||Grindcore Vibes||");
        m_cmdResult.append("||1||340||46||||Fear Factory||Demanufacture||Demanufacture||");
        m_cmdResult.append("||1||340||47||||Fear Factory||Demanufacture||Replica||");
        m_cmdResult.append("||1||340||48||||Grailknights||Return To Castle Grailskull||Moonlit Masquerade||");
        m_cmdResult.append("||1||340||49||||Grailknights||Return To Castle Grailskull||Fight Until You Die||");
        m_cmdResult.append("||1||340||50||4:45||Grave Digger||Excalibur||Excalibur||");
        m_cmdResult.append("||1||340||51||||Grave Digger||Rheingold||Maidens Of War||");
        m_cmdResult.append("||1||340||52||4:32||Grave Digger||Tunes Of War||The Dark Of The Sun||");
        m_cmdResult.append("||1||340||53||4:05||Grave Digger||Tunes Of War||Rebellion (The Clans Are Marching)||");
        m_cmdResult.append("||1||340||54||||Grave Digger||Witch Hunter||Witch Hunter||");
        m_cmdResult.append("||1||340||55||4:34||Graveworm||Collateral Defect||I Need A Hero||");
        m_cmdResult.append("||1||340||56||4:49||Hammerfall||Glory To The Brave||Hammerfall||");
        m_cmdResult.append("||1||340||57||3:44||Hammerfall||Glory To The Brave||Child Of The Damned||");
        m_cmdResult.append("||1||340||58||5:14||Hypocrisy||10 Years of Chaos and Confusion||Fractured Millennium||");
        m_cmdResult.append("||1||340||59||||Hypocrisy||Abducted||Killing Art||");
        m_cmdResult.append("||1||340||60||||Hypocrisy||The Arrival||War within||");
        m_cmdResult.append("||1||340||61||||Hypocrisy||Virus||Compulsive Psychosis||");
        m_cmdResult.append("||1||340||62||||Iced Earth||Burnt Offerings||Last December||");
        m_cmdResult.append("||1||340||63||3:43||Iced Earth||Something Wicked This Way Comes||Burning Times||");
        m_cmdResult.append("||1||340||64||||Iced Earth||The Dark Saga||The Hunter||");
        m_cmdResult.append("||1||340||65||4:42||In Flames||Clayman||Bullet Ride||");
        m_cmdResult.append("||1||340||66||||In Flames||Colony||Colony||");
        m_cmdResult.append("||1||340||67||||In Flames||Reroute to Remain||Cloud Connected||");
        m_cmdResult.append("||1||340||68||3:17||Iron Maiden||Iron Maiden||Running Free||");
        m_cmdResult.append("||1||340||69||5:00||Iron Maiden||Killers||Killers||");
        m_cmdResult.append("||1||340||70||6:36||Iron Maiden||The Number Of The Beast||22 Acacia Avenue||");
        m_cmdResult.append("||1||340||71||7:11||Iron Maiden||The Number Of The Beast||Hallowed Be Thy Name||");
        m_cmdResult.append("||1||340||72||||Judas Priest||British Steel||Breaking the Law||");
        m_cmdResult.append("||1||340||73||||Judas Priest||Defenders of the Faith||The Sentinel||");
        m_cmdResult.append("||1||340||74||||Judas Priest||Defenders of the Faith||Love Bites||");
        m_cmdResult.append("||1||340||75||||Judas Priest||Painkiller||Painkiller||");
        m_cmdResult.append("||1||340||76||||Korpiklaani||Spirit of the Forest||Wooden Pints||");
        m_cmdResult.append("||1||340||77||||Korpiklaani||Voice of Wilderness||Beer Beer||");
        m_cmdResult.append("||1||340||78||||Kreator||Enemy Of God||Enemy Of God||");
        m_cmdResult.append("||1||340||79||||Kreator||Hordes Of Chaos||hordes of chaos (a necrologue for the elite)||");
        m_cmdResult.append("||1||340||80||||Kreator||Hordes Of Chaos||warcurse||");
        m_cmdResult.append("||1||340||81||||Kreator||Phantom Antichrist||Civilisation Collapse||");
        m_cmdResult.append("||1||340||82||||Kreator||Phantom Antichrist||United In Hate||");
        m_cmdResult.append("||1||340||83||||Manowar||Hail To England||Each Dawn I Die||");
        m_cmdResult.append("||1||340||84||||Manowar||Hail To England||Kill with Power||");
        m_cmdResult.append("||1||340||85||||Manowar||Into Glory Ride||Gloves of Metal||");
        m_cmdResult.append("||1||340||86||||Manowar||Kings Of Metal||Hail And Kill||");
        m_cmdResult.append("||1||340||87||||Manowar||Kings Of Metal||Blood Of The Kings||");
        m_cmdResult.append("||1||340||88||||Manowar||Louder Than Hell||The Power||");
        m_cmdResult.append("||1||340||89||||Pantera||Cowboys From Hell||Cowboys From Hell||");
        m_cmdResult.append("||1||340||90||||Pantera||Vulgar Display of Power||Fucking Hostile||");
        m_cmdResult.append("||1||340||91||||Pantera||Vulgar Display of Power||This Love||");
        m_cmdResult.append("||1||340||92||||Powerwolf||Blood of the Saints||We Drink Your Blood||");
        m_cmdResult.append("||1||340||93||||Powerwolf||Blood of the Saints||Die, Die, Crucified||");
        m_cmdResult.append("||1||340||94||||Rammstein||Herzeleid||Wollt Ihr Das Bett In Flammen||");
        m_cmdResult.append("||1||340||95||||Rammstein||Herzleid||Rammstein||");
        m_cmdResult.append("||1||340||96||||Savatage||Dead Winter Dead||Doesn't Matter Anyway||");
        m_cmdResult.append("||1||340||97||||Savatage||Hall Of The Mountain King||Hall Of The Mountain King||");
        m_cmdResult.append("||1||340||98||||Slayer||Soundtrack To The Apocalypse||Angel Of Death||");
        m_cmdResult.append("||1||340||99||||Slayer||Soundtrack To The Apocalypse||Raining Blood||");
        m_cmdResult.append("||1||340||100||||Slayer||World Painted Blood||World Painted Blood||");
        m_cmdResult.append("||1||340||101||||Sodom||In War And Pieces||In War And Pieces||");
        m_cmdResult.append("||1||340||102||||Sodom||In War And Pieces||Hellfire||");
        m_cmdResult.append("||1||340||103||||Testament||First Strike Still Deadly||The Preacher||");
        m_cmdResult.append("||1||340||104||||Testament||First Strike Still Deadly||Alone In The Dark||");
        m_cmdResult.append("||1||340||105||||Turbonegro||Sexual Harassment||Dude Without a Face||");
    }

    m_statusMessage = "OK.";
    m_status = 0;
#endif

    // postprocess results
    m_cmdResultFields.clear();
    for ( int i = 0; i < m_cmdResult.size(); ++i )
    {
        m_cmdResultFields.append( m_cmdResult.at( i ).split("||") );
        qDebug() << m_cmdResultFields[i];
    }


    return m_status;
}



