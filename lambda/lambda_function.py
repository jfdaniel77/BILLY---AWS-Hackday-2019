import json
import boto3

from urllib.parse import urlencode
from urllib.request import Request, urlopen

def lambda_handler(event, context):
    
    client = boto3.client('rekognition')
    
    payload = {}
    
    sagemakerPayload = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0]#,0,0]
    
    for record in event['Records']:
        bucketName = record['s3']['bucket']['name']
        objectName = record['s3']['object']['key']
    
        response = client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucketName,
                    'Name': objectName,
                }
            },
            MaxLabels= 123,
            MinConfidence= 65
        )
    
        print('Response = ' + json.dumps(response))
        
        payload["requestID"] = objectName[7:]
        #payload["data"] = response
        
        # Get result from sagemaker
        for labels in response["Labels"]:
            labelName = labels["Name"]
            responseValue = labels["Confidence"]
  
            if (labelName == "Wine"):
            	sagemakerPayload[0] = responseValue	
            elif (labelName == "Water"):
            	sagemakerPayload[1] = responseValue	
            elif (labelName == "Saucer"):
            	sagemakerPayload[2] = responseValue	
            elif (labelName == "Produce"):
            	sagemakerPayload[3] = responseValue	
            elif (labelName == "Light Fixture"):
            	sagemakerPayload[4] = responseValue	
            elif (labelName == "Jewelry"):
            	sagemakerPayload[5] = responseValue	
            elif (labelName == "Weapon"):
            	sagemakerPayload[6] = responseValue
            elif (labelName == "Powder"):
            	sagemakerPayload[7] = responseValue
            elif (labelName == "File Binder"):
            	sagemakerPayload[8] = responseValue
            elif (labelName == "Sphere"):
            	sagemakerPayload[9] = responseValue
            elif (labelName == "Helmet"):
            	sagemakerPayload[10] = responseValue
            elif (labelName == "Curtain"):
            	sagemakerPayload[11] = responseValue
            elif (labelName == "Flooring"):
            	sagemakerPayload[12] = responseValue
            elif (labelName == "Pool"):
            	sagemakerPayload[13] = responseValue	
            elif (labelName == "Bowl"):
            	sagemakerPayload[14] = responseValue
            elif (labelName == "Milk"):
            	sagemakerPayload[15] = responseValue
            elif (labelName == "Arrow"):
            	sagemakerPayload[16] = responseValue	
            elif (labelName == "Mineral Water"):
            	sagemakerPayload[17] = responseValue
            elif (labelName == "Motor"):
            	sagemakerPayload[18] = responseValue
            elif (labelName == "Paper Towel"):
            	sagemakerPayload[19] = responseValue
            elif (labelName == "Sea Life"):
            	sagemakerPayload[20] = responseValue
            elif (labelName == "Sea"):
            	sagemakerPayload[21] = responseValue
            elif (labelName == "Tent"):
            	sagemakerPayload[22] = responseValue
            elif (labelName == "Origami"):
            	sagemakerPayload[23] = responseValue
            elif (labelName == "Newspaper"):
            	sagemakerPayload[24] = responseValue
            elif (labelName == "Game"):
            	sagemakerPayload[25] = responseValue
            elif (labelName == "Building"):
            	sagemakerPayload[26] = responseValue
            elif (labelName == "Bandana"):
            	sagemakerPayload[27] = responseValue
            elif (labelName == "Gemstone"):
            	sagemakerPayload[28] = responseValue
            elif (labelName == "Badge"):
            	sagemakerPayload[29] = responseValue
            elif (labelName == "Flyer"):
            	sagemakerPayload[30] = responseValue
            elif (labelName == "Machine"):
            	sagemakerPayload[31] = responseValue
            elif (labelName == "Beer"):
            	sagemakerPayload[32] = responseValue
            elif (labelName == "Tissue"):
            	sagemakerPayload[33] = responseValue
            elif (labelName == "Digital Watch"):
            	sagemakerPayload[34] = responseValue
            elif (labelName == "Passport"):
            	sagemakerPayload[35] = responseValue
            elif (labelName == "Mailbox"):
            	sagemakerPayload[36] = responseValue
            elif (labelName == "Herbal"):
            	sagemakerPayload[37] = responseValue
            elif (labelName == "Ocean"):
            	sagemakerPayload[38] = responseValue
            elif (labelName == "Icing"):
            	sagemakerPayload[39] = responseValue
            elif (labelName == "Jug"):
            	sagemakerPayload[40] = responseValue
            elif (labelName == "Food"):
            	sagemakerPayload[41] = responseValue
            elif (labelName == "Speaker"):
            	sagemakerPayload[42] = responseValue
            elif (labelName == "Mineral"):
            	sagemakerPayload[43] = responseValue
            elif (labelName == "Toothpaste"):
            	sagemakerPayload[44] = responseValue
            elif (labelName == "Handwriting"):
            	sagemakerPayload[45] = responseValue
            elif (labelName == "Bee"):
            	sagemakerPayload[46] = responseValue
            elif (labelName == "Wristwatch"):
            	sagemakerPayload[47] = responseValue
            elif (labelName == "Pop Bottle"):
            	sagemakerPayload[48] = responseValue
            elif (labelName == "Couch"):
            	sagemakerPayload[49] = responseValue		
            elif (labelName == "Electronic Chip"):
            	sagemakerPayload[50] = responseValue
            elif (labelName == "Sake"):
            	sagemakerPayload[51] = responseValue	
            elif (labelName == "Tie"):
            	sagemakerPayload[52] = responseValue	
            elif (labelName == "File Folder"):
            	sagemakerPayload[53] = responseValue	
            elif (labelName == "Home Decor"):
            	sagemakerPayload[54] = responseValue	
            elif (labelName == "Driving License"):
            	sagemakerPayload[55] = responseValue	
            elif (labelName == "Tin"):
            	sagemakerPayload[56] = responseValue
            elif (labelName == "Nickel"):
            	sagemakerPayload[57] = responseValue
            elif (labelName == "Sand"):
            	sagemakerPayload[58] = responseValue
            elif (labelName == "Tattoo"):
            	sagemakerPayload[59] = responseValue
            elif (labelName == "Dryer"):
            	sagemakerPayload[60] = responseValue
            elif (labelName == "Vehicle"):
            	sagemakerPayload[61] = responseValue
            elif (labelName == "Winter"):
            	sagemakerPayload[62] = responseValue
            elif (labelName == "Light"):
            	sagemakerPayload[63] = responseValue	
            elif (labelName == "Tabletop"):
            	sagemakerPayload[64] = responseValue
            elif (labelName == "Gold"):
            	sagemakerPayload[65] = responseValue
            elif (labelName == "Ketchup"):
            	sagemakerPayload[66] = responseValue	
            elif (labelName == "Flour"):
            	sagemakerPayload[67] = responseValue
            elif (labelName == "Hand"):
            	sagemakerPayload[68] = responseValue
            elif (labelName == "Silver"):
            	sagemakerPayload[69] = responseValue
            elif (labelName == "Vegetation"):
            	sagemakerPayload[70] = responseValue
            elif (labelName == "Soil"):
            	sagemakerPayload[71] = responseValue
            elif (labelName == "Hornet"):
            	sagemakerPayload[72] = responseValue
            elif (labelName == "Alphabet"):
            	sagemakerPayload[73] = responseValue
            elif (labelName == "Locket"):
            	sagemakerPayload[74] = responseValue
            elif (labelName == "Fork"):
            	sagemakerPayload[75] = responseValue
            elif (labelName == "Vacuum Cleaner"):
            	sagemakerPayload[76] = responseValue
            elif (labelName == "Relish"):
            	sagemakerPayload[77] = responseValue
            elif (labelName == "First Aid"):
            	sagemakerPayload[78] = responseValue
            elif (labelName == "Brush"):
            	sagemakerPayload[79] = responseValue
            elif (labelName == "Gauge"):
            	sagemakerPayload[80] = responseValue
            elif (labelName == "Money"):
            	sagemakerPayload[81] = responseValue
            elif (labelName == "Urban"):
            	sagemakerPayload[82] = responseValue
            elif (labelName == "Banister"):
            	sagemakerPayload[83] = responseValue
            elif (labelName == "Emblem"):
            	sagemakerPayload[84] = responseValue
            elif (labelName == "Cosmetics"):
            	sagemakerPayload[85] = responseValue
            elif (labelName == "Hardware"):
            	sagemakerPayload[86] = responseValue
            elif (labelName == "Room"):
            	sagemakerPayload[87] = responseValue
            elif (labelName == "Cutlery"):
            	sagemakerPayload[88] = responseValue
            elif (labelName == "People"):
            	sagemakerPayload[89] = responseValue
            elif (labelName == "Shampoo"):
            	sagemakerPayload[90] = responseValue
            elif (labelName == "Portrait"):
            	sagemakerPayload[91] = responseValue
            elif (labelName == "Whisky"):
            	sagemakerPayload[92] = responseValue
            elif (labelName == "Diamond"):
            	sagemakerPayload[93] = responseValue
            elif (labelName == "Spiral"):
            	sagemakerPayload[94] = responseValue
            elif (labelName == "Cuff"):
            	sagemakerPayload[95] = responseValue
            elif (labelName == "Goblet"):
            	sagemakerPayload[96] = responseValue
            elif (labelName == "Wristwatch"):
            	sagemakerPayload[97] = responseValue
            elif (labelName == "Screw"):
            	sagemakerPayload[98] = responseValue
            elif (labelName == "Mouse"):
            	sagemakerPayload[99] = responseValue		
            elif (labelName == "Purple"):
            	sagemakerPayload[100] = responseValue
            elif (labelName == "Magazine"):
                    sagemakerPayload[101] = responseValue
            elif (labelName == "White Board"):
                    sagemakerPayload[102] = responseValue
            elif (labelName == "Leisure Activities"):
                    sagemakerPayload[103] = responseValue
            elif (labelName == "Limestone"):
                    sagemakerPayload[104] = responseValue
            elif (labelName == "License"):
                    sagemakerPayload[105] = responseValue
            elif (labelName == "Plywood"):
                    sagemakerPayload[106] = responseValue
            elif (labelName == "Gum"):
                    sagemakerPayload[107] = responseValue
            elif (labelName == "Human"):
                    sagemakerPayload[108] = responseValue
            elif (labelName == "Plot"):
                    sagemakerPayload[109] = responseValue
            elif (labelName == "Router"):
                    sagemakerPayload[110] = responseValue
            elif (labelName == "Suede"):
                    sagemakerPayload[111] = responseValue
            elif (labelName == "Hard Disk"):
                    sagemakerPayload[112] = responseValue
            elif (labelName == "Sunglasses"):
                    sagemakerPayload[113] = responseValue
            elif (labelName == "Baseball"):
                    sagemakerPayload[114] = responseValue
            elif (labelName == "Belt"):
                    sagemakerPayload[115] = responseValue
            elif (labelName == "Person"):
                    sagemakerPayload[116] = responseValue
            elif (labelName == "Jacuzzi"):
                    sagemakerPayload[117] = responseValue
            elif (labelName == "Toy"):
                    sagemakerPayload[118] = responseValue
            elif (labelName == "Mat"):
                    sagemakerPayload[119] = responseValue
            elif (labelName == "Chair"):
                    sagemakerPayload[120] = responseValue
            elif (labelName == "Cardboard"):
                    sagemakerPayload[121] = responseValue
            elif (labelName == "Audio Speaker"):
                    sagemakerPayload[122] = responseValue
            elif (labelName == "Power Drill"):
                    sagemakerPayload[123] = responseValue
            elif (labelName == "Slope"):
                    sagemakerPayload[124] = responseValue
            elif (labelName == "Mixing Bowl"):
                    sagemakerPayload[125] = responseValue
            elif (labelName == "Mousepad"):
                    sagemakerPayload[126] = responseValue
            elif (labelName == "Peel"):
                    sagemakerPayload[127] = responseValue
            elif (labelName == "Menu"):
                    sagemakerPayload[128] = responseValue
            elif (labelName == "Tape"):
                    sagemakerPayload[129] = responseValue
            elif (labelName == "Banner"):
                    sagemakerPayload[130] = responseValue
            elif (labelName == "Text"):
                    sagemakerPayload[131] = responseValue
            elif (labelName == "Headband"):
                    sagemakerPayload[132] = responseValue
            elif (labelName == "Wine Bottle"):
                    sagemakerPayload[133] = responseValue
            elif (labelName == "Cooler"):
                    sagemakerPayload[134] = responseValue
            elif (labelName == "Bathtub"):
                    sagemakerPayload[135] = responseValue
            elif (labelName == "Pill"):
                    sagemakerPayload[136] = responseValue
            elif (labelName == "Snow"):
                    sagemakerPayload[137] = responseValue
            elif (labelName == "Electronics"):
                    sagemakerPayload[138] = responseValue
            elif (labelName == "Liquor"):
                    sagemakerPayload[139] = responseValue
            elif (labelName == "Cpu"):
                    sagemakerPayload[140] = responseValue
            elif (labelName == "Adapter"):
                    sagemakerPayload[141] = responseValue
            elif (labelName == "Smoke"):
                    sagemakerPayload[142] = responseValue
            elif (labelName == "Paint Container"):
                    sagemakerPayload[143] = responseValue
            elif (labelName == "Porcelain"):
                    sagemakerPayload[144] = responseValue
            elif (labelName == "Bandage"):
                    sagemakerPayload[145] = responseValue
            elif (labelName == "Strawberry"):
                    sagemakerPayload[146] = responseValue
            elif (labelName == "Surface Computer"):
                    sagemakerPayload[147] = responseValue
            elif (labelName == "Dish"):
                    sagemakerPayload[148] = responseValue
            elif (labelName == "Handbag"):
                    sagemakerPayload[149] = responseValue
            elif (labelName == "Sprout"):
                    sagemakerPayload[150] = responseValue
            elif (labelName == "Disk"):
                    sagemakerPayload[151] = responseValue
            elif (labelName == "Tool"):
                    sagemakerPayload[152] = responseValue
            elif (labelName == "Screwdriver"):
                    sagemakerPayload[153] = responseValue
            elif (labelName == "Spotlight"):
                    sagemakerPayload[154] = responseValue
            elif (labelName == "Solar Panels"):
                    sagemakerPayload[155] = responseValue
            elif (labelName == "Box"):
                    sagemakerPayload[156] = responseValue
            elif (labelName == "City"):
                    sagemakerPayload[157] = responseValue
            elif (labelName == "Blow Dryer"):
                    sagemakerPayload[158] = responseValue
            elif (labelName == "Skin"):
                    sagemakerPayload[159] = responseValue
            elif (labelName == "Coffee Cup"):
                    sagemakerPayload[160] = responseValue
            elif (labelName == "Collage"):
                    sagemakerPayload[161] = responseValue
            elif (labelName == "Slate"):
                    sagemakerPayload[162] = responseValue
            elif (labelName == "Wall"):
                    sagemakerPayload[163] = responseValue
            elif (labelName == "Plastic Bag"):
                    sagemakerPayload[164] = responseValue
            elif (labelName == "Weaponry"):
                    sagemakerPayload[165] = responseValue
            elif (labelName == "Lager"):
                    sagemakerPayload[166] = responseValue
            elif (labelName == "Tablet Computer"):
                    sagemakerPayload[167] = responseValue
            elif (labelName == "Shaker"):
                    sagemakerPayload[168] = responseValue
            elif (labelName == "Symbol"):
                    sagemakerPayload[169] = responseValue
            elif (labelName == "LCD Screen"):
                    sagemakerPayload[170] = responseValue
            elif (labelName == "Coca"):
                    sagemakerPayload[171] = responseValue
            elif (labelName == "Accessories"):
                    sagemakerPayload[172] = responseValue
            elif (labelName == "Monitor"):
                    sagemakerPayload[173] = responseValue
            elif (labelName == "Harmonica"):
                    sagemakerPayload[174] = responseValue
            elif (labelName == "Lighting"):
                    sagemakerPayload[175] = responseValue
            elif (labelName == "Lamp"):
                    sagemakerPayload[176] = responseValue
            elif (labelName == "Tub"):
                    sagemakerPayload[177] = responseValue
            elif (labelName == "Dress"):
                    sagemakerPayload[178] = responseValue
            elif (labelName == "Stout"):
                    sagemakerPayload[179] = responseValue
            elif (labelName == "Brochure"):
                    sagemakerPayload[180] = responseValue
            elif (labelName == "Wallet"):
                    sagemakerPayload[181] = responseValue
            elif (labelName == "LED"):
                    sagemakerPayload[182] = responseValue
            elif (labelName == "Logo"):
                    sagemakerPayload[183] = responseValue
            elif (labelName == "Painting"):
                    sagemakerPayload[184] = responseValue
            elif (labelName == "Planter"):
                    sagemakerPayload[185] = responseValue
            elif (labelName == "Apparel"):
                    sagemakerPayload[186] = responseValue
            elif (labelName == "Mail"):
                    sagemakerPayload[187] = responseValue
            elif (labelName == "Pendant"):
                    sagemakerPayload[188] = responseValue
            elif (labelName == "Wine Glass"):
                    sagemakerPayload[189] = responseValue
            elif (labelName == "Paper"):
                    sagemakerPayload[190] = responseValue
            elif (labelName == "Jar"):
                    sagemakerPayload[191] = responseValue
            elif (labelName == "Sign"):
                    sagemakerPayload[192] = responseValue
            elif (labelName == "Airmail"):
                    sagemakerPayload[193] = responseValue
            elif (labelName == "Interior Design"):
                    sagemakerPayload[194] = responseValue
            elif (labelName == "Petal"):
                    sagemakerPayload[195] = responseValue
            elif (labelName == "PEZ Dispenser"):
                    sagemakerPayload[196] = responseValue
            elif (labelName == "Dune"):
                    sagemakerPayload[197] = responseValue
            elif (labelName == "Confectionery"):
                    sagemakerPayload[198] = responseValue
            elif (labelName == "Document"):
                    sagemakerPayload[199] = responseValue
            elif (labelName == "Goggles"):
                    sagemakerPayload[200] = responseValue
            elif (labelName == "Sculpture"):
                    sagemakerPayload[201] = responseValue
            elif (labelName == "Napkin"):
                    sagemakerPayload[202] = responseValue
            elif (labelName == "Advertisement"):
                    sagemakerPayload[203] = responseValue
            elif (labelName == "Cup"):
                    sagemakerPayload[204] = responseValue
            elif (labelName == "Herbs"):
                    sagemakerPayload[205] = responseValue
            elif (labelName == "Head"):
                    sagemakerPayload[206] = responseValue
            elif (labelName == "Dishwasher"):
                    sagemakerPayload[207] = responseValue
            elif (labelName == "Fossil"):
                    sagemakerPayload[208] = responseValue
            elif (labelName == "Capsule"):
                    sagemakerPayload[209] = responseValue
            elif (labelName == "Creme"):
                    sagemakerPayload[210] = responseValue
            elif (labelName == "Cushion"):
                    sagemakerPayload[211] = responseValue
            elif (labelName == "Ashtray"):
                    sagemakerPayload[212] = responseValue
            elif (labelName == "Seasoning"):
                    sagemakerPayload[213] = responseValue
            elif (labelName == "Handle"):
                    sagemakerPayload[214] = responseValue
            elif (labelName == "Land"):
                    sagemakerPayload[215] = responseValue
            elif (labelName == "Towel"):
                    sagemakerPayload[216] = responseValue
            elif (labelName == "Doormat"):
                    sagemakerPayload[217] = responseValue
            elif (labelName == "Spoon"):
                    sagemakerPayload[218] = responseValue
            elif (labelName == "Art"):
                    sagemakerPayload[219] = responseValue
            elif (labelName == "Cake"):
                    sagemakerPayload[220] = responseValue
            elif (labelName == "Trademark"):
                    sagemakerPayload[221] = responseValue
            elif (labelName == "Envelope"):
                    sagemakerPayload[222] = responseValue
            elif (labelName == "Texture"):
                    sagemakerPayload[223] = responseValue
            elif (labelName == "Bud"):
                    sagemakerPayload[224] = responseValue
            elif (labelName == "Clam"):
                    sagemakerPayload[225] = responseValue
            elif (labelName == "Female"):
                    sagemakerPayload[226] = responseValue
            elif (labelName == "Fish"):
                    sagemakerPayload[227] = responseValue
            elif (labelName == "Team"):
                    sagemakerPayload[228] = responseValue
            elif (labelName == "Bun"):
                    sagemakerPayload[229] = responseValue
            elif (labelName == "Face"):
                    sagemakerPayload[230] = responseValue
            elif (labelName == "Vegetable"):
                    sagemakerPayload[231] = responseValue
            elif (labelName == "Toothbrush"):
                    sagemakerPayload[232] = responseValue
            elif (labelName == "Window"):
                    sagemakerPayload[233] = responseValue
            elif (labelName == "Nature"):
                    sagemakerPayload[234] = responseValue
            elif (labelName == "Bullet"):
                    sagemakerPayload[235] = responseValue
            elif (labelName == "Ticket"):
                    sagemakerPayload[236] = responseValue
            elif (labelName == "Novel"):
                    sagemakerPayload[237] = responseValue
            elif (labelName == "Deodorant"):
                    sagemakerPayload[238] = responseValue
            elif (labelName == "Rug"):
                    sagemakerPayload[239] = responseValue
            elif (labelName == "Footwear"):
                    sagemakerPayload[240] = responseValue
            elif (labelName == "Chocolate"):
                    sagemakerPayload[241] = responseValue
            elif (labelName == "Ice"):
                    sagemakerPayload[242] = responseValue
            elif (labelName == "Shower Faucet"):
                    sagemakerPayload[243] = responseValue
            elif (labelName == "Photography"):
                    sagemakerPayload[244] = responseValue
            elif (labelName == "Vase"):
                    sagemakerPayload[245] = responseValue
            elif (labelName == "Ring"):
                    sagemakerPayload[246] = responseValue
            elif (labelName == "Chandelier"):
                    sagemakerPayload[247] = responseValue
            elif (labelName == "Lens Cap"):
                    sagemakerPayload[248] = responseValue
            elif (labelName == "Hat"):
                    sagemakerPayload[249] = responseValue
            elif (labelName == "Icicle"):
                    sagemakerPayload[250] = responseValue
            elif (labelName == "Display"):
                    sagemakerPayload[251] = responseValue
            elif (labelName == "Hammer"):
                    sagemakerPayload[252] = responseValue
            elif (labelName == "Dollar"):
                    sagemakerPayload[253] = responseValue
            elif (labelName == "Label"):
                    sagemakerPayload[254] = responseValue
            elif (labelName == "Alcohol"):
                    sagemakerPayload[255] = responseValue
            elif (labelName == "Page"):
                    sagemakerPayload[256] = responseValue
            elif (labelName == "Photo"):
                    sagemakerPayload[257] = responseValue
            elif (labelName == "Syrup"):
                    sagemakerPayload[258] = responseValue
            elif (labelName == "Coil"):
                    sagemakerPayload[259] = responseValue
            elif (labelName == "Coin"):
                    sagemakerPayload[260] = responseValue
            elif (labelName == "Asphalt"):
                    sagemakerPayload[261] = responseValue
            elif (labelName == "Sink"):
                    sagemakerPayload[262] = responseValue
            elif (labelName == "Bracelet"):
                    sagemakerPayload[263] = responseValue
            elif (labelName == "Town"):
                    sagemakerPayload[264] = responseValue
            elif (labelName == "Potted Plant"):
                    sagemakerPayload[265] = responseValue
            elif (labelName == "Desk"):
                    sagemakerPayload[266] = responseValue
            elif (labelName == "Beverage"):
                    sagemakerPayload[267] = responseValue
            elif (labelName == "Absinthe"):
                    sagemakerPayload[268] = responseValue
            elif (labelName == "Bronze"):
                    sagemakerPayload[269] = responseValue
            elif (labelName == "Architecture"):
                    sagemakerPayload[270] = responseValue
            elif (labelName == "Clothing"):
                    sagemakerPayload[271] = responseValue
            elif (labelName == "Canvas"):
                    sagemakerPayload[272] = responseValue
            elif (labelName == "Lightbulb"):
                    sagemakerPayload[273] = responseValue
            elif (labelName == "Aluminium"):
                    sagemakerPayload[274] = responseValue
            elif (labelName == "Canned Goods"):
                    sagemakerPayload[275] = responseValue
            elif (labelName == "Spoke"):
                    sagemakerPayload[276] = responseValue
            elif (labelName == "Droplet"):
                    sagemakerPayload[277] = responseValue
            elif (labelName == "Pump"):
                    sagemakerPayload[278] = responseValue
            elif (labelName == "Ink Bottle"):
                    sagemakerPayload[279] = responseValue
            elif (labelName == "Broccoli"):
                    sagemakerPayload[280] = responseValue
            elif (labelName == "Khaki"):
                    sagemakerPayload[281] = responseValue
            elif (labelName == "Electrical Device"):
                    sagemakerPayload[282] = responseValue
            elif (labelName == "Linen"):
                    sagemakerPayload[283] = responseValue
            elif (labelName == "Andrena"):
                    sagemakerPayload[284] = responseValue
            elif (labelName == "Newsstand"):
                    sagemakerPayload[285] = responseValue
            elif (labelName == "Diaper"):
                    sagemakerPayload[286] = responseValue
            elif (labelName == "Crystal"):
                    sagemakerPayload[287] = responseValue
            elif (labelName == "Anther"):
                    sagemakerPayload[288] = responseValue
            elif (labelName == "Package Delivery"):
                    sagemakerPayload[289] = responseValue
            elif (labelName == "Transportation"):
                    sagemakerPayload[290] = responseValue
            elif (labelName == "Coke"):
                    sagemakerPayload[291] = responseValue
            elif (labelName == "Shelf"):
                    sagemakerPayload[292] = responseValue
            elif (labelName == "Hair Drier"):
                    sagemakerPayload[293] = responseValue
            elif (labelName == "Plant"):
                    sagemakerPayload[294] = responseValue
            elif (labelName == "Figurine"):
                    sagemakerPayload[295] = responseValue
            elif (labelName == "Ammunition"):
                    sagemakerPayload[296] = responseValue
            elif (labelName == "Frisbee"):
                    sagemakerPayload[297] = responseValue
            elif (labelName == "Modern Art"):
                    sagemakerPayload[298] = responseValue
            elif (labelName == "Bomb"):
                    sagemakerPayload[299] = responseValue
            elif (labelName == "Can Opener"):
                    sagemakerPayload[300] = responseValue
            elif (labelName == "Wood"):
                    sagemakerPayload[301] = responseValue
            elif (labelName == "Spray Can"):
                    sagemakerPayload[302] = responseValue
            elif (labelName == "Tile"):
                    sagemakerPayload[303] = responseValue
            elif (labelName == "Wasp"):
                    sagemakerPayload[304] = responseValue
            elif (labelName == "Rubber Eraser"):
                    sagemakerPayload[305] = responseValue
            elif (labelName == "Business Card"):
                    sagemakerPayload[306] = responseValue
            elif (labelName == "Alloy Wheel"):
                    sagemakerPayload[307] = responseValue
            elif (labelName == "Double Sink"):
                    sagemakerPayload[308] = responseValue
            elif (labelName == "Shopping Bag"):
                    sagemakerPayload[309] = responseValue
            elif (labelName == "Blossom"):
                    sagemakerPayload[310] = responseValue
            elif (labelName == "Carton"):
                    sagemakerPayload[311] = responseValue
            elif (labelName == "Green"):
                    sagemakerPayload[312] = responseValue
            elif (labelName == "Word"):
                    sagemakerPayload[313] = responseValue
            elif (labelName == "Pickle"):
                    sagemakerPayload[314] = responseValue
            elif (labelName == "Shark"):
                    sagemakerPayload[315] = responseValue
            elif (labelName == "Furniture"):
                    sagemakerPayload[316] = responseValue
            elif (labelName == "Flashlight"):
                    sagemakerPayload[317] = responseValue
            elif (labelName == "Dessert"):
                    sagemakerPayload[318] = responseValue
            elif (labelName == "Bread"):
                    sagemakerPayload[319] = responseValue
            elif (labelName == "Bottle"):
                    sagemakerPayload[320] = responseValue
            elif (labelName == "Book"):
                    sagemakerPayload[321] = responseValue
            elif (labelName == "Ornament"):
                    sagemakerPayload[322] = responseValue
            elif (labelName == "Cooktop"):
                    sagemakerPayload[323] = responseValue
            elif (labelName == "Computer"):
                    sagemakerPayload[324] = responseValue
            elif (labelName == "Medication"):
                    sagemakerPayload[325] = responseValue
            elif (labelName == "Arrowhead"):
                    sagemakerPayload[326] = responseValue
            elif (labelName == "Invertebrate"):
                    sagemakerPayload[327] = responseValue
            elif (labelName == "Team Sport"):
                    sagemakerPayload[328] = responseValue
            elif (labelName == "Automobile"):
                    sagemakerPayload[329] = responseValue
            elif (labelName == "Water Jug"):
                    sagemakerPayload[330] = responseValue
            elif (labelName == "Pants"):
                    sagemakerPayload[331] = responseValue
            elif (labelName == "Shoe"):
                    sagemakerPayload[332] = responseValue
            elif (labelName == "Letter"):
                    sagemakerPayload[333] = responseValue
            elif (labelName == "Wedding Cake"):
                    sagemakerPayload[334] = responseValue
            elif (labelName == "Shop"):
                    sagemakerPayload[335] = responseValue
            elif (labelName == "Switch"):
                    sagemakerPayload[336] = responseValue
            elif (labelName == "Lotion"):
                    sagemakerPayload[337] = responseValue
            elif (labelName == "Animal"):
                    sagemakerPayload[338] = responseValue
            elif (labelName == "Softball"):
                    sagemakerPayload[339] = responseValue
            elif (labelName == "Glass"):
                    sagemakerPayload[340] = responseValue
            elif (labelName == "Tarmac"):
                    sagemakerPayload[341] = responseValue
            elif (labelName == "Plastic"):
                    sagemakerPayload[342] = responseValue
            elif (labelName == "Outdoors"):
                    sagemakerPayload[343] = responseValue
            elif (labelName == "Contact Lens"):
                    sagemakerPayload[344] = responseValue
            elif (labelName == "Appliance"):
                    sagemakerPayload[345] = responseValue
            elif (labelName == "Beer Bottle"):
                    sagemakerPayload[346] = responseValue
            elif (labelName == "Gas Pump"):
                    sagemakerPayload[347] = responseValue
            elif (labelName == "Wax Seal"):
                    sagemakerPayload[348] = responseValue
            elif (labelName == "Handrail"):
                    sagemakerPayload[349] = responseValue
            elif (labelName == "Guitar"):
                    sagemakerPayload[350] = responseValue
            elif (labelName == "Water Bottle"):
                    sagemakerPayload[351] = responseValue
            elif (labelName == "Table"):
                    sagemakerPayload[352] = responseValue
            elif (labelName == "Flagstone"):
                    sagemakerPayload[353] = responseValue
            elif (labelName == "Soup Bowl"):
                    sagemakerPayload[354] = responseValue
            elif (labelName == "Lunch"):
                    sagemakerPayload[355] = responseValue
            elif (labelName == "Graphics"):
                    sagemakerPayload[356] = responseValue
            elif (labelName == "Sack"):
                    sagemakerPayload[357] = responseValue
            elif (labelName == "Tray"):
                    sagemakerPayload[358] = responseValue
            elif (labelName == "Indoors"):
                    sagemakerPayload[359] = responseValue
            elif (labelName == "Modem"):
                    sagemakerPayload[360] = responseValue
            elif (labelName == "Pillow"):
                    sagemakerPayload[361] = responseValue
            elif (labelName == "Id Cards"):
                    sagemakerPayload[362] = responseValue
            elif (labelName == "Seashell"):
                    sagemakerPayload[363] = responseValue
            elif (labelName == "Camera Lens"):
                    sagemakerPayload[364] = responseValue
            elif (labelName == "Mattress"):
                    sagemakerPayload[365] = responseValue
            elif (labelName == "Window Shade"):
                    sagemakerPayload[366] = responseValue
            elif (labelName == "Incense"):
                    sagemakerPayload[367] = responseValue
            elif (labelName == "Mixer"):
                    sagemakerPayload[368] = responseValue
            elif (labelName == "Cream"):
                    sagemakerPayload[369] = responseValue
            elif (labelName == "Steamer"):
                    sagemakerPayload[370] = responseValue
            elif (labelName == "Velvet"):
                    sagemakerPayload[371] = responseValue
            elif (labelName == "Drink"):
                    sagemakerPayload[372] = responseValue
            elif (labelName == "Soap"):
                    sagemakerPayload[373] = responseValue
            elif (labelName == "Crash Helmet"):
                    sagemakerPayload[374] = responseValue
            elif (labelName == "Sticker"):
                    sagemakerPayload[375] = responseValue
            elif (labelName == "Sport"):
                    sagemakerPayload[376] = responseValue
            elif (labelName == "Bubble"):
                    sagemakerPayload[377] = responseValue
            elif (labelName == "Accessory"):
                    sagemakerPayload[378] = responseValue
            elif (labelName == "Computer Hardware"):
                    sagemakerPayload[379] = responseValue
            elif (labelName == "Necktie"):
                    sagemakerPayload[380] = responseValue
            elif (labelName == "Car Wheel"):
                    sagemakerPayload[381] = responseValue
            elif (labelName == "Woman"):
                    sagemakerPayload[382] = responseValue
            elif (labelName == "Sports"):
                    sagemakerPayload[383] = responseValue
            elif (labelName == "Brass Section"):
                    sagemakerPayload[384] = responseValue
            elif (labelName == "Rock"):
                    sagemakerPayload[385] = responseValue
            elif (labelName == "Hubcap"):
                    sagemakerPayload[386] = responseValue
            elif (labelName == "Porthole"):
                    sagemakerPayload[387] = responseValue
            elif (labelName == "Gin"):
                    sagemakerPayload[388] = responseValue
            elif (labelName == "Tire"):
                    sagemakerPayload[389] = responseValue
            elif (labelName == "Can"):
                    sagemakerPayload[390] = responseValue
            elif (labelName == "Car"):
                    sagemakerPayload[391] = responseValue
            elif (labelName == "Poster"):
                    sagemakerPayload[392] = responseValue
            elif (labelName == "Concrete"):
                    sagemakerPayload[393] = responseValue
            elif (labelName == "Bumper"):
                    sagemakerPayload[394] = responseValue
            elif (labelName == "Wheel"):
                    sagemakerPayload[395] = responseValue
            elif (labelName == "Sock"):
                    sagemakerPayload[396] = responseValue
            elif (labelName == "Cross"):
                    sagemakerPayload[397] = responseValue
            elif (labelName == "Screen"):
                    sagemakerPayload[398] = responseValue
            elif (labelName == "Meal"):
                    sagemakerPayload[399] = responseValue
            elif (labelName == "Musical Instrument"):
                    sagemakerPayload[400] = responseValue
            elif (labelName == "Burger"):
                    sagemakerPayload[401] = responseValue
            elif (labelName == "Dynamite"):
                    sagemakerPayload[402] = responseValue
            elif (labelName == "Pottery"):
                    sagemakerPayload[403] = responseValue
            elif (labelName == "Insect"):
                    sagemakerPayload[404] = responseValue
            elif (labelName == "Soda"):
                    sagemakerPayload[405] = responseValue
            elif (labelName == "Floor"):
                    sagemakerPayload[406] = responseValue
            elif (labelName == "Flower"):
                    sagemakerPayload[407] = responseValue
            elif (labelName == "Stain"):
                    sagemakerPayload[408] = responseValue
            elif (labelName == "Fruit"):
                    sagemakerPayload[409] = responseValue
            elif (labelName == "Egg"):
                    sagemakerPayload[410] = responseValue
            elif (labelName == "Bag"):
                    sagemakerPayload[411] = responseValue
            elif (labelName == "Plastic Wrap"):
                    sagemakerPayload[412] = responseValue
            elif (labelName == "Foil"):
                    sagemakerPayload[413] = responseValue
            elif (labelName == "Smoke Pipe"):
                    sagemakerPayload[414] = responseValue
            elif (labelName == "Hot Tub"):
                    sagemakerPayload[415] = responseValue
            elif (labelName == "Letterbox"):
                    sagemakerPayload[416] = responseValue
            elif (labelName == "Brick"):
                    sagemakerPayload[417] = responseValue
       
                    
        clientSM = boto3.client('sagemaker-runtime')
        
        print("SagemakerPayload len: " + str(len(sagemakerPayload)))
        sagemakerPayloadStr = ','.join(str(e) for e in sagemakerPayload)
        print("Sage maker payload = " + sagemakerPayloadStr)
        responseSageMaker = clientSM.invoke_endpoint(
            EndpointName='knn-2019-03-11-03-50-44-586',
            ContentType='text/csv',
            Body=sagemakerPayloadStr
        )
        sageresult = responseSageMaker['Body'].read().decode()
        payload["data"] = sageresult
        print("Sage maker response = " + sageresult)
    
    #Store into Redis
    url = "http://18.204.42.219:8081/result" # Set destination URL here
    post_fields = payload    # Set POST fields here

    request = Request(url, urlencode(post_fields).encode())
    #print(request)
    
    backend_resp = urlopen(request)
    #print(backend_resp)
    
    return {
        'statusCode': 200,
        'body': json.dumps(payload)
    }