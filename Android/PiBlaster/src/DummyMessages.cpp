

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
        payload.append("0068080011009AA17-F608009AA17-F6080011003344004167800718.8 GB00810.13 GB");
        payload.append("0065080010009DACE-470F009DACE-470F00120013002330073.38 GB009318.94 MB");
    }
    else if ( cmd == "lsfulldir 1 0" )
    {
        code = 102;
        msg = "OK";
        payload.append("004508001100110031180010002190010005Alben005Alben");
        payload.append("006308001100110032520010002310010014Extreme_Metal3014Extreme_Metal3");
        payload.append("00440800110011003339001000100010005Music005Music");
        payload.append("0056080011001100334000100010003105010PartyMetal010PartyMetal");
        payload.append("00460800110011003341001000130010006bilder006bilder");
    }
    else if ( cmd == "lsfulldir 1 340" )
    {
        code = 102;
        msg = "OK";
        payload.append("0094080012001100334000110044:23011Amon Amarth027Twilight Of The Thunder God020Guardians Of Asgaard");
        payload.append("0095080012001100334000120044:18011Amon Amarth027Twilight Of The Thunder God021Varyags Of Miklagaard");
        payload.append("007208001200110033400013000011Amon Amarth016Versus The World013Death in Fire");
        payload.append("007008001200110033400014000011Amon Amarth021With Oden On Our Side006Asator");
        payload.append("0063080012001100334000150044:05008Amorphis005Elegy014Against Widows");
        payload.append("0074080012001100334000160045:40007Anthrax024Return of the killer A's007Indians");
        payload.append("007408001200110033400017000010Arch Enemy020Anthems Of Rebellion012We Will Rise");
        payload.append("008508001200110033400018000010Arch Enemy020Anthems Of Rebellion023Dead Eyes See No Future");
        payload.append("007108001200110033400019000010Arch Enemy016Doomsday Machine013My Apocalypse");
        payload.append("0078080012001100334000210000012At The Gates018Suicidal Final Art015Blinded By Fear");
        payload.append("0069080012001100334000211000013Black Sabbath013Black Sabbath010The Wizard");
        payload.append("00660800120011003340002120042:52013Black Sabbath008Paranoid008Paranoid");
        payload.append("0071080012001100334000213000014Blind Guardian016Follow the blind008Valhalla");
        payload.append("0093080012001100334000214000014Blind Guardian032Imaginations from the other Side014Mordred's Song");
        payload.append("00890800120011003340002150045:06014Blind Guardian025Nightfall In Middle-Earth013Mirror Mirror");
        payload.append("0091080012001100334000216000014Blind Guardian020Somewhere Far Beyond024Journey Through The Dark");
        payload.append("0081080012001100334000217000014Blind Guardian020Somewhere Far Beyond014Ashes To Ashes");
        payload.append("0087080012001100334000218000014Blind Guardian020Somewhere Far Beyond020Somewhere Far Beyond");
        payload.append("00960800120011003340002190044:50014Blind Guardian029Tales from the Twilight World016Welcome To Dying");
        payload.append("0071080012001100334000220000012Bolt Thrower009Mercenary017No Guts, No Glory");
        payload.append("0075080012001100334000221000012Bolt Thrower016Those Once Loyal014At first Light");
        payload.append("0071080012001100334000222000012Bolt Thrower016Those Once Loyal010Entrenched");
        payload.append("0074080012001100334000223000012Bolt Thrower016Those Once Loyal013The Killchain");
        payload.append("0066080012001100334000224000017Children Of Bodom008Downfall008Downfall");
        payload.append("0087080012001100334000225000017Children Of Bodom017Follow The Reaper020Bodom After Midnight");
        payload.append("0082080012001100334000226000017Children Of Bodom017Follow The Reaper015Everytime I Die");
        payload.append("0082080012001100334000227000017Children Of Bodom023Skeletons In The Closet009Aces High");
        payload.append("0083080012001100334000228000017Children Of Bodom023Skeletons In The Closet010Rebel Yell");
        payload.append("0078080012001100334000229000017Dark Tranquillity012A Closer End01622 Acacia Avenue");
        payload.append("0082080012001100334000230000017Dark Tranquillity011Damage Done021Hours Passed in Exile");
        payload.append("0081080012001100334000231000017Dark Tranquillity011Damage Done020Cathode Ray Sunshine");
        payload.append("0097080012001100334000232000026Die Apokalyptischen Reiter019Riders on the Storm019Riders on the Storm");
        payload.append("0068080012001100334000233000009Ensiferum009Ensiferum017Guardians of Fate");
        payload.append("0050080012001100334000234000009Ensiferum004Iron004Iron");
        payload.append("0057080012001100334000235000009Ensiferum004Iron011Sword Chant");
        payload.append("0061080012001100334000236000011Equilibrium005Sagas012Blut im Auge");
        payload.append("0058080012001100334000237000011Equilibrium005Sagas009Unbesiegt");
        payload.append("0072080012001100334000238000011Equilibrium012Turis Fratyr016Wingthors Hammer");
        payload.append("00720800120011003340002390044:41013Evil Hedgehog006Rising016Dressed in Black");
        payload.append("00750800120011003340002400045:44013Evil Hedgehog006Rising019One Thousand Voices");
        payload.append("0074080012001100334000241000009Evocation019Tales from the Tomb013Feed the Fire");
        payload.append("01070800120011003340002420042:32025Excrementory Grindfuckers026Bitte nicht vor den Gästen019Nein kein Grindcore");
        payload.append("01010800120011003340002430041:44025Excrementory Grindfuckers026Bitte nicht vor den Gästen013Halb und Halb");
        payload.append("0096080012001100334000244000025Excrementory Grindfuckers025Excrementory Grindfuckers013Vater Morgana");
        payload.append("0093080012001100334000245000025Excrementory Grindfuckers020Headliner Der Herzen015Grindcore Vibes");
        payload.append("0071080012001100334000246000012Fear Factory013Demanufacture013Demanufacture");
        payload.append("0065080012001100334000247000012Fear Factory013Demanufacture007Replica");
        payload.append("0090080012001100334000248000012Grailknights027Return To Castle Grailskull018Moonlit Masquerade");
        payload.append("0091080012001100334000249000012Grailknights027Return To Castle Grailskull019Fight Until You Die");
        payload.append("00670800120011003340002500044:45012Grave Digger009Excalibur009Excalibur");
        payload.append("0068080012001100334000251000012Grave Digger009Rheingold014Maidens Of War");
        payload.append("00800800120011003340002520044:32012Grave Digger012Tunes Of War019The Dark Of The Sun");
        payload.append("00950800120011003340002530044:05012Grave Digger012Tunes Of War034Rebellion (The Clans Are Marching)");
        payload.append("0069080012001100334000254000012Grave Digger012Witch Hunter012Witch Hunter");
        payload.append("00760800120011003340002550044:34009Graveworm017Collateral Defect013I Need A Hero");
        payload.append("00750800120011003340002560044:49010Hammerfall018Glory To The Brave010Hammerfall");
        payload.append("00840800120011003340002570043:44010Hammerfall018Glory To The Brave019Child Of The Damned");
        payload.append("00970800120011003340002580045:14009Hypocrisy03110 Years of Chaos and Confusion020Fractured Millennium");
        payload.append("0061080012001100334000259000009Hypocrisy008Abducted011Killing Art");
        payload.append("0063080012001100334000260000009Hypocrisy011The Arrival010War within");
        payload.append("0067080012001100334000261000009Hypocrisy005Virus020Compulsive Psychosis");
        payload.append("0071080012001100334000262000010Iced Earth015Burnt Offerings013Last December");
        payload.append("00910800120011003340002630043:43010Iced Earth031Something Wicked This Way Comes013Burning Times");
        payload.append("0066080012001100334000264000010Iced Earth013The Dark Saga010The Hunter");
        payload.append("00640800120011003340002650044:42009In Flames007Clayman011Bullet Ride");
        payload.append("0054080012001100334000266000009In Flames006Colony006Colony");
        payload.append("0074080012001100334000267000009In Flames017Reroute to Remain015Cloud Connected");
        payload.append("00710800120011003340002680043:17011Iron Maiden011Iron Maiden012Running Free");
        payload.append("00620800120011003340002690045:00011Iron Maiden007Killers007Killers");
        payload.append("00870800120011003340002700046:36011Iron Maiden023The Number Of The Beast01622 Acacia Avenue");
        payload.append("00910800120011003340002710047:11011Iron Maiden023The Number Of The Beast020Hallowed Be Thy Name");
        payload.append("0074080012001100334000272000012Judas Priest013British Steel016Breaking the Law");
        payload.append("0079080012001100334000273000012Judas Priest022Defenders of the Faith012The Sentinel");
        payload.append("0077080012001100334000274000012Judas Priest022Defenders of the Faith010Love Bites");
        payload.append("0065080012001100334000275000012Judas Priest010Painkiller010Painkiller");
        payload.append("0076080012001100334000276000011Korpiklaani020Spirit of the Forest012Wooden Pints");
        payload.append("0072080012001100334000277000011Korpiklaani019Voice of Wilderness009Beer Beer");
        payload.append("0064080012001100334000278000007Kreator012Enemy Of God012Enemy Of God");
        payload.append("0099080012001100334000279000007Kreator015Hordes Of Chaos044hordes of chaos (a necrologue for the elite)");
        payload.append("0063080012001100334000280000007Kreator015Hordes Of Chaos008warcurse");
        payload.append("0079080012001100334000281000007Kreator018Phantom Antichrist021Civilisation Collapse");
        payload.append("0072080012001100334000282000007Kreator018Phantom Antichrist014United In Hate");
        payload.append("0070080012001100334000283000007Manowar015Hail To England015Each Dawn I Die");
        payload.append("0070080012001100334000284000007Manowar015Hail To England015Kill with Power");
        payload.append("0070080012001100334000285000007Manowar015Into Glory Ride015Gloves of Metal");
        payload.append("0067080012001100334000286000007Manowar014Kings Of Metal013Hail And Kill");
        payload.append("0072080012001100334000287000007Manowar014Kings Of Metal018Blood Of The Kings");
        payload.append("0065080012001100334000288000007Manowar016Louder Than Hell009The Power");
        payload.append("0074080012001100334000289000007Pantera017Cowboys From Hell017Cowboys From Hell");
        payload.append("0078080012001100334000290000007Pantera023Vulgar Display of Power015Fucking Hostile");
        payload.append("0072080012001100334000291000007Pantera023Vulgar Display of Power009This Love");
        payload.append("0080080012001100334000292000009Powerwolf019Blood of the Saints019We Drink Your Blood");
        payload.append("0080080012001100334000293000009Powerwolf019Blood of the Saints019Die, Die, Crucified");
        payload.append("0080080012001100334000294000009Rammstein009Herzeleid029Wollt Ihr Das Bett In Flammen");
        payload.append("0059080012001100334000295000009Rammstein008Herzleid009Rammstein");
        payload.append("0078080012001100334000296000008Savatage016Dead Winter Dead021Doesn't Matter Anyway");
        payload.append("0091080012001100334000297000008Savatage025Hall Of The Mountain King025Hall Of The Mountain King");
        payload.append("0081080012001100334000298000006Slayer028Soundtrack To The Apocalypse014Angel Of Death");
        payload.append("0080080012001100334000299000006Slayer028Soundtrack To The Apocalypse013Raining Blood");
        payload.append("00780800120011003340003100000006Slayer019World Painted Blood019World Painted Blood");
        payload.append("00730800120011003340003101000005Sodom017In War And Pieces017In War And Pieces");
        payload.append("00640800120011003340003102000005Sodom017In War And Pieces008Hellfire");
        payload.append("00800800120011003340003103000009Testament025First Strike Still Deadly012The Preacher");
        payload.append("00850800120011003340003104000009Testament025First Strike Still Deadly017Alone In The Dark");
        payload.append("00800800120011003340003105000010Turbonegro017Sexual Harassment019Dude Without a Face");
    }
    else if ( cmd == "plappendmultiple 0" || cmd == "plappendmultiple 1" )
    {
        msg = QString::number( inPayload.size() ) + " items added to playlist";
        code = 201;
    }
    else if ( cmd == "plshow 0 0 100 0" )
    {
        code = 202;
        msg = "OK";
        payload.append("00360300100010023Sepultura - Ratamahatta");
        payload.append("00350300110010022Kvelertak - Apenbaring");
        payload.append("00410300120010028Kvelertak - Spring Fra Livet");
        payload.append("00310300130010018Kvelertak - Trepan");
        payload.append("00370300140010024Kvelertak - Evig Vandrar");
        payload.append("00340300150010021Kvelertak - Snilepisk");
        payload.append("00360300160010023Kvelertak - Nekrokosmos");
        payload.append("00470300170010034Amon Amarth - Guardians Of Asgaard");
        payload.append("00480300180010035Amon Amarth - Varyags Of Miklagaard");
        payload.append("00400300190010027Amon Amarth - Death in Fire");
        payload.append("003403002100010020Amon Amarth - Asator");
        payload.append("003903002110012025Amorphis - Against Widows");
        payload.append("003103002120010017Anthrax - Indians");
        payload.append("003903002130010025Arch Enemy - We Will Rise");
        payload.append("005003002140010036Arch Enemy - Dead Eyes See No Future");
        payload.append("004003002150010026Arch Enemy - My Apocalypse");
        payload.append("004403002160010030At The Gates - Blinded By Fear");
        payload.append("004003002170010026Black Sabbath - The Wizard");
        payload.append("003803002180010024Black Sabbath - Paranoid");
        payload.append("003903002190010025Blind Guardian - Valhalla");
        payload.append("004503002200010031Blind Guardian - Mordred's Song");
        payload.append("004403002210010030Blind Guardian - Mirror Mirror");
        payload.append("005503002220010041Blind Guardian - Journey Through The Dark");
        payload.append("004503002230010031Blind Guardian - Ashes To Ashes");
        payload.append("005103002240010037Blind Guardian - Somewhere Far Beyond");
        payload.append("004703002250010033Blind Guardian - Welcome To Dying");
        payload.append("004603002260010032Bolt Thrower - No Guts, No Glory");
        payload.append("004303002270010029Bolt Thrower - At first Light");
        payload.append("003903002280010025Bolt Thrower - Entrenched");
        payload.append("004203002290010028Bolt Thrower - The Killchain");
        payload.append("004203002300010028Children Of Bodom - Downfall");
        payload.append("005403002310010040Children Of Bodom - Bodom After Midnight");
        payload.append("004903002320010035Children Of Bodom - Everytime I Die");
        payload.append("004303002330010029Children Of Bodom - Aces High");
        payload.append("004403002340010030Children Of Bodom - Rebel Yell");
        payload.append("005003002350010036Dark Tranquillity - 22 Acacia Avenue");
        payload.append("005503002360010041Dark Tranquillity - Hours Passed in Exile");
        payload.append("005403002370010040Dark Tranquillity - Cathode Ray Sunshine");
        payload.append("006203002380010048Die Apokalyptischen Reiter - Riders on the Storm");
        payload.append("004303002390010029Ensiferum - Guardians of Fate");
        payload.append("003003002400010016Ensiferum - Iron");
        payload.append("003703002410010023Ensiferum - Sword Chant");
        payload.append("004003002420010026Equilibrium - Blut im Auge");
        payload.append("003703002430010023Equilibrium - Unbesiegt");
        payload.append("004403002440010030Equilibrium - Wingthors Hammer");
        payload.append("004603002450010032Evil Hedgehog - Dressed in Black");
        payload.append("004903002460010035Evil Hedgehog - One Thousand Voices");
        payload.append("003903002470010025Evocation - Feed the Fire");
        payload.append("006103002480010047Excrementory Grindfuckers - Nein kein Grindcore");
        payload.append("005503002490010041Excrementory Grindfuckers - Halb und Halb");
        payload.append("005503002500010041Excrementory Grindfuckers - Vater Morgana");
        payload.append("005703002510010043Excrementory Grindfuckers - Grindcore Vibes");
        payload.append("004203002520010028Fear Factory - Demanufacture");
        payload.append("003603002530010022Fear Factory - Replica");
        payload.append("004703002540010033Grailknights - Moonlit Masquerade");
        payload.append("004803002550010034Grailknights - Fight Until You Die");
        payload.append("003803002560010024Grave Digger - Excalibur");
        payload.append("004303002570010029Grave Digger - Maidens Of War");
        payload.append("004803002580010034Grave Digger - The Dark Of The Sun");
        payload.append("006303002590010049Grave Digger - Rebellion (The Clans Are Marching)");
        payload.append("004103002600010027Grave Digger - Witch Hunter");
        payload.append("003903002610010025Graveworm - I Need A Hero");
        payload.append("003703002620010023Hammerfall - Hammerfall");
        payload.append("004603002630010032Hammerfall - Child Of The Damned");
        payload.append("004603002640010032Hypocrisy - Fractured Millennium");
        payload.append("003703002650010023Hypocrisy - Killing Art");
        payload.append("003603002660010022Hypocrisy - War within");
        payload.append("004603002670010032Hypocrisy - Compulsive Psychosis");
        payload.append("004003002680010026Iced Earth - Last December");
        payload.append("004003002690010026Iced Earth - Burning Times");
        payload.append("003703002700010023Iced Earth - The Hunter");
        payload.append("003703002710010023In Flames - Bullet Ride");
        payload.append("003203002720010018In Flames - Colony");
        payload.append("004103002730010027In Flames - Cloud Connected");
        payload.append("004003002740010026Iron Maiden - Running Free");
        payload.append("003503002750010021Iron Maiden - Killers");
        payload.append("004403002760010030Iron Maiden - 22 Acacia Avenue");
        payload.append("004803002770010034Iron Maiden - Hallowed Be Thy Name");
        payload.append("004503002780010031Judas Priest - Breaking the Law");
        payload.append("004103002790010027Judas Priest - The Sentinel");
        payload.append("003903002800010025Judas Priest - Love Bites");
        payload.append("003903002810010025Judas Priest - Painkiller");
        payload.append("004003002820010026Korpiklaani - Wooden Pints");
        payload.append("003703002830010023Korpiklaani - Beer Beer");
        payload.append("003603002840010022Kreator - Enemy Of God");
        payload.append("006803002850010054Kreator - hordes of chaos (a necrologue for the elite)");
        payload.append("003203002860010018Kreator - warcurse");
        payload.append("004503002870010031Kreator - Civilisation Collapse");
        payload.append("003803002880010024Kreator - United In Hate");
        payload.append("003903002890010025Manowar - Each Dawn I Die");
        payload.append("003903002900010025Manowar - Kill with Power");
        payload.append("003903002910010025Manowar - Gloves of Metal");
        payload.append("003703002920010023Manowar - Hail And Kill");
        payload.append("004203002930010028Manowar - Blood Of The Kings");
        payload.append("003303002940010019Manowar - The Power");
        payload.append("004103002950010027Pantera - Cowboys From Hell");
        payload.append("003903002960010025Pantera - Fucking Hostile");
        payload.append("003303002970010019Pantera - This Love");
        payload.append("004503002980010031Powerwolf - We Drink Your Blood");
        payload.append("004503002990010031Powerwolf - Die, Die, Crucified");
    }
    else if ( cmd == "playstatus" )
    {
        status = 0;
        code = 304;
        msg = "OK";
        payload.append("01211100110061331900010002260033400011015Everytime I Die017Follow The Reaper017Children Of Bodom019Melodic Death Metal0042000");
    }



    RFCommMessageObject* msgObj = new RFCommMessageObject( id, status, code, payload.size(), msg );
    for ( int i = 0; i < payload.size(); ++i )
        msgObj->addPayload( payload[i].right(payload[i].length()-4) );

    return msgObj;
}
