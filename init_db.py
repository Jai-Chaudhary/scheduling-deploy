from pymongo import MongoClient

client = MongoClient()
client.schedule.config.drop()

client.schedule.config.insert({
    'name': 'site',
    'data': {
		"1-55TH": {
			"machines": ["MR1", "MR2"],
			"horizon": {
				"begin": 450,
				"end": 1320
			}
		},
		"1-YORK": {
			"machines": ["MR1", "MR2"],
			"horizon": {
				"begin": 450,
				"end": 1320
			}
		},
		"1-W84TH": {
			"machines": ["W84MR3T418"],
			"horizon": {
				"begin": 450,
				"end": 1200
			}
        }
    }
})
