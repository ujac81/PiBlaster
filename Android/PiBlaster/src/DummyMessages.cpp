

#include "RFCommMessageObject.h"

#include <QString>
#include <QList>



RFCommMessageObject* CreateDummyResponse( int id, const QString& cmd, const QList<QString>& inPayload )
{
    int status = 0;
    int code = -1;
    QList<QString> payload;
    QString msg = "Command not known by message dummy";


    if ( cmd == "1234" )
    {
        code = 1;
        msg = "Password OK";
    }
    else if ( cmd == "disconnect" )
    {
        status = 101;
        msg = "OK";
    }
    else if ( cmd == "showdevices" )
    {
        code = 101;
        msg = "OK";
        payload.append("||0||DACE-470F||DACE-470F||1||11||90||2.95 GB||759.81 MB||");
        payload.append("||1||AA17-F608||AA17-F608||1||344||1678||18.8 GB||10.13 GB||");
    }
    else if ( cmd == "lsfulldir 1 0" )
    {
        code = 102;
        msg = "OK";
        payload.append("||1||1||1||0||3||0||2013NOAF||2013NOAF||");
        payload.append("||1||1||118||0||19||0||Alben||Alben||");
        payload.append("||1||1||252||0||31||0||Extreme_Metal3||Extreme_Metal3||");
        payload.append("||1||1||339||0||0||0||Music||Music||");
        payload.append("||1||1||340||0||0||105||PartyMetal||PartyMetal||");
    }
    else if ( cmd == "lsfulldir 1 340" )
    {
        code = 102;
        msg = "OK";
        payload.append("||2||1||340||1||4:23||Amon Amarth||Twilight Of The Thunder God||Guardians Of Asgaard||");
        payload.append("||2||1||340||2||4:18||Amon Amarth||Twilight Of The Thunder God||Varyags Of Miklagaard||");
        payload.append("||2||1||340||3||||Amon Amarth||Versus The World||Death in Fire||");
        payload.append("||2||1||340||4||||Amon Amarth||With Oden On Our Side||Asator||");
        payload.append("||2||1||340||5||4:05||Amorphis||Elegy||Against Widows||");
        payload.append("||2||1||340||6||5:40||Anthrax||Return of the killer A's||Indians||");
        payload.append("||2||1||340||7||||Arch Enemy||Anthems Of Rebellion||We Will Rise||");
        payload.append("||2||1||340||8||||Arch Enemy||Anthems Of Rebellion||Dead Eyes See No Future||");
        payload.append("||2||1||340||9||||Arch Enemy||Doomsday Machine||My Apocalypse||");
        payload.append("||2||1||340||10||||At The Gates||Suicidal Final Art||Blinded By Fear||");
        payload.append("||2||1||340||11||||Black Sabbath||Black Sabbath||The Wizard||");
        payload.append("||2||1||340||12||2:52||Black Sabbath||Paranoid||Paranoid||");
        payload.append("||2||1||340||13||||Blind Guardian||Follow the blind||Valhalla||");
        payload.append("||2||1||340||14||||Blind Guardian||Imaginations from the other Side||Mordred's Song||");
        payload.append("||2||1||340||15||5:06||Blind Guardian||Nightfall In Middle-Earth||Mirror Mirror||");
        payload.append("||2||1||340||16||||Blind Guardian||Somewhere Far Beyond||Journey Through The Dark||");
        payload.append("||2||1||340||17||||Blind Guardian||Somewhere Far Beyond||Ashes To Ashes||");
        payload.append("||2||1||340||18||||Blind Guardian||Somewhere Far Beyond||Somewhere Far Beyond||");
        payload.append("||2||1||340||19||4:50||Blind Guardian||Tales from the Twilight World||Welcome To Dying||");
        payload.append("||2||1||340||20||||Bolt Thrower||Mercenary||No Guts, No Glory||");
        payload.append("||2||1||340||21||||Bolt Thrower||Those Once Loyal||At first Light||");
        payload.append("||2||1||340||22||||Bolt Thrower||Those Once Loyal||Entrenched||");
        payload.append("||2||1||340||23||||Bolt Thrower||Those Once Loyal||The Killchain||");
        payload.append("||2||1||340||24||||Children Of Bodom||Downfall||Downfall||");
        payload.append("||2||1||340||25||||Children Of Bodom||Follow The Reaper||Bodom After Midnight||");
        payload.append("||2||1||340||26||||Children Of Bodom||Follow The Reaper||Everytime I Die||");
        payload.append("||2||1||340||27||||Children Of Bodom||Skeletons In The Closet||Aces High||");
        payload.append("||2||1||340||28||||Children Of Bodom||Skeletons In The Closet||Rebel Yell||");
        payload.append("||2||1||340||29||||Dark Tranquillity||A Closer End||22 Acacia Avenue||");
        payload.append("||2||1||340||30||||Dark Tranquillity||Damage Done||Hours Passed in Exile||");
        payload.append("||2||1||340||31||||Dark Tranquillity||Damage Done||Cathode Ray Sunshine||");
        payload.append("||2||1||340||32||||Die Apokalyptischen Reiter||Riders on the Storm||Riders on the Storm||");
        payload.append("||2||1||340||33||||Ensiferum||Ensiferum||Guardians of Fate||");
        payload.append("||2||1||340||34||||Ensiferum||Iron||Iron||");
        payload.append("||2||1||340||35||||Ensiferum||Iron||Sword Chant||");
        payload.append("||2||1||340||36||||Equilibrium||Sagas||Blut im Auge||");
        payload.append("||2||1||340||37||||Equilibrium||Sagas||Unbesiegt||");
        payload.append("||2||1||340||38||||Equilibrium||Turis Fratyr||Wingthors Hammer||");
        payload.append("||2||1||340||39||4:41||Evil Hedgehog||Rising||Dressed in Black||");
        payload.append("||2||1||340||40||5:44||Evil Hedgehog||Rising||One Thousand Voices||");
        payload.append("||2||1||340||41||||Evocation||Tales from the Tomb||Feed the Fire||");
        payload.append("||2||1||340||42||2:32||Excrementory Grindfuckers||Bitte nicht vor den Gästen||Nein kein Grindcore||");
        payload.append("||2||1||340||43||1:44||Excrementory Grindfuckers||Bitte nicht vor den Gästen||Halb und Halb||");
        payload.append("||2||1||340||44||||Excrementory Grindfuckers||Excrementory Grindfuckers||Vater Morgana||");
        payload.append("||2||1||340||45||||Excrementory Grindfuckers||Headliner Der Herzen||Grindcore Vibes||");
        payload.append("||2||1||340||46||||Fear Factory||Demanufacture||Demanufacture||");
        payload.append("||2||1||340||47||||Fear Factory||Demanufacture||Replica||");
        payload.append("||2||1||340||48||||Grailknights||Return To Castle Grailskull||Moonlit Masquerade||");
        payload.append("||2||1||340||49||||Grailknights||Return To Castle Grailskull||Fight Until You Die||");
        payload.append("||2||1||340||50||4:45||Grave Digger||Excalibur||Excalibur||");
        payload.append("||2||1||340||51||||Grave Digger||Rheingold||Maidens Of War||");
        payload.append("||2||1||340||52||4:32||Grave Digger||Tunes Of War||The Dark Of The Sun||");
        payload.append("||2||1||340||53||4:05||Grave Digger||Tunes Of War||Rebellion (The Clans Are Marching)||");
        payload.append("||2||1||340||54||||Grave Digger||Witch Hunter||Witch Hunter||");
        payload.append("||2||1||340||55||4:34||Graveworm||Collateral Defect||I Need A Hero||");
        payload.append("||2||1||340||56||4:49||Hammerfall||Glory To The Brave||Hammerfall||");
        payload.append("||2||1||340||57||3:44||Hammerfall||Glory To The Brave||Child Of The Damned||");
        payload.append("||2||1||340||58||5:14||Hypocrisy||10 Years of Chaos and Confusion||Fractured Millennium||");
        payload.append("||2||1||340||59||||Hypocrisy||Abducted||Killing Art||");
        payload.append("||2||1||340||60||||Hypocrisy||The Arrival||War within||");
        payload.append("||2||1||340||61||||Hypocrisy||Virus||Compulsive Psychosis||");
        payload.append("||2||1||340||62||||Iced Earth||Burnt Offerings||Last December||");
        payload.append("||2||1||340||63||3:43||Iced Earth||Something Wicked This Way Comes||Burning Times||");
        payload.append("||2||1||340||64||||Iced Earth||The Dark Saga||The Hunter||");
        payload.append("||2||1||340||65||4:42||In Flames||Clayman||Bullet Ride||");
        payload.append("||2||1||340||66||||In Flames||Colony||Colony||");
        payload.append("||2||1||340||67||||In Flames||Reroute to Remain||Cloud Connected||");
        payload.append("||2||1||340||68||3:17||Iron Maiden||Iron Maiden||Running Free||");
        payload.append("||2||1||340||69||5:00||Iron Maiden||Killers||Killers||");
        payload.append("||2||1||340||70||6:36||Iron Maiden||The Number Of The Beast||22 Acacia Avenue||");
        payload.append("||2||1||340||71||7:11||Iron Maiden||The Number Of The Beast||Hallowed Be Thy Name||");
        payload.append("||2||1||340||72||||Judas Priest||British Steel||Breaking the Law||");
        payload.append("||2||1||340||73||||Judas Priest||Defenders of the Faith||The Sentinel||");
        payload.append("||2||1||340||74||||Judas Priest||Defenders of the Faith||Love Bites||");
        payload.append("||2||1||340||75||||Judas Priest||Painkiller||Painkiller||");
        payload.append("||2||1||340||76||||Korpiklaani||Spirit of the Forest||Wooden Pints||");
        payload.append("||2||1||340||77||||Korpiklaani||Voice of Wilderness||Beer Beer||");
        payload.append("||2||1||340||78||||Kreator||Enemy Of God||Enemy Of God||");
        payload.append("||2||1||340||79||||Kreator||Hordes Of Chaos||hordes of chaos (a necrologue for the elite)||");
        payload.append("||2||1||340||80||||Kreator||Hordes Of Chaos||warcurse||");
        payload.append("||2||1||340||81||||Kreator||Phantom Antichrist||Civilisation Collapse||");
        payload.append("||2||1||340||82||||Kreator||Phantom Antichrist||United In Hate||");
        payload.append("||2||1||340||83||||Manowar||Hail To England||Each Dawn I Die||");
        payload.append("||2||1||340||84||||Manowar||Hail To England||Kill with Power||");
        payload.append("||2||1||340||85||||Manowar||Into Glory Ride||Gloves of Metal||");
        payload.append("||2||1||340||86||||Manowar||Kings Of Metal||Hail And Kill||");
        payload.append("||2||1||340||87||||Manowar||Kings Of Metal||Blood Of The Kings||");
        payload.append("||2||1||340||88||||Manowar||Louder Than Hell||The Power||");
        payload.append("||2||1||340||89||||Pantera||Cowboys From Hell||Cowboys From Hell||");
        payload.append("||2||1||340||90||||Pantera||Vulgar Display of Power||Fucking Hostile||");
        payload.append("||2||1||340||91||||Pantera||Vulgar Display of Power||This Love||");
        payload.append("||2||1||340||92||||Powerwolf||Blood of the Saints||We Drink Your Blood||");
        payload.append("||2||1||340||93||||Powerwolf||Blood of the Saints||Die, Die, Crucified||");
        payload.append("||2||1||340||94||||Rammstein||Herzeleid||Wollt Ihr Das Bett In Flammen||");
        payload.append("||2||1||340||95||||Rammstein||Herzleid||Rammstein||");
        payload.append("||2||1||340||96||||Savatage||Dead Winter Dead||Doesn't Matter Anyway||");
        payload.append("||2||1||340||97||||Savatage||Hall Of The Mountain King||Hall Of The Mountain King||");
        payload.append("||2||1||340||98||||Slayer||Soundtrack To The Apocalypse||Angel Of Death||");
        payload.append("||2||1||340||99||||Slayer||Soundtrack To The Apocalypse||Raining Blood||");
        payload.append("||2||1||340||100||||Slayer||World Painted Blood||World Painted Blood||");
        payload.append("||2||1||340||101||||Sodom||In War And Pieces||In War And Pieces||");
        payload.append("||2||1||340||102||||Sodom||In War And Pieces||Hellfire||");
        payload.append("||2||1||340||103||||Testament||First Strike Still Deadly||The Preacher||");
        payload.append("||2||1||340||104||||Testament||First Strike Still Deadly||Alone In The Dark||");
        payload.append("||2||1||340||105||||Turbonegro||Sexual Harassment||Dude Without a Face||");
    }
    else if ( cmd == "plappendmultiple 0" || cmd == "plappendmultiple 1" )
    {
        msg = QString::number( inPayload.size() ) + " items added to playlist";
        code = 201;
    }
    else if ( cmd == "plshow 0 0 1000 0" )
    {
        code = 202;
        msg = "OK";
        payload.append("||0||0||Amon Amarth - Guardians Of Asgaard||");
        payload.append("||1||0||Amon Amarth - Varyags Of Miklagaard||");
        payload.append("||2||0||Amon Amarth - Death in Fire||");
        payload.append("||3||0||Amon Amarth - Asator||");
        payload.append("||4||0||Amorphis - Against Widows||");
        payload.append("||5||0||Anthrax - Indians||");
        payload.append("||6||0||Arch Enemy - We Will Rise||");
        payload.append("||7||0||Arch Enemy - Dead Eyes See No Future||");
        payload.append("||8||0||Arch Enemy - My Apocalypse||");
        payload.append("||9||0||At The Gates - Blinded By Fear||");
        payload.append("||10||0||Black Sabbath - The Wizard||");
        payload.append("||11||0||Black Sabbath - Paranoid||");
        payload.append("||12||0||Blind Guardian - Valhalla||");
        payload.append("||13||0||Blind Guardian - Mordred's Song||");
        payload.append("||14||0||Blind Guardian - Mirror Mirror||");
        payload.append("||15||0||Blind Guardian - Journey Through The Dark||");
        payload.append("||16||0||Blind Guardian - Ashes To Ashes||");
        payload.append("||17||0||Blind Guardian - Somewhere Far Beyond||");
        payload.append("||18||0||Blind Guardian - Welcome To Dying||");
        payload.append("||19||0||Bolt Thrower - No Guts, No Glory||");
        payload.append("||20||0||Bolt Thrower - At first Light||");
        payload.append("||21||0||Bolt Thrower - Entrenched||");
        payload.append("||22||0||Bolt Thrower - The Killchain||");
        payload.append("||23||0||Children Of Bodom - Downfall||");
        payload.append("||24||0||Children Of Bodom - Bodom After Midnight||");
        payload.append("||25||0||Children Of Bodom - Everytime I Die||");
        payload.append("||26||0||Children Of Bodom - Aces High||");
        payload.append("||27||0||Children Of Bodom - Rebel Yell||");
        payload.append("||28||0||Dark Tranquillity - 22 Acacia Avenue||");
        payload.append("||29||0||Dark Tranquillity - Hours Passed in Exile||");
        payload.append("||30||0||Dark Tranquillity - Cathode Ray Sunshine||");
        payload.append("||31||0||Die Apokalyptischen Reiter - Riders on the Storm||");
        payload.append("||32||0||Ensiferum - Guardians of Fate||");
        payload.append("||33||0||Ensiferum - Iron||");
        payload.append("||34||0||Ensiferum - Sword Chant||");
        payload.append("||35||0||Equilibrium - Blut im Auge||");
        payload.append("||36||0||Equilibrium - Unbesiegt||");
        payload.append("||37||0||Equilibrium - Wingthors Hammer||");
        payload.append("||38||0||Evil Hedgehog - Dressed in Black||");
        payload.append("||39||0||Evil Hedgehog - One Thousand Voices||");
        payload.append("||40||0||Evocation - Feed the Fire||");
        payload.append("||41||0||Excrementory Grindfuckers - Nein kein Grindcore||");
        payload.append("||42||0||Excrementory Grindfuckers - Halb und Halb||");
        payload.append("||43||0||Excrementory Grindfuckers - Vater Morgana||");
        payload.append("||44||0||Excrementory Grindfuckers - Grindcore Vibes||");
        payload.append("||45||0||Fear Factory - Demanufacture||");
        payload.append("||46||0||Fear Factory - Replica||");
        payload.append("||47||0||Grailknights - Moonlit Masquerade||");
        payload.append("||48||0||Grailknights - Fight Until You Die||");
        payload.append("||49||0||Grave Digger - Excalibur||");
        payload.append("||50||0||Grave Digger - Maidens Of War||");
        payload.append("||51||0||Grave Digger - The Dark Of The Sun||");
        payload.append("||52||0||Grave Digger - Rebellion (The Clans Are Marching)||");
        payload.append("||53||0||Grave Digger - Witch Hunter||");
        payload.append("||54||0||Graveworm - I Need A Hero||");
        payload.append("||55||0||Hammerfall - Hammerfall||");
        payload.append("||56||0||Hammerfall - Child Of The Damned||");
        payload.append("||57||0||Hypocrisy - Fractured Millennium||");
        payload.append("||58||0||Hypocrisy - Killing Art||");
        payload.append("||59||0||Hypocrisy - War within||");
        payload.append("||60||0||Hypocrisy - Compulsive Psychosis||");
        payload.append("||61||0||Iced Earth - Last December||");
        payload.append("||62||0||Iced Earth - Burning Times||");
        payload.append("||63||0||Iced Earth - The Hunter||");
        payload.append("||64||0||In Flames - Bullet Ride||");
        payload.append("||65||0||In Flames - Colony||");
        payload.append("||66||0||In Flames - Cloud Connected||");
        payload.append("||67||0||Iron Maiden - Running Free||");
        payload.append("||68||0||Iron Maiden - Killers||");
        payload.append("||69||0||Iron Maiden - 22 Acacia Avenue||");
        payload.append("||70||0||Iron Maiden - Hallowed Be Thy Name||");
        payload.append("||71||0||Judas Priest - Breaking the Law||");
        payload.append("||72||0||Judas Priest - The Sentinel||");
        payload.append("||73||0||Judas Priest - Love Bites||");
        payload.append("||74||0||Judas Priest - Painkiller||");
        payload.append("||75||0||Korpiklaani - Wooden Pints||");
        payload.append("||76||0||Korpiklaani - Beer Beer||");
        payload.append("||77||0||Kreator - Enemy Of God||");
        payload.append("||78||0||Kreator - hordes of chaos (a necrologue for the elite)||");
        payload.append("||79||0||Kreator - warcurse||");
        payload.append("||80||0||Kreator - Civilisation Collapse||");
        payload.append("||81||0||Kreator - United In Hate||");
        payload.append("||82||0||Manowar - Each Dawn I Die||");
        payload.append("||83||0||Manowar - Kill with Power||");
        payload.append("||84||0||Manowar - Gloves of Metal||");
        payload.append("||85||0||Manowar - Hail And Kill||");
        payload.append("||86||0||Manowar - Blood Of The Kings||");
        payload.append("||87||0||Manowar - The Power||");
        payload.append("||88||0||Pantera - Cowboys From Hell||");
        payload.append("||89||0||Pantera - Fucking Hostile||");
        payload.append("||90||0||Pantera - This Love||");
        payload.append("||91||0||Powerwolf - We Drink Your Blood||");
        payload.append("||92||0||Powerwolf - Die, Die, Crucified||");
        payload.append("||93||0||Rammstein - Wollt Ihr Das Bett In Flammen||");
        payload.append("||94||0||Rammstein - Rammstein||");
        payload.append("||95||0||Savatage - Doesn't Matter Anyway||");
        payload.append("||96||0||Savatage - Hall Of The Mountain King||");
        payload.append("||97||0||Slayer - Angel Of Death||");
        payload.append("||98||0||Slayer - Raining Blood||");
        payload.append("||99||0||Slayer - World Painted Blood||");
        payload.append("||100||0||Sodom - In War And Pieces||");
        payload.append("||101||0||Sodom - Hellfire||");
        payload.append("||102||0||Testament - The Preacher||");
        payload.append("||103||0||Testament - Alone In The Dark||");
        payload.append("||104||0||Turbonegro - Dude Without a Face||");
        payload.append("||105||0||Inactive Messiah - Inactive Messiah Intro||");
        payload.append("||106||0||Inactive Messiah - Sing||");
        payload.append("||107||0||Inactive Messiah - All Your Dreams||");
        payload.append("||108||0||Inactive Messiah - Be My Drug||");
        payload.append("||109||0||Inactive Messiah - Synthetic Snow||");
        payload.append("||110||0||Inactive Messiah - Beat It||");
        payload.append("||111||0||Inactive Messiah - Pain||");
        payload.append("||112||0||Inactive Messiah - Hear Me Tonight||");
        payload.append("||113||0||Inactive Messiah - Before The End||");
        payload.append("||114||0||Inactive Messiah - Lord Of Lies||");
        payload.append("||115||0||Inactive Messiah - Satyricus||");
        payload.append("||116||0||Inactive Messiah - Soulless||");
        payload.append("||117||0||Inactive Messiah - Chosen one||");
        payload.append("||118||0||Inactive Messiah - Failure||");
        payload.append("||119||0||Inactive Messiah - Theatrical world||");
        payload.append("||120||0||Inactive Messiah - Sinful nation||");
        payload.append("||121||0||Inactive Messiah - Showdown||");
        payload.append("||122||0||Inactive Messiah - Eat my flesh and drink my blood||");
        payload.append("||123||0||Inactive Messiah - Forged in flames||");
        payload.append("||124||0||Inactive Messiah - From birth to death||");
        payload.append("||125||0||Inactive Messiah - Like an endless lament||");
    }



    RFCommMessageObject* msgObj = new RFCommMessageObject( id, status, code, payload.size(), msg );
    for ( int i = 0; i < payload.size(); ++i )
        msgObj->addPayload( payload[i] );

    return msgObj;
}
