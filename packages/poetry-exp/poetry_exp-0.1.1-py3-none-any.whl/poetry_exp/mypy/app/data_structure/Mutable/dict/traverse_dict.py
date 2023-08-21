result = {
     "msdtcValidateDict": {
		"NetworkDtcAccessAdmin": {
			"Status": True,
			"Value": "1"
		},
		"NetworkDtcClients": {
			"Status": True,
			"Value": "1"
		},
		"LuTransactions": {
			"Status": True,
			"Value": "1"
		},
		"NetworkDtcAccessInbound": {
			"Status": True,
			"Value": "1"
		}
     }
}

for key, val in result['msdtcValidateDict'].items():
    print val
    if val['Status']:
        print 'True'

