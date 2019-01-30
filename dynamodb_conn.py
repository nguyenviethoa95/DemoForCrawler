import boto3
import config
import json

session = boto3.Session(region_name=config.CURRENT_REGION,
                        aws_access_key_id=config.AWS_CONFIG['AWS_SERVER_PUBLIC_KEY'],
                        aws_secret_access_key=config.AWS_CONFIG['AWS_SERVER_SECRET_KEY'])
dynamodb = session.resource('dynamodb').Table('geo')
dict = {
        'ID':'1',
        'name':'baden-wuerttemberg',
        'landkreis': [
            {
                'name':'ALB-DONAU',
                'gemeind':['Allmendingen','Altheim','Altheim(Alb)','Amstetten','Asselfingen','Ballendorf','Balzheim','Beimerstetten','Berghülen','Bernstadt','Bärslingen','Breitingen','Dornstadt','Emeringen','Emerkingen','Griesingen','Grundsheim','HausenamBussen','Heroldstatt','Holzkirch','Hüttisheim','IllerkirchbergIllerrieden','Lauterach','Lonsee','Merklingen','Neenstetten','Nellingen','Nerenstetten','Oberdischingen','Obermarchtal','Oberstadion','Öllingen','Öpfingen','Rammingen','Rechtenstein','Rottenacker','Schnürpflingen','Setzingen','Staig','Untermarchtal','Unterstadion','Unterwachingen','Weidenstetten','Westerheim','Westerstetten'],
                'stadt':['Blaubeuren','Blaustein','Dietenheim','Ehingen(Donau)-Kreisstadt','Erbach','Laichingen','Langenau','Munderkingen','Schelklingen']
             },
            {
                'name':'BIBERACH',
                'stadt':['BadBuchau','BadSchussenried','BiberachanderRiß-Kreisstadt','Laupheim','Ochsenhausen','Riedlingen'],
                'gemeind': ['Achstetten','Alleshausen','Allmannsweiler','Altheim','Attenweiler','Berkheim','Betzenweiler','Burgrieden','DettingenanderIller','Dürmentingen','Dürnau','Eberhardzell','Erlenmoos','Erolzheim','Ertingen','Gutenzell-Hürbel','Hochdorf','Ingoldingen','Kanzach','KirchberganderIller','KirchdorfanderIller','Langenenslingen','Maselheim','Mietingen','Mittelbiberach','Moosburg','Oggelshausen','RotanderRot','Schemmerhofen','Schwendi','Seekirch','SteinhausenanderRottum','Tannheim','Tiefenbach','Ummendorf','Unlingen','Uttenweiler','Wain','Warthausen']
            }
        ]
    }
res = dynamodb.put_item(
    Item = dict
)

